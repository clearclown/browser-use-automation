"""
Automated IEEE search with browser-use and PDF extraction
browser-useを使ったIEEE自動検索とPDF取得
"""

import asyncio
import json
import logging
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)


class IEEEAutomatedSearcher:
	"""IEEE Xploreでの自動検索とPDF取得"""

	def __init__(self, llm: ChatOpenAI | None = None, headless: bool = False):
		self.llm = llm or ChatOpenAI(model='gpt-4o', temperature=0.0)
		self.headless = headless

	async def search_and_collect(
		self, search_strategy: dict[str, Any], research_info: dict[str, Any], max_papers: int = 20
	) -> list[dict[str, Any]]:
		"""
		検索戦略に基づいてIEEE Xploreを検索し、論文情報を収集

		Args:
			search_strategy: PRISMA方式の検索戦略
			research_info: 研究情報
			max_papers: 収集する最大論文数

		Returns:
			論文情報のリスト
		"""
		print('\n' + '=' * 80)
		print('🔍 IEEE Xplore自動検索を開始します')
		print('=' * 80 + '\n')

		all_papers = []
		search_queries = search_strategy.get('search_queries', [])

		if not search_queries:
			logger.warning('No search queries found in strategy')
			return all_papers

		# ブラウザセッションを作成
		profile = BrowserProfile(
			headless=self.headless,
			disable_security=False,
			extra_chromium_args=[
				'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
			],
		)
		browser_session = BrowserSession(browser_profile=profile)

		try:
			# 各検索クエリで検索を実行
			for query_idx, query in enumerate(search_queries, 1):
				print(f'\n📝 検索 {query_idx}/{len(search_queries)}: {query}')

				# 検索タスクを作成
				papers_per_query = max(5, max_papers // len(search_queries))
				search_task = self._build_search_task(query, papers_per_query, search_strategy)

				# Agentを使って検索
				agent = Agent(
					task=search_task,
					llm=self.llm,
					browser_session=browser_session,
					max_actions_per_step=15,
				)

				try:
					history = await agent.run(max_steps=30)

					# 結果を抽出
					papers = self._extract_papers_from_history(history, query)

					if papers:
						print(f'  ✅ {len(papers)}件の論文を発見')
						all_papers.extend(papers)
					else:
						print('  ⚠️  論文が見つかりませんでした')

				except Exception as e:
					logger.error(f'Error during search for query "{query}": {e}')
					continue

				# 上限に達したら終了
				if len(all_papers) >= max_papers:
					print(f'\n🎯 目標論文数 {max_papers} に到達しました')
					break

				# レート制限を避けるため少し待機
				await asyncio.sleep(2)

		finally:
			await browser_session.kill()

		# 重複を除去
		unique_papers = self._deduplicate_papers(all_papers)

		print(f'\n✅ 合計 {len(unique_papers)} 件の論文を収集しました')
		print(f'   （重複除去前: {len(all_papers)} 件）')

		return unique_papers[:max_papers]

	def _build_search_task(self, query: str, max_results: int, search_strategy: dict[str, Any]) -> str:
		"""Agentに渡す検索タスクを構築"""
		year_range = search_strategy.get('year_range', {})
		start_year = year_range.get('start', 2018)
		end_year = year_range.get('end', 2024)

		task = f"""
IEEE Xploreで以下の検索を実行し、論文情報を収集してください：

検索クエリ: "{query}"
出版年範囲: {start_year} - {end_year}
取得件数: 最大{max_results}件

手順:
1. IEEE Xplore (https://ieeexplore.ieee.org/) にアクセス
2. 検索ボックスに "{query}" を入力して検索
3. 出版年フィルタで {start_year}-{end_year} を設定
4. 検索結果から上位{max_results}件の論文について以下の情報を収集:
   - タイトル
   - 著者
   - 出版年
   - 出版物名（Journal/Conference名）
   - DOI
   - Abstract
   - 論文URL
   - PDFダウンロードリンク（可能であれば）

5. 収集した情報をJSON形式で以下のように出力:
{{
  "papers": [
    {{
      "title": "論文タイトル",
      "authors": ["著者1", "著者2"],
      "year": 2023,
      "publication": "Journal/Conference名",
      "doi": "10.1109/...",
      "abstract": "要約文",
      "url": "https://ieeexplore.ieee.org/document/...",
      "pdf_url": "PDF URL if available"
    }}
  ]
}}

注意:
- 各論文のページを個別に訪問して詳細情報を確認してください
- 情報が取得できない項目は "N/A" としてください
- PDFは直接ダウンロードせず、URLのみ記録してください
"""
		return task

	def _extract_papers_from_history(self, history: Any, query: str) -> list[dict[str, Any]]:
		"""Agent実行履歴から論文情報を抽出"""
		papers = []

		# historyから最終結果を取得
		if hasattr(history, 'final_result') and history.final_result:
			result_text = str(history.final_result())

			# JSON形式のデータを抽出
			try:
				# JSONブロックを探す
				json_match = re.search(r'\{[\s\S]*"papers"[\s\S]*\}', result_text)
				if json_match:
					data = json.loads(json_match.group(0))
					papers = data.get('papers', [])

					# 各論文に検索クエリ情報を追加
					for paper in papers:
						paper['search_query'] = query

			except json.JSONDecodeError as e:
				logger.warning(f'Failed to parse JSON from result: {e}')

		# historyの各ステップから情報を抽出する代替手段
		if not papers and hasattr(history, 'history'):
			for step in history.history:
				if hasattr(step, 'result') and step.result:
					for result in step.result:
						if hasattr(result, 'extracted_content'):
							content = result.extracted_content
							if content and 'title' in content.lower():
								# Try to extract paper info from content
								try:
									paper_data = self._parse_paper_info(content)
									if paper_data:
										paper_data['search_query'] = query
										papers.append(paper_data)
								except Exception as e:
									logger.debug(f'Failed to parse paper info: {e}')

		return papers

	def _parse_paper_info(self, content: str) -> dict[str, Any] | None:
		"""テキストから論文情報をパース（簡易版）"""
		# 簡易的なパース処理
		# 実際の実装では、より堅牢なパースが必要
		try:
			# JSON形式を探す
			json_match = re.search(r'\{[^}]+\}', content)
			if json_match:
				return json.loads(json_match.group(0))
		except (json.JSONDecodeError, AttributeError):
			pass

		return None

	def _deduplicate_papers(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""タイトルベースで論文の重複を除去"""
		seen_titles = set()
		unique_papers = []

		for paper in papers:
			title = paper.get('title', '').lower().strip()
			if title and title not in seen_titles:
				seen_titles.add(title)
				unique_papers.append(paper)

		return unique_papers

	def save_papers(self, papers: list[dict[str, Any]], output_path: Path) -> None:
		"""論文情報をJSONファイルに保存"""
		output_path.parent.mkdir(parents=True, exist_ok=True)

		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump({'papers': papers, 'total_count': len(papers)}, f, indent=2, ensure_ascii=False)

		logger.info(f'Papers saved to: {output_path}')


async def main():
	"""テスト実行用のメイン関数"""
	# 検索戦略を読み込み
	strategy_path = Path('automated_research/data/search_strategy.json')
	research_info_path = Path('automated_research/data/research_info.json')

	if not strategy_path.exists():
		print('⚠️  検索戦略ファイルが見つかりません。')
		print('先に prisma_search_strategy.py を実行してください。')
		return

	if not research_info_path.exists():
		print('⚠️  研究情報ファイルが見つかりません。')
		return

	with open(strategy_path, encoding='utf-8') as f:
		search_strategy = json.load(f)

	with open(research_info_path, encoding='utf-8') as f:
		research_info = json.load(f)

	# 検索を実行
	searcher = IEEEAutomatedSearcher(headless=False)
	papers = await searcher.search_and_collect(search_strategy, research_info, max_papers=10)

	# 保存
	output_path = Path('automated_research/data/collected_papers.json')
	searcher.save_papers(papers, output_path)

	print(f'\n💾 論文情報を保存しました: {output_path}')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
