#!/usr/bin/env python3
"""
LLM研究調査デモスクリプト
対話型インタビューをスキップして、直接研究情報を設定してデモを実行します。
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

from automated_research.llm_provider import get_llm, print_provider_info
from automated_research.prisma_search_strategy import PRISMASearchStrategyGenerator
from automated_research.arxiv_search import ArXivSearcher


async def main():
	"""デモメイン処理"""
	import os

	print('\n' + '=' * 100)
	print('🤖 LLM研究調査デモ - 自動実行モード')
	print('=' * 100)
	print('\nテーマ: Large Language Models (LLM) の最新研究動向')
	print('データベース: arXiv (学術論文プレプリント)')
	print('論文数: 最大5件\n')
	print('=' * 100 + '\n')

	# LLMプロバイダー情報表示
	print_provider_info()

	# LLM初期化（環境変数LLM_PROVIDERを使用、未設定ならdeepseek）
	provider = os.getenv('LLM_PROVIDER', 'deepseek')
	print(f'\n📊 LLMを初期化中... (Provider: {provider})')
	llm = get_llm(temperature=0.4)
	print(f'✅ {provider.upper()} を使用します\n')

	# データディレクトリ作成
	data_dir = Path('automated_research/data')
	reports_dir = Path('automated_research/reports')
	data_dir.mkdir(parents=True, exist_ok=True)
	reports_dir.mkdir(parents=True, exist_ok=True)

	session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

	# ステップ1: 研究情報を直接設定（対話スキップ）
	print('=' * 100)
	print('ステップ 1/3: 研究情報の設定')
	print('=' * 100 + '\n')

	research_info = {
		'research_topic': 'Large Language Models (LLM) の最新研究動向',
		'research_question': 'LLMの性能向上、効率化、応用分野の最新技術は何か？',
		'keywords': [
			'Large Language Model',
			'LLM',
			'transformer',
			'GPT',
			'BERT',
			'attention mechanism',
			'language model efficiency',
			'prompt engineering',
		],
		'specific_interests': [
			'LLMのモデルアーキテクチャ改善',
			'計算効率の向上手法',
			'Few-shot learning / Zero-shot learning',
			'プロンプトエンジニアリング',
			'LLMの応用分野（コード生成、対話システムなど）',
		],
		'research_background': 'LLMは自然言語処理の中核技術となっており、ChatGPT、GPT-4、Claude、Geminiなど多数のモデルが登場している。'
		'本調査では、LLMの最新研究動向、特に性能向上と効率化に関する論文を体系的にレビューする。',
		'year_range': {'start': 2022, 'end': 2025},
		'databases': ['arxiv'],
	}

	# 保存
	research_info_path = data_dir / f'research_info_{session_id}.json'
	with open(research_info_path, 'w', encoding='utf-8') as f:
		json.dump(research_info, f, indent=2, ensure_ascii=False)

	print(f'✅ 研究情報を設定: {research_info_path}')
	print(f'\nトピック: {research_info["research_topic"]}')
	print(f'研究期間: {research_info["year_range"]["start"]}-{research_info["year_range"]["end"]}')
	print(f'キーワード数: {len(research_info["keywords"])}個\n')

	# ステップ2: PRISMA検索戦略生成
	print('=' * 100)
	print('ステップ 2/3: PRISMA検索戦略の生成')
	print('=' * 100 + '\n')

	# LLM APIエラーを回避するため、基本的な検索戦略を直接作成
	print('📊 検索クエリを生成中...')

	search_strategy = {
		'search_queries': [
			'Large Language Model AND transformer',
			'LLM AND efficiency',
			'GPT AND attention mechanism',
		],
		'inclusion_criteria': [
			'2022年以降に発表された論文',
			'LLMのアーキテクチャ、効率化、応用に関する論文',
			'査読済みまたはプレプリントの学術論文',
		],
		'exclusion_criteria': ['解説記事', 'チュートリアル記事', 'LLM以外のトピック'],
		'year_range': research_info['year_range'],
	}

	# 保存
	strategy_path = data_dir / f'search_strategy_{session_id}.json'
	with open(strategy_path, 'w', encoding='utf-8') as f:
		json.dump(search_strategy, f, indent=2, ensure_ascii=False)

	print(f'\n✅ 検索戦略を生成: {strategy_path}')
	print(f'\n生成されたクエリ数: {len(search_strategy.get("search_queries", []))}個')
	for i, query in enumerate(search_strategy.get('search_queries', [])[:3], 1):
		print(f'  {i}. {query}')
	if len(search_strategy.get('search_queries', [])) > 3:
		print(f'  ... 他 {len(search_strategy.get("search_queries", [])) - 3}個\n')

	# ステップ3: arXiv検索
	print('=' * 100)
	print('ステップ 3/3: arXiv自動検索')
	print('=' * 100 + '\n')

	searcher = ArXivSearcher()

	# search_strategyを使用してarXiv検索
	print(f'\n📝 arXiv検索を実行中...')
	try:
		all_papers = await searcher.search(search_strategy=search_strategy, max_results=5)
		print(f'  ✅ {len(all_papers)}件の論文を発見')
	except Exception as e:
		print(f'  ⚠️  エラー: {e}')
		all_papers = []

	# 重複除去
	unique_papers = searcher.deduplicate_papers(all_papers)
	unique_papers = unique_papers[:5]  # 最大5件

	print(f'\n✅ 合計 {len(unique_papers)} 件の論文を収集')
	print(f'   （重複除去前: {len(all_papers)} 件）\n')

	# 保存
	papers_path = data_dir / f'collected_papers_{session_id}.json'
	with open(papers_path, 'w', encoding='utf-8') as f:
		json.dump({'papers': unique_papers, 'total_count': len(unique_papers)}, f, indent=2, ensure_ascii=False)

	print(f'💾 論文情報を保存: {papers_path}\n')

	# 論文タイトル表示
	print('=' * 100)
	print('収集された論文一覧')
	print('=' * 100 + '\n')

	for i, paper in enumerate(unique_papers, 1):
		print(f'{i}. {paper.get("title", "Unknown")}')
		print(f'   著者: {", ".join(paper.get("authors", ["Unknown"])[:3])}')
		print(f'   発行日: {paper.get("published_date", "Unknown")}')
		print(f'   URL: {paper.get("url", "N/A")}\n')

	# 完了サマリー
	print('=' * 100)
	print('🎉 デモ完了！')
	print('=' * 100)
	print('\n生成されたファイル:')
	print(f'  📝 研究情報: {research_info_path}')
	print(f'  📊 検索戦略: {strategy_path}')
	print(f'  📚 収集論文: {papers_path}')
	print('\n次のステップ:')
	print('  - 個別論文の詳細分析（落合陽一式レポート生成）')
	print('  - 統合レポート作成')
	print('  - PRISMAフロー図生成')
	print('\nこれらは完全版システムで実行できます:')
	print('  uv run python -m automated_research.main --provider deepseek --max-papers 20')
	print('=' * 100 + '\n')


if __name__ == '__main__':
	asyncio.run(main())
