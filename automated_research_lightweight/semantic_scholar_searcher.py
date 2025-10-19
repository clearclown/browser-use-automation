"""
Semantic Scholar API Searcher

公式APIを使用した軽量実装（認証不要）
リソース: 5-10MB, <1% CPU

API Docs: https://api.semanticscholar.org/api-docs/
"""

import asyncio
from typing import Any

import httpx


class SemanticScholarSearcher:
	"""Semantic Scholar公式API検索エンジン"""

	def __init__(self, timeout: int = 30):
		"""
		Args:
			timeout: HTTP接続タイムアウト（秒）
		"""
		self.timeout = timeout
		self.base_url = 'https://api.semanticscholar.org/graph/v1'

		# APIヘッダー（API Keyは不要だが、レート制限に注意）
		self.headers = {
			'Accept': 'application/json',
		}

	async def search_papers(
		self,
		query: str,
		year_start: int | None = None,
		year_end: int | None = None,
		max_results: int = 10,
	) -> list[dict[str, Any]]:
		"""
		Semantic Scholar APIで論文を検索

		Args:
			query: 検索クエリ
			year_start: 開始年（オプション）
			year_end: 終了年（オプション）
			max_results: 最大取得件数

		Returns:
			論文情報のリスト
		"""
		papers = []

		async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
			# 検索パラメータ
			params = {
				'query': query,
				'limit': max_results,
				'fields': 'paperId,title,authors,year,abstract,url,openAccessPdf,citationCount,influentialCitationCount',
			}

			# 年フィルタ（Semantic Scholarはyearパラメータでフィルタリング可能）
			if year_start and year_end:
				params['year'] = f'{year_start}-{year_end}'
			elif year_start:
				params['year'] = f'{year_start}-'
			elif year_end:
				params['year'] = f'-{year_end}'

			try:
				# API呼び出し
				response = await client.get(f'{self.base_url}/paper/search', params=params)
				response.raise_for_status()

				data = response.json()

				# 論文データをパース
				for paper_data in data.get('data', []):
					paper = self._parse_paper(paper_data)
					if paper:
						papers.append(paper)

			except httpx.HTTPStatusError as e:
				print(f'❌ Semantic Scholar HTTPエラー: {e.response.status_code}')
			except httpx.RequestError as e:
				print(f'❌ Semantic Scholar リクエストエラー: {e}')
			except Exception as e:
				print(f'❌ Semantic Scholar 予期しないエラー: {e}')

		return papers

	def _parse_paper(self, paper_data: dict[str, Any]) -> dict[str, Any] | None:
		"""
		論文データをパース

		Args:
			paper_data: APIレスポンスの論文データ

		Returns:
			論文情報辞書
		"""
		try:
			# 著者リスト
			authors = [author.get('name', 'Unknown') for author in paper_data.get('authors', [])]

			# PDF URL（オープンアクセスの場合）
			pdf_url = None
			if paper_data.get('openAccessPdf'):
				pdf_url = paper_data['openAccessPdf'].get('url')

			# Semantic Scholar URL
			paper_id = paper_data.get('paperId', '')
			semantic_url = f'https://www.semanticscholar.org/paper/{paper_id}' if paper_id else None

			return {
				'title': paper_data.get('title', 'Unknown Title'),
				'authors': authors,
				'published_date': str(paper_data.get('year', 'N/A')),
				'url': semantic_url or paper_data.get('url', 'N/A'),
				'pdf_url': pdf_url,
				'abstract': paper_data.get('abstract', 'アブストラクトなし'),
				'source': 'Semantic Scholar API',
				'citation_count': paper_data.get('citationCount', 0),
				'influential_citation_count': paper_data.get('influentialCitationCount', 0),
			}

		except Exception as e:
			print(f'⚠️ 論文パースエラー: {e}')
			return None


# テスト実行用
async def _test():
	"""動作確認テスト"""
	searcher = SemanticScholarSearcher()

	print('🔍 Semantic Scholar API検索テスト')
	print('検索クエリ: "deep learning"')
	print('')

	papers = await searcher.search_papers(query='deep learning', year_start=2023, year_end=2025, max_results=3)

	print(f'✅ {len(papers)}件の論文を取得\n')

	for idx, paper in enumerate(papers, 1):
		print(f'{idx}. {paper["title"]}')
		print(f'   著者: {", ".join(paper["authors"][:3])}')
		print(f'   発行日: {paper["published_date"]}')
		print(f'   URL: {paper["url"]}')
		print(f'   引用数: {paper["citation_count"]} (影響力: {paper["influential_citation_count"]})')
		if paper.get('pdf_url'):
			print(f'   PDF: {paper["pdf_url"]}')
		print('')


if __name__ == '__main__':
	asyncio.run(_test())
