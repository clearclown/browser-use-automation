"""
J-STAGE search module
Japan Science and Technology Information Aggregator, Electronic
https://www.jstage.jst.go.jp/
"""

import asyncio
import logging
import re
from typing import Any
from urllib.parse import quote

import aiohttp

logger = logging.getLogger(__name__)


class JStageSearcher:
	"""Search J-STAGE for Japanese academic papers"""

	def __init__(self):
		self.base_url = 'https://www.jstage.jst.go.jp'
		self.search_api_url = f'{self.base_url}/api/search'

	def build_jstage_query(self, search_string: str) -> dict[str, str]:
		"""
		Build J-STAGE API query parameters

		Args:
			search_string: Search query string

		Returns:
			Dict of query parameters for J-STAGE API
		"""
		# J-STAGE API uses 'text' parameter for general search
		# Convert Boolean operators to J-STAGE format
		query = search_string.replace(' AND ', ' ').replace(' OR ', ' | ')

		return {
			'text': query,
			'service': '1',  # Search articles
		}

	async def search(self, search_strategy: dict[str, Any], max_results: int = 20) -> list[dict[str, Any]]:
		"""
		Search J-STAGE using the search strategy

		Args:
			search_strategy: PRISMA search strategy
			max_results: Maximum results to return

		Returns:
			List of paper dictionaries
		"""
		all_papers = []
		search_queries = search_strategy.get('search_queries', [])
		year_range = search_strategy.get('year_range', {})
		year_start = year_range.get('start')
		year_end = year_range.get('end')

		if not search_queries:
			logger.warning('No search queries found in strategy')
			return all_papers

		results_per_query = max(1, max_results // len(search_queries))

		async with aiohttp.ClientSession() as session:
			for query_idx, query in enumerate(search_queries, 1):
				logger.info(f'Searching J-STAGE with query {query_idx}/{len(search_queries)}: {query}')

				query_params = self.build_jstage_query(query)
				papers = await self._fetch_jstage_results(session, query_params, results_per_query)

				if papers:
					logger.info(f'Found {len(papers)} papers for query: {query}')
					all_papers.extend(papers)

				# Rate limiting
				await asyncio.sleep(1)

		# Deduplicate and filter
		unique_papers = self.deduplicate_papers(all_papers)

		if year_start or year_end:
			unique_papers = self._filter_by_year(unique_papers, year_start, year_end)

		logger.info(f'Total unique papers from J-STAGE: {len(unique_papers)} (before: {len(all_papers)})')

		return unique_papers[:max_results]

	async def _fetch_jstage_results(
		self, session: aiohttp.ClientSession, query_params: dict[str, str], max_results: int
	) -> list[dict[str, Any]]:
		"""
		Fetch results from J-STAGE

		Note: J-STAGE doesn't have a public REST API, so we simulate fetching
		In a real implementation, this would use browser automation or scraping
		"""
		# For now, return empty list as J-STAGE requires browser automation
		# This would be implemented using browser-use in production
		logger.info('J-STAGE search requires browser automation (not implemented in unit tests)')
		return []

	def parse_article(self, article: dict[str, Any]) -> dict[str, Any]:
		"""
		Parse a J-STAGE article entry into standardized format

		Args:
			article: Article data from J-STAGE

		Returns:
			Standardized paper dict
		"""
		# Extract authors
		authors = []
		author_data = article.get('authors', [])
		if isinstance(author_data, list):
			for author in author_data:
				if isinstance(author, dict):
					name = author.get('name', '')
					if name:
						authors.append(name)
				elif isinstance(author, str):
					authors.append(author)

		# Extract year
		year = article.get('year')
		if not year and article.get('published_date'):
			year = self._extract_year(article['published_date'])

		# Build URL
		url = article.get('url', '')
		if not url and article.get('doi'):
			url = self.build_article_url(doi=article['doi'])

		return {
			'title': article.get('title', ''),
			'authors': authors,
			'abstract': article.get('abstract', ''),
			'journal': article.get('journal', ''),
			'year': year,
			'volume': article.get('volume', ''),
			'issue': article.get('issue', ''),
			'pages': article.get('pages', ''),
			'doi': article.get('doi', ''),
			'url': url,
			'source': 'J-STAGE',
		}

	def build_article_url(
		self,
		doi: str | None = None,
		journal: str | None = None,
		volume: str | None = None,
		issue: str | None = None,
		page: str | None = None,
	) -> str:
		"""
		Build J-STAGE article URL

		Args:
			doi: DOI of the article
			journal: Journal code
			volume: Volume number
			issue: Issue number
			page: Starting page

		Returns:
			URL to the article
		"""
		if doi:
			# J-STAGE DOI-based URL
			# DOIs typically look like: 10.2197/ipsjdc.2023.0001
			# Extract journal code from DOI if possible
			match = re.search(r'10\.\d+/([^/]+)/', doi)
			if match:
				journal_code = match.group(1)
				return f'{self.base_url}/article/{journal_code}/{doi.split("/")[-1]}'
			return f'{self.base_url}/article/{doi}'

		if journal and volume:
			# Build URL from components
			url = f'{self.base_url}/article/{journal}/{volume}'
			if issue:
				url += f'/{issue}'
			if page:
				url += f'/{page}'
			return url

		return self.base_url

	def contains_japanese(self, text: str) -> bool:
		"""
		Check if text contains Japanese characters

		Args:
			text: Text to check

		Returns:
			True if contains hiragana, katakana, or kanji
		"""
		# Hiragana: \u3040-\u309F
		# Katakana: \u30A0-\u30FF
		# Kanji: \u4E00-\u9FFF
		japanese_pattern = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
		return bool(re.search(japanese_pattern, text))

	def deduplicate_papers(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""
		Remove duplicate papers based on DOI or URL

		Args:
			papers: List of papers

		Returns:
			Deduplicated list
		"""
		seen_identifiers = set()
		unique_papers = []

		for paper in papers:
			# Try DOI first
			doi = paper.get('doi', '')
			if doi:
				if doi in seen_identifiers:
					continue
				seen_identifiers.add(doi)
				unique_papers.append(paper)
				continue

			# Try URL
			url = paper.get('url', '')
			if url:
				if url in seen_identifiers:
					continue
				seen_identifiers.add(url)
				unique_papers.append(paper)
				continue

			# Try title as last resort
			title = paper.get('title', '').lower().strip()
			if title:
				if title in seen_identifiers:
					continue
				seen_identifiers.add(title)
				unique_papers.append(paper)

		return unique_papers

	def _filter_by_year(
		self, papers: list[dict[str, Any]], year_start: int | None = None, year_end: int | None = None
	) -> list[dict[str, Any]]:
		"""Filter papers by publication year"""
		if not year_start and not year_end:
			return papers

		filtered = []
		for paper in papers:
			year = paper.get('year')
			if year is None:
				continue

			if year_start and year < year_start:
				continue
			if year_end and year > year_end:
				continue

			filtered.append(paper)

		return filtered

	def _extract_year(self, date_string: str) -> int | None:
		"""Extract year from date string"""
		match = re.search(r'(\d{4})', date_string)
		if match:
			return int(match.group(1))
		return None
