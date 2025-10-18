#!/usr/bin/env python3
"""
Automated Research Assistant - Main Entry Point
完全自動化研究支援システム - メインエントリーポイント

このスクリプトは以下のステップを自動実行します：
1. ユーザーへの対話型ヒアリング
2. PRISMA方式の検索戦略生成
3. IEEE Xploreでの自動検索と論文収集
4. 各論文の落合陽一式レポート生成
5. 統合レポートの作成

Usage:
    python -m automated_research.main

    または

    python automated_research/main.py
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from automated_research.llm_provider import get_llm, print_provider_info
from automated_research.ochiai_report_generator import OchiaiReportGenerator
from automated_research.prisma_search_strategy import PRISMASearchStrategyGenerator
from automated_research.research_interview import ResearchInterviewer
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.integrations.ieee_search import IEEESearchService

load_dotenv()

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


class AutomatedResearchAssistant:
	"""完全自動化研究支援システム"""

	def __init__(
		self, llm: Any | None = None, headless: bool = False, max_papers: int = 20, non_interactive: bool = False, research_topic: str | None = None
	):
		"""
		Initialize the automated research assistant

		Args:
			llm: Language model instance (if None, will use get_llm() to auto-select from env)
			headless: Run browser in headless mode
			max_papers: Maximum number of papers to collect
			non_interactive: Skip interactive interview and use predefined research info
			research_topic: Research topic for non-interactive mode
		"""
		self.llm = llm or get_llm(temperature=0.4)
		self.headless = headless
		self.max_papers = max_papers
		self.non_interactive = non_interactive
		self.research_topic = research_topic

		# データ保存ディレクトリ
		self.base_dir = Path('automated_research')
		self.data_dir = self.base_dir / 'data'
		self.reports_dir = self.base_dir / 'reports'
		self.logs_dir = self.base_dir / 'logs'

		# ディレクトリ作成
		for dir_path in [self.data_dir, self.reports_dir, self.logs_dir]:
			dir_path.mkdir(parents=True, exist_ok=True)

		# セッションID（ファイル名に使用）
		self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

	async def run_full_pipeline(self) -> None:
		"""完全パイプラインを実行"""
		print('\n' + '=' * 100)
		print('🤖 完全自動化研究支援システム')
		print('=' * 100)
		print('\nこのシステムは以下を自動実行します：')
		print('  1. 研究内容のヒアリング')
		print('  2. PRISMA方式の検索戦略立案')
		print('  3. IEEE Xploreでの自動検索')
		print('  4. 論文の詳細分析（落合陽一式）')
		print('  5. 統合レポートの生成')
		print('\n' + '=' * 100 + '\n')

		try:
			# ステップ1: ユーザーヒアリング
			research_info = await self._step1_interview()

			# ステップ2: PRISMA検索戦略生成
			search_strategy = await self._step2_generate_strategy(research_info)

			# ステップ3: IEEE自動検索
			papers = await self._step3_search_papers(search_strategy)

			if not papers:
				print('\n⚠️  論文が見つかりませんでした。検索条件を見直してください。')
				return

			# ステップ4: 各論文のレポート生成
			reports = await self._step4_generate_reports(papers, research_info)

			# ステップ5: 統合レポート生成
			await self._step5_generate_summary(reports, research_info, search_strategy)

			# 完了
			self._print_completion_summary()

		except KeyboardInterrupt:
			print('\n\n⚠️  処理が中断されました。')
			logger.info('Process interrupted by user')
		except Exception as e:
			print(f'\n\n❌ エラーが発生しました: {e}')
			logger.error(f'Fatal error in pipeline: {e}', exc_info=True)
			raise

	async def _step1_interview(self) -> dict[str, Any]:
		"""ステップ1: ユーザーヒアリング"""
		print('\n' + '🎯 ' * 30)
		print('ステップ 1/5: 研究内容のヒアリング')
		print('🎯 ' * 30 + '\n')

		if self.non_interactive:
			# 非対話型モード：事前定義された研究情報を使用
			print('📝 非対話型モード：事前定義された研究情報を使用\n')

			topic = self.research_topic or 'Large Language Models (LLM) の最新研究動向'
			research_info = {
				'research_topic': topic,
				'research_question': f'{topic}における最新技術と応用分野は何か？',
				'keywords': [
					'large language model',
					'LLM',
					'transformer',
					'neural network',
					'deep learning',
					'natural language processing',
				],
				'specific_interests': [
					'最新のアーキテクチャ改善',
					'効率化手法',
					'応用分野',
					'性能向上技術',
				],
				'research_background': f'{topic}の研究動向を体系的に調査する。',
				'year_range': {'start': 2022, 'end': 2025},
				'databases': ['ieee'],
			}

			print(f'✅ 研究トピック: {research_info["research_topic"]}')
			print(f'✅ 研究期間: {research_info["year_range"]["start"]}-{research_info["year_range"]["end"]}\n')
		else:
			# 対話型モード
			interviewer = ResearchInterviewer(llm=self.llm)
			research_info = await interviewer.conduct_interview()

		# 保存
		output_path = self.data_dir / f'research_info_{self.session_id}.json'
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(research_info, f, indent=2, ensure_ascii=False)

		print(f'💾 研究情報を保存: {output_path}\n')

		return research_info

	async def _step2_generate_strategy(self, research_info: dict[str, Any]) -> dict[str, Any]:
		"""ステップ2: PRISMA検索戦略生成"""
		print('\n' + '📊 ' * 30)
		print('ステップ 2/5: PRISMA方式検索戦略の生成')
		print('📊 ' * 30 + '\n')

		generator = PRISMASearchStrategyGenerator(llm=self.llm)
		search_strategy = await generator.generate_search_strategy(research_info)

		# 保存
		output_path = self.data_dir / f'search_strategy_{self.session_id}.json'
		generator.save_search_strategy(search_strategy, output_path)

		return search_strategy

	async def _step3_search_papers(self, search_strategy: dict[str, Any]) -> list[dict[str, Any]]:
		"""ステップ3: IEEE自動検索"""
		print('\n' + '🔍 ' * 30)
		print('ステップ 3/5: IEEE Xploreでの自動検索')
		print('🔍 ' * 30 + '\n')

		search_queries = search_strategy.get('search_queries', [])
		if not search_queries:
			logger.warning('No search queries found')
			return []

		# ブラウザセッション作成
		profile = BrowserProfile(
			headless=self.headless,
			disable_security=False,
			extra_chromium_args=[
				'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
			],
		)
		browser_session = BrowserSession(browser_profile=profile)

		all_papers = []

		try:
			await browser_session.start()
			print('✅ ブラウザセッション開始\n')

			ieee_service = IEEESearchService()

			papers_per_query = max(5, self.max_papers // len(search_queries))

			for query_idx, query in enumerate(search_queries, 1):
				print(f'\n📝 検索 {query_idx}/{len(search_queries)}: "{query}"')

				try:
					# IEEE検索を実行
					papers = await ieee_service.search(query=query, max_results=papers_per_query, browser_session=browser_session)

					print(f'  ✅ {len(papers)}件の論文を発見')

					# 検索クエリ情報を追加
					for paper in papers:
						paper['search_query'] = query

					all_papers.extend(papers)

				except Exception as e:
					logger.error(f'Error searching for "{query}": {e}')
					print(f'  ⚠️  エラー: {e}')
					continue

				# 上限に達したら終了
				if len(all_papers) >= self.max_papers:
					print(f'\n🎯 目標論文数 {self.max_papers} に到達')
					break

				# レート制限を避けるため待機
				await asyncio.sleep(2)

		finally:
			await browser_session.kill()
			print('\n✅ ブラウザセッション終了')

		# 重複除去
		unique_papers = self._deduplicate_papers(all_papers)
		unique_papers = unique_papers[: self.max_papers]

		print(f'\n✅ 合計 {len(unique_papers)} 件の論文を収集')
		print(f'   （重複除去前: {len(all_papers)} 件）')

		# 保存
		output_path = self.data_dir / f'collected_papers_{self.session_id}.json'
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump({'papers': unique_papers, 'total_count': len(unique_papers)}, f, indent=2, ensure_ascii=False)

		print(f'\n💾 論文情報を保存: {output_path}')

		return unique_papers

	async def _step4_generate_reports(self, papers: list[dict[str, Any]], research_info: dict[str, Any]) -> list[dict[str, str]]:
		"""ステップ4: 各論文の落合陽一式レポート生成"""
		print('\n' + '📝 ' * 30)
		print('ステップ 4/5: 各論文の詳細分析（落合陽一式）')
		print('📝 ' * 30 + '\n')

		generator = OchiaiReportGenerator(llm=self.llm)
		reports = []

		# レポート保存ディレクトリ
		session_reports_dir = self.reports_dir / f'session_{self.session_id}'
		session_reports_dir.mkdir(parents=True, exist_ok=True)

		for idx, paper in enumerate(papers, 1):
			print(f'\n[{idx}/{len(papers)}] 分析中: {paper.get("title", "Unknown")[:80]}...')

			try:
				# レポート生成
				report = await generator.generate_paper_report(paper, research_info, pdf_content=None)

				# 保存
				safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in paper.get('title', 'paper'))
				safe_title = safe_title[:50]
				filename = f'{idx:03d}_{safe_title}.md'

				report_path = session_reports_dir / filename
				with open(report_path, 'w', encoding='utf-8') as f:
					f.write(report)

				reports.append({'paper_info': paper, 'report': report, 'file_path': str(report_path)})

				print(f'  ✅ レポート保存: {report_path.name}')

			except Exception as e:
				logger.error(f'Error generating report for paper {idx}: {e}')
				print(f'  ⚠️  レポート生成エラー: {e}')
				continue

			# APIレート制限を避けるため少し待機
			if idx < len(papers):
				await asyncio.sleep(1)

		print(f'\n✅ {len(reports)}/{len(papers)} 件のレポートを生成')

		return reports

	async def _step5_generate_summary(
		self, reports: list[dict[str, str]], research_info: dict[str, Any], search_strategy: dict[str, Any]
	) -> None:
		"""ステップ5: 統合レポート生成"""
		print('\n' + '📊 ' * 30)
		print('ステップ 5/5: 統合レポートの生成')
		print('📊 ' * 30 + '\n')

		generator = OchiaiReportGenerator(llm=self.llm)

		# すべてのレポートテキストを抽出
		all_report_texts = [r['report'] for r in reports]

		# 統合レポート生成
		summary_report = await generator.generate_summary_report(all_report_texts, research_info, search_strategy)

		# 保存
		summary_path = self.reports_dir / f'summary_report_{self.session_id}.md'
		with open(summary_path, 'w', encoding='utf-8') as f:
			f.write(summary_report)

		print(f'\n✅ 統合レポートを生成: {summary_path}')

		# 追加：論文リスト一覧もJSON形式で保存
		papers_list = [r['paper_info'] for r in reports]
		papers_list_path = self.reports_dir / f'papers_list_{self.session_id}.json'
		with open(papers_list_path, 'w', encoding='utf-8') as f:
			json.dump({'papers': papers_list, 'total': len(papers_list)}, f, indent=2, ensure_ascii=False)

		print(f'✅ 論文リストを保存: {papers_list_path}')

	def _deduplicate_papers(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""タイトルベースで重複除去"""
		seen_titles = set()
		unique_papers = []

		for paper in papers:
			title = paper.get('title', '').lower().strip()
			if title and title not in seen_titles:
				seen_titles.add(title)
				unique_papers.append(paper)

		return unique_papers

	def _print_completion_summary(self) -> None:
		"""完了サマリーを表示"""
		print('\n\n' + '=' * 100)
		print('🎉 すべての処理が完了しました！')
		print('=' * 100)
		print('\n生成されたファイル:')
		print(f'  📁 データディレクトリ: {self.data_dir}')
		print(f'  📁 レポートディレクトリ: {self.reports_dir}')
		print('\n主要な成果物:')
		print(f'  📝 研究情報: {self.data_dir}/research_info_{self.session_id}.json')
		print(f'  📊 検索戦略: {self.data_dir}/search_strategy_{self.session_id}.json')
		print(f'  📚 収集論文: {self.data_dir}/collected_papers_{self.session_id}.json')
		print(f'  📄 個別レポート: {self.reports_dir}/session_{self.session_id}/')
		print(f'  📖 統合レポート: {self.reports_dir}/summary_report_{self.session_id}.md')
		print('\n' + '=' * 100 + '\n')


