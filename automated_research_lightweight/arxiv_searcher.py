"""
arXiv API Searcher

公式APIを使用した軽量実装（認証不要）
リソース: 5-10MB, <1% CPU
"""

import asyncio
from typing import Any

try:
	import arxiv
except ImportError:
	print('❌ arxiv パッケージがインストールされていません: uv pip install arxiv')
	arxiv = None


class ArxivSearcher:
	"""arXiv公式API検索エンジン"""

	def __init__(self, max_results: int = 10):
		"""
		Args:
			max_results: 最大取得件数（デフォルト: 10）
		"""
		if arxiv is None:
			raise ImportError('arxiv パッケージが必要です: uv pip install arxiv')

		self.max_results = max_results

	async def search_papers(
		self,
		query: str,
		year_start: int | None = None,
		year_end: int | None = None,
		max_results: int | None = None,
	) -> list[dict[str, Any]]:
		"""
		arXiv APIで論文を検索

		Args:
			query: 検索クエリ
			year_start: 開始年（オプション）
			year_end: 終了年（オプション）
			max_results: 最大取得件数（Noneの場合はデフォルト値を使用）

		Returns:
			論文情報のリスト
		"""
		papers = []
		max_count = max_results if max_results is not None else self.max_results

		# arxiv.Search APIは同期なので、asyncio.to_threadで非同期化
		search = arxiv.Search(query=query, max_results=max_count, sort_by=arxiv.SortCriterion.SubmittedDate)

		try:
			# 非同期実行
			results = await asyncio.to_thread(lambda: list(search.results()))

			for paper in results:
				# 年フィルタ（オプション）
				if year_start or year_end:
					paper_year = paper.published.year
					if year_start and paper_year < year_start:
						continue
					if year_end and paper_year > year_end:
						continue

				papers.append(
					{
						'title': paper.title,
						'authors': [author.name for author in paper.authors],
						'published_date': paper.published.strftime('%Y-%m-%d'),
						'url': paper.entry_id,
						'pdf_url': paper.pdf_url,
						'abstract': paper.summary,
						'source': 'arXiv API',
						'categories': paper.categories,
					}
				)

		except Exception as e:
			print(f'❌ arXiv API エラー: {e}')

		return papers


# テスト実行用
async def _test():
	"""動作確認テスト"""
	searcher = ArxivSearcher()

	print('🔍 arXiv API検索テスト')
	print('検索クエリ: "deep learning"')
	print('')

	papers = await searcher.search_papers(query='deep learning', year_start=2023, year_end=2025, max_results=3)

	print(f'✅ {len(papers)}件の論文を取得\n')

	for idx, paper in enumerate(papers, 1):
		print(f'{idx}. {paper["title"]}')
		print(f'   著者: {", ".join(paper["authors"][:3])}')
		print(f'   発行日: {paper["published_date"]}')
		print(f'   URL: {paper["url"]}')
		print(f'   PDF: {paper["pdf_url"]}')
		print('')


if __name__ == '__main__':
	asyncio.run(_test())
