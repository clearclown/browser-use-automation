#!/usr/bin/env python3
"""
Automated Research Assistant - Streamlit Web UI
完全自動化研究支援システム - Streamlit Webインターフェース

複数行入力、マルチLLMプロバイダー選択、インタラクティブな操作が可能なGUI
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from automated_research.llm_provider import get_available_providers, get_llm
from automated_research.main import AutomatedResearchAssistant


def init_session_state():
	"""セッション状態の初期化"""
	if 'research_running' not in st.session_state:
		st.session_state.research_running = False
	if 'results' not in st.session_state:
		st.session_state.results = None
	if 'logs' not in st.session_state:
		st.session_state.logs = []


def add_log(message: str):
	"""ログメッセージを追加"""
	timestamp = datetime.now().strftime('%H:%M:%S')
	st.session_state.logs.append(f'[{timestamp}] {message}')


async def run_research(
	provider: str,
	model: str | None,
	research_topic: str,
	research_question: str,
	keywords: list[str],
	specific_interests: list[str],
	research_background: str,
	year_start: int,
	year_end: int,
	max_papers: int,
	headless: bool,
):
	"""研究調査を実行"""
	try:
		# ブラウザタイムアウトを延長（環境変数で設定 - 最初に実行）
		import os

		os.environ['TIMEOUT_NavigateToUrlEvent'] = '60'  # 60秒
		os.environ['TIMEOUT_BrowserStateRequestEvent'] = '120'  # 120秒
		os.environ['TIMEOUT_ClickElementEvent'] = '30'  # 30秒

		add_log(f'🚀 研究調査を開始: {research_topic}')
		add_log(f'📊 LLMプロバイダー: {provider}')

		# LLM初期化
		llm = get_llm(provider=provider, model=model, temperature=0.4)
		add_log(f'✅ {provider.upper()} を初期化完了')

		# システム初期化
		assistant = AutomatedResearchAssistant(
			llm=llm, headless=headless, max_papers=max_papers, non_interactive=True, research_topic=research_topic
		)

		# 研究情報を手動設定（対話型スキップ）
		research_info = {
			'research_topic': research_topic,
			'research_question': research_question,
			'keywords': keywords,
			'specific_interests': specific_interests,
			'research_background': research_background,
			'year_range': {'start': year_start, 'end': year_end},
			'databases': ['ieee'],
		}

		# ステップ1: 研究情報保存
		add_log('📝 ステップ1: 研究情報を保存')
		output_path = assistant.data_dir / f'research_info_{assistant.session_id}.json'
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(research_info, f, indent=2, ensure_ascii=False)
		add_log(f'💾 {output_path}')

		# ステップ2: PRISMA検索戦略生成
		add_log('📊 ステップ2: PRISMA検索戦略を生成中...')
		search_strategy = await assistant._step2_generate_strategy(research_info)
		add_log(f'✅ {len(search_strategy.get("search_queries", []))}個の検索クエリを生成')

		# ステップ3: 論文検索
		add_log('🔍 ステップ3: IEEE Xploreで論文を検索中...')
		papers = await assistant._step3_search_papers(search_strategy)
		add_log(f'✅ {len(papers)}件の論文を収集')

		if not papers:
			add_log('⚠️ 論文が見つかりませんでした')
			return {
				'success': False,
				'message': '論文が見つかりませんでした。検索条件を見直してください。',
				'papers': [],
			}

		# ステップ4: レポート生成
		add_log(f'📝 ステップ4: {len(papers)}件の論文レポートを生成中...')
		reports = await assistant._step4_generate_reports(papers, research_info)
		add_log(f'✅ {len(reports)}件のレポートを生成完了')

		# ステップ5: 統合レポート生成
		add_log('📊 ステップ5: 統合レポートを生成中...')
		await assistant._step5_generate_summary(reports, research_info, search_strategy)
		add_log('✅ 統合レポート生成完了')

		# 結果を返す
		summary_path = assistant.reports_dir / f'summary_report_{assistant.session_id}.md'
		with open(summary_path, encoding='utf-8') as f:
			summary_content = f.read()

		add_log('🎉 すべての処理が完了しました！')

		return {
			'success': True,
			'message': '研究調査が正常に完了しました',
			'papers': papers,
			'reports': reports,
			'summary_report': summary_content,
			'summary_path': str(summary_path),
			'session_id': assistant.session_id,
		}

	except Exception as e:
		add_log(f'❌ エラー: {e}')
		return {'success': False, 'message': f'エラーが発生しました: {e}', 'papers': []}


def main():
	"""Streamlit メインアプリケーション"""
	st.set_page_config(page_title='自動研究支援システム', page_icon='🤖', layout='wide', initial_sidebar_state='expanded')

	init_session_state()

	# ヘッダー
	st.title('🤖 完全自動化研究支援システム')
	st.markdown('---')
	st.markdown(
		"""
	**PRISMA 2020準拠の自動文献調査システム**

	このシステムは以下を自動実行します：
	1. 研究内容のヒアリング
	2. PRISMA方式の検索戦略立案
	3. IEEE Xploreでの自動検索
	4. 論文の詳細分析（落合陽一式）
	5. 統合レポートの生成
	"""
	)

	# サイドバー: LLM設定
	with st.sidebar:
		st.header('⚙️ LLM設定')

		# 利用可能なプロバイダーを取得
		available_providers = get_available_providers()

		if not available_providers:
			st.error('❌ APIキーが設定されていません。.envファイルを確認してください。')
			st.stop()

		provider = st.selectbox(
			'LLMプロバイダー',
			options=available_providers,
			help='使用するLLMプロバイダーを選択（.envで設定されたAPIキーが必要）',
		)

		# プロバイダー別のデフォルトモデル
		default_models = {
			'openai': 'gpt-4o',
			'claude': 'claude-3-5-sonnet-20241022',
			'deepseek': 'deepseek-chat',
			'google': 'gemini-2.0-flash-exp',
			'groq': 'llama-3.3-70b-versatile',
		}

		model = st.text_input('モデル名（オプション）', value=default_models.get(provider, ''), help='空欄の場合はデフォルトモデルを使用')

		st.markdown('---')
		st.header('📊 検索設定')

		max_papers = st.slider('最大論文数', min_value=1, max_value=1000, value=10, step=1)
		headless = st.checkbox('ヘッドレスモード', value=True, help='ブラウザを非表示で実行（推奨）')

		year_start = st.number_input('開始年', min_value=2000, max_value=2025, value=2022, step=1)
		year_end = st.number_input('終了年', min_value=2000, max_value=2025, value=2025, step=1)

	# メインコンテンツ: 研究情報入力フォーム
	st.header('📝 研究情報入力')

	col1, col2 = st.columns([2, 1])

	with col1:
		research_topic = st.text_input(
			'研究トピック *',
			placeholder='例: Large Language Models (LLM) の最新研究動向',
			help='調査したい研究テーマを入力してください',
		)

		research_question = st.text_area(
			'研究課題・リサーチクエスチョン *',
			placeholder='例: LLMの性能向上、効率化、応用分野の最新技術は何か？',
			height=100,
			help='複数行で詳細に記述できます',
		)

		research_background = st.text_area(
			'研究背景',
			placeholder='例: LLMは自然言語処理の中核技術となっており、本調査では最新研究動向を体系的にレビューする。',
			height=150,
			help='研究の背景や目的を記述してください（複数行可）',
		)

	with col2:
		keywords_input = st.text_area(
			'キーワード（1行に1つ） *',
			placeholder='Large Language Model\nLLM\ntransformer\nGPT\nBERT',
			height=200,
			help='検索キーワードを1行に1つずつ入力',
		)

		interests_input = st.text_area(
			'特定の関心領域（1行に1つ）',
			placeholder='モデルアーキテクチャ改善\n計算効率の向上\nFew-shot learning',
			height=200,
			help='特に注目したい領域を1行に1つずつ入力',
		)

	# 入力バリデーション
	keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
	specific_interests = [i.strip() for i in interests_input.split('\n') if i.strip()]

	# 実行ボタン
	st.markdown('---')

	col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])

	with col_btn1:
		run_button = st.button('🚀 研究調査を開始', type='primary', disabled=st.session_state.research_running, use_container_width=True)

	with col_btn2:
		if st.button('🗑️ ログをクリア', use_container_width=True):
			st.session_state.logs = []
			st.rerun()

	# 入力チェック
	if run_button:
		if not research_topic or not research_question or not keywords:
			st.error('❌ 必須項目（*）を入力してください')
		else:
			st.session_state.research_running = True
			st.session_state.results = None

			# 非同期実行
			with st.spinner('🔄 研究調査を実行中...'):
				results = asyncio.run(
					run_research(
						provider=provider,
						model=model if model else None,
						research_topic=research_topic,
						research_question=research_question,
						keywords=keywords,
						specific_interests=specific_interests,
						research_background=research_background,
						year_start=year_start,
						year_end=year_end,
						max_papers=max_papers,
						headless=headless,
					)
				)

				st.session_state.results = results
				st.session_state.research_running = False
				st.rerun()

	# ログ表示
	if st.session_state.logs:
		st.markdown('---')
		st.header('📋 実行ログ')
		log_container = st.container(height=300)
		with log_container:
			for log in st.session_state.logs:
				st.text(log)

	# 結果表示
	if st.session_state.results:
		st.markdown('---')
		st.header('📊 結果')

		results = st.session_state.results

		if results['success']:
			st.success(f'✅ {results["message"]}')

			# タブで結果を表示
			tab1, tab2, tab3 = st.tabs(['📚 収集論文', '📄 統合レポート', '📁 生成ファイル'])

			with tab1:
				st.subheader(f'収集論文一覧（{len(results["papers"])}件）')

				for idx, paper in enumerate(results['papers'], 1):
					with st.expander(f'{idx}. {paper.get("title", "Unknown")}'):
						st.markdown(f'**著者:** {", ".join(paper.get("authors", ["Unknown"]))}')
						st.markdown(f'**発行日:** {paper.get("published_date", "N/A")}')
						st.markdown(f'**URL:** [{paper.get("url", "N/A")}]({paper.get("url", "#")})')

						if 'abstract' in paper:
							st.markdown('**概要:**')
							st.markdown(paper['abstract'])

			with tab2:
				st.subheader('統合レポート')
				st.markdown(results.get('summary_report', ''))

				# ダウンロードボタン
				if 'summary_report' in results:
					st.download_button(
						label='📥 レポートをダウンロード（Markdown）',
						data=results['summary_report'],
						file_name=f'research_report_{results["session_id"]}.md',
						mime='text/markdown',
					)

			with tab3:
				st.subheader('生成されたファイル')
				st.markdown(f'**セッションID:** `{results["session_id"]}`')
				st.markdown(f'**統合レポート:** `{results.get("summary_path", "N/A")}`')
				st.markdown('**個別レポート:** `automated_research/reports/session_{}/`'.format(results['session_id']))
				st.markdown('**データファイル:** `automated_research/data/`')

		else:
			st.error(f'❌ {results["message"]}')


if __name__ == '__main__':
	main()