async def main():
	"""メインエントリーポイント"""
	import argparse
	import os

	# ブラウザタイムアウトを延長（環境変数で設定）
	# ブラウザ起動関連（最も重要）
	os.environ.setdefault('TIMEOUT_BrowserStartEvent', '180')  # 180秒（ブラウザ起動全体）
	os.environ.setdefault('TIMEOUT_BrowserLaunchEvent', '180')  # 180秒（ブラウザプロセス起動）
	os.environ.setdefault('TIMEOUT_CDP_URL_WAIT', '180')  # 180秒（CDP URL待機）
	os.environ.setdefault('TIMEOUT_BrowserConnectedEvent', '120')  # 120秒（ブラウザ接続）
	os.environ.setdefault('TIMEOUT_TabCreatedEvent', '60')  # 60秒（タブ作成）

	# ブラウザ操作関連
	os.environ.setdefault('TIMEOUT_NavigateToUrlEvent', '90')  # 90秒（ページ遷移）
	os.environ.setdefault('TIMEOUT_NavigationStartedEvent', '60')  # 60秒
	os.environ.setdefault('TIMEOUT_NavigationCompleteEvent', '90')  # 90秒
	os.environ.setdefault('TIMEOUT_BrowserStateRequestEvent', '120')  # 120秒
	os.environ.setdefault('TIMEOUT_ClickElementEvent', '30')  # 30秒
	os.environ.setdefault('TIMEOUT_UploadFileEvent', '60')  # 60秒

	# その他のイベント
	os.environ.setdefault('TIMEOUT_BrowserKillEvent', '30')  # 30秒
	os.environ.setdefault('TIMEOUT_BrowserStoppedEvent', '30')  # 30秒
	os.environ.setdefault('TIMEOUT_BrowserErrorEvent', '30')  # 30秒
	os.environ.setdefault('TIMEOUT_StorageStateSavedEvent', '60')  # 60秒
	os.environ.setdefault('TIMEOUT_StorageStateLoadedEvent', '60')  # 60秒
	os.environ.setdefault('TIMEOUT_FileDownloadedEvent', '120')  # 120秒（論文ダウンロード）

	parser = argparse.ArgumentParser(description='完全自動化研究支援システム')
	parser.add_argument('--headless', action='store_true', help='ヘッドレスモードで実行')
	parser.add_argument('--max-papers', type=int, default=20, help='収集する最大論文数（デフォルト: 20）')
	parser.add_argument(
		'--provider', type=str, default=None, help='LLMプロバイダー（openai, claude, deepseek, google, groq）'
	)
	parser.add_argument('--model', type=str, default=None, help='使用するLLMモデル（プロバイダーのデフォルトを使用する場合は省略可）')
	parser.add_argument('--non-interactive', action='store_true', help='非対話型モード（デモ用の事前定義された研究情報を使用）')
	parser.add_argument('--research-topic', type=str, default=None, help='研究トピック（--non-interactiveと併用）')

	args = parser.parse_args()

	# LLMプロバイダー情報を表示
	print_provider_info()

	# LLM初期化（環境変数またはコマンドライン引数から）
	llm = get_llm(provider=args.provider, model=args.model, temperature=0.4)

	# システム初期化
	assistant = AutomatedResearchAssistant(
		llm=llm, headless=args.headless, max_papers=args.max_papers, non_interactive=args.non_interactive, research_topic=args.research_topic
	)

	# パイプライン実行
	await assistant.run_full_pipeline()


if __name__ == '__main__':
	asyncio.run(main())
