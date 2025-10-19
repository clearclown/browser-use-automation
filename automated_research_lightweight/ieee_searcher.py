"""
IEEE Xplore Lightweight Searcher

httpx + BeautifulSoupによる軽量スクレイピング実装
ブラウザ不使用で400-600MBのリソース削減
"""

import asyncio
import re
from typing import Any
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup


class IEEELightweightSearcher:
	"""IEEE Xplore軽量検索エンジン（ブラウザ不使用）"""

	def __init__(self, timeout: int = 30):
		"""
		Args:
			timeout: HTTP接続タイムアウト（秒）
		"""
		self.timeout = timeout
		self.base_url = 'https://ieeexplore.ieee.org'

		# ブラウザに見せかけるヘッダー
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
		}

	async def search_papers(
		self,
		query: str,
		year_start: int | None = None,
		year_end: int | None = None,
		max_results: int = 10,
	) -> list[dict[str, Any]]:
		"""
		IEEE Xploreで論文を検索

		Args:
			query: 検索クエリ
			year_start: 開始年（オプション）
			year_end: 終了年（オプション）
			max_results: 最大取得件数

		Returns:
			論文情報のリスト
		"""
		papers = []

		async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout, follow_redirects=True) as client:
			# 検索URLを構築
			search_params = {'queryText': query, 'highlight': 'true', 'returnFacets': 'ALL', 'returnType': 'SEARCH'}

			if year_start and year_end:
				search_params['ranges'] = f'{year_start}_{year_end}_Year'

			search_url = f'{self.base_url}/search/searchresult.jsp?{urlencode(search_params)}'

			try:
				# 検索ページを取得
				response = await client.get(search_url)
				response.raise_for_status()

				# HTMLをパース
				soup = BeautifulSoup(response.text, 'html.parser')

				# 論文エントリを抽出
				paper_entries = soup.find_all('div', class_='List-results-items')

				for entry in paper_entries[:max_results]:
					paper = await self._parse_paper_entry(entry, client)
					if paper:
						papers.append(paper)

			except httpx.HTTPStatusError as e:
				print(f'❌ IEEE Xplore HTTPエラー: {e.response.status_code}')
			except httpx.RequestError as e:
				print(f'❌ IEEE Xplore リクエストエラー: {e}')
			except Exception as e:
				print(f'❌ IEEE Xplore 予期しないエラー: {e}')

		return papers

	async def _parse_paper_entry(self, entry: Any, client: httpx.AsyncClient) -> dict[str, Any] | None:
		"""
		論文エントリをパースして情報を抽出

		Args:
			entry: BeautifulSoup論文エントリ
			client: httpxクライアント

		Returns:
			論文情報辞書
		"""
		try:
			# タイトル
			title_tag = entry.find('h2')
			title = title_tag.get_text(strip=True) if title_tag else 'Unknown Title'

			# 論文URL
			link_tag = title_tag.find('a') if title_tag else None
			paper_url = f"{self.base_url}{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else None

			# 著者
			authors_tags = entry.find_all('span', class_='author')
			authors = [author.get_text(strip=True) for author in authors_tags]

			# 発行日
			date_tag = entry.find('div', class_='description')
			published_date = None
			if date_tag:
				date_text = date_tag.get_text(strip=True)
				# "Published in: ... Date of Publication: 01 January 2023"のようなパターンを抽出
				date_match = re.search(r'Date of Publication:\s*(.+)', date_text)
				if date_match:
					published_date = date_match.group(1).strip()

			# アブストラクト（詳細ページから取得）
			abstract = None
			if paper_url:
				abstract = await self._fetch_abstract(paper_url, client)

			return {
				'title': title,
				'authors': authors,
				'published_date': published_date or 'N/A',
				'url': paper_url or 'N/A',
				'abstract': abstract or 'アブストラクト取得失敗',
				'source': 'IEEE Xplore (Lightweight)',
			}

		except Exception as e:
			print(f'⚠️ 論文パースエラー: {e}')
			return None

	async def _fetch_abstract(self, paper_url: str, client: httpx.AsyncClient) -> str | None:
		"""
		論文詳細ページからアブストラクトを取得

		Args:
			paper_url: 論文URL
			client: httpxクライアント

		Returns:
			アブストラクトテキスト
		"""
		try:
			# 詳細ページを取得
			response = await client.get(paper_url)
			response.raise_for_status()

			soup = BeautifulSoup(response.text, 'html.parser')

			# アブストラクトを抽出（複数パターン対応）
			abstract_tag = soup.find('div', class_='abstract-text') or soup.find('div', class_='section', string=re.compile(r'Abstract'))

			if abstract_tag:
				return abstract_tag.get_text(strip=True)

			# JSONメタデータから抽出（別パターン）
			meta_tag = soup.find('meta', property='og:description')
			if meta_tag and 'content' in meta_tag.attrs:
				return meta_tag['content']

			return None

		except Exception as e:
			print(f'⚠️ アブストラクト取得エラー: {e}')
			return None


# テスト実行用
async def _test():
	"""動作確認テスト"""
	searcher = IEEELightweightSearcher()

	print('🔍 IEEE Xplore軽量検索テスト')
	print('検索クエリ: "deep learning"')
	print('')

	papers = await searcher.search_papers(query='deep learning', year_start=2022, year_end=2025, max_results=3)

	print(f'✅ {len(papers)}件の論文を取得\n')

	for idx, paper in enumerate(papers, 1):
		print(f'{idx}. {paper["title"]}')
		print(f'   著者: {", ".join(paper["authors"][:3])}')
		print(f'   発行日: {paper["published_date"]}')
		print(f'   URL: {paper["url"]}')
		print('')


if __name__ == '__main__':
	asyncio.run(_test())
