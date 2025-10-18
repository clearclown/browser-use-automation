"""
arXiv search module using arXiv API
Implements automated search for academic papers on arXiv
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Any
from urllib.parse import quote

import aiohttp

logger = logging.getLogger(__name__)


class ArXivSearcher:
	"""Search arXiv for academic papers using the arXiv API"""

	def __init__(self):
		self.base_url = 'http://export.arxiv.org/api/query'

	def build_arxiv_query(self, search_string: str, year_start: int | None = None, year_end: int | None = None) -> str:
		"""
		Build arXiv API query string from search parameters

		Args:
			search_string: Search query (supports AND, OR, NOT operators)
			year_start: Start year for filtering
			year_end: End year for filtering

		Returns:
			Formatted query string for arXiv API
		"""
		# Convert Boolean operators to arXiv API format
		query = search_string.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' ANDNOT ')

		# Clean up multiple spaces
		query = ' '.join(query.split())

		# For arXiv, we search in all fields by default
		# Can be refined to specific fields like ti: (title), abs: (abstract), au: (author)
		return query

	async def search(self, search_strategy: dict[str, Any], max_results: int = 20) -> list[dict[str, Any]]:
		"""
		Search arXiv using the search strategy

		Args:
			search_strategy: PRISMA search strategy with queries
			max_results: Maximum number of results to return

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
				logger.info(f'Searching arXiv with query {query_idx}/{len(search_queries)}: {query}')

				arxiv_query = self.build_arxiv_query(query, year_start, year_end)
				papers = await self._fetch_arxiv_results(session, arxiv_query, results_per_query)

				if papers:
					logger.info(f'Found {len(papers)} papers for query: {query}')
					all_papers.extend(papers)

				# Rate limiting
				await asyncio.sleep(1)

		# Deduplicate and filter
		unique_papers = self.deduplicate_papers(all_papers)

		if year_start or year_end:
			unique_papers = self.filter_by_year(unique_papers, year_start, year_end)

		logger.info(f'Total unique papers from arXiv: {len(unique_papers)} (before: {len(all_papers)})')

		return unique_papers[:max_results]

	async def _fetch_arxiv_results(
		self, session: aiohttp.ClientSession, query: str, max_results: int
	) -> list[dict[str, Any]]:
		"""
		Fetch results from arXiv API

		Args:
			session: aiohttp session
			query: Search query
			max_results: Max results to fetch

		Returns:
			List of parsed papers
		"""
		params = {
			'search_query': f'all:{query}',
			'start': 0,
			'max_results': max_results,
			'sortBy': 'relevance',
			'sortOrder': 'descending',
		}

		try:
			url = f'{self.base_url}?{self._build_query_string(params)}'
			async with session.get(url) as response:
				if response.status == 200:
					content = await response.text()
					return self._parse_arxiv_xml(content)
				else:
					logger.error(f'arXiv API returned status {response.status}')
					return []
		except Exception as e:
			logger.error(f'Error fetching from arXiv: {e}')
			return []

	def _build_query_string(self, params: dict[str, Any]) -> str:
		"""Build URL query string from parameters"""
		return '&'.join(f'{k}={quote(str(v))}' for k, v in params.items())

	def _parse_arxiv_xml(self, xml_content: str) -> list[dict[str, Any]]:
		"""
		Parse arXiv API XML response

		Args:
			xml_content: XML response from arXiv API

		Returns:
			List of paper dictionaries
		"""
		import xml.etree.ElementTree as ET

		papers = []

		try:
			root = ET.fromstring(xml_content)

			# Define namespaces
			ns = {
				'atom': 'http://www.w3.org/2005/Atom',
				'arxiv': 'http://arxiv.org/schemas/atom',
			}

			for entry in root.findall('atom:entry', ns):
				try:
					paper = self._parse_xml_entry(entry, ns)
					if paper:
						papers.append(paper)
				except Exception as e:
					logger.debug(f'Error parsing entry: {e}')
					continue

		except ET.ParseError as e:
			logger.error(f'Error parsing arXiv XML: {e}')

		return papers

	def _parse_xml_entry(self, entry: Any, ns: dict[str, str]) -> dict[str, Any]:
		"""Parse a single XML entry into a paper dict"""
		# Extract ID
		id_elem = entry.find('atom:id', ns)
		arxiv_id = self.extract_arxiv_id(id_elem.text if id_elem is not None else '')

		# Extract title
		title_elem = entry.find('atom:title', ns)
		title = title_elem.text.strip() if title_elem is not None else 'Unknown'

		# Extract abstract
		summary_elem = entry.find('atom:summary', ns)
		abstract = summary_elem.text.strip() if summary_elem is not None else ''

		# Extract authors
		authors = []
		for author in entry.findall('atom:author', ns):
			name_elem = author.find('atom:name', ns)
			if name_elem is not None:
				authors.append(name_elem.text.strip())

		# Extract published date
		published_elem = entry.find('atom:published', ns)
		published_date = published_elem.text if published_elem is not None else None
		year = self._extract_year_from_date(published_date) if published_date else None

		# Extract categories
		categories = []
		primary_category = entry.find('arxiv:primary_category', ns)
		if primary_category is not None:
			categories.append(primary_category.get('term', ''))

		for category in entry.findall('atom:category', ns):
			term = category.get('term', '')
			if term and term not in categories:
				categories.append(term)

		# Build URLs
		url = f'https://arxiv.org/abs/{arxiv_id}'
		pdf_url = self.build_pdf_url(arxiv_id)

		return {
			'title': title,
			'authors': authors,
			'abstract': abstract,
			'arxiv_id': arxiv_id,
			'url': url,
			'pdf_url': pdf_url,
			'published_date': published_date,
			'year': year,
			'categories': categories,
			'source': 'arXiv',
		}

	def parse_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
		"""
		Parse a dictionary-format arXiv entry (for testing)

		Args:
			entry: Entry dict from arXiv API

		Returns:
			Standardized paper dict
		"""
		arxiv_id = self.extract_arxiv_id(entry.get('id', ''))

		authors = []
		for author in entry.get('authors', []):
			if isinstance(author, dict):
				authors.append(author.get('name', ''))
			else:
				authors.append(str(author))

		published_date = entry.get('published', '')
		year = self._extract_year_from_date(published_date)

		categories = []
		if 'primary_category' in entry:
			categories.append(entry['primary_category'].get('term', ''))
		for cat in entry.get('categories', []):
			term = cat.get('term', '')
			if term and term not in categories:
				categories.append(term)

		return {
			'title': entry.get('title', ''),
			'authors': authors,
			'abstract': entry.get('summary', ''),
			'arxiv_id': arxiv_id,
			'url': f'https://arxiv.org/abs/{arxiv_id}',
			'pdf_url': self.build_pdf_url(arxiv_id),
			'published_date': published_date,
			'year': year,
			'categories': categories,
			'source': 'arXiv',
		}

	def extract_arxiv_id(self, id_string: str) -> str:
		"""
		Extract clean arXiv ID from various formats

		Args:
			id_string: arXiv ID or URL

		Returns:
			Clean arXiv ID (e.g., '2301.12345')
		"""
		# Match arXiv ID pattern: YYMM.NNNNN or YYMM.NNNNNvX
		match = re.search(r'(\d{4}\.\d{4,5})', id_string)
		if match:
			return match.group(1)
		return id_string

	def build_pdf_url(self, arxiv_id: str) -> str:
		"""Build PDF URL from arXiv ID"""
		return f'https://arxiv.org/pdf/{arxiv_id}.pdf'

	def _extract_year_from_date(self, date_string: str | None) -> int | None:
		"""Extract year from ISO date string"""
		if not date_string:
			return None

		try:
			# Try parsing ISO format
			dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
			return dt.year
		except (ValueError, AttributeError):
			# Try extracting year directly
			match = re.search(r'(\d{4})', date_string)
			if match:
				return int(match.group(1))
			return None

	def deduplicate_papers(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""Remove duplicate papers based on arXiv ID"""
		seen_ids = set()
		unique_papers = []

		for paper in papers:
			arxiv_id = paper.get('arxiv_id', '')
			if arxiv_id and arxiv_id not in seen_ids:
				seen_ids.add(arxiv_id)
				unique_papers.append(paper)

		return unique_papers

	def filter_by_year(
		self, papers: list[dict[str, Any]], year_start: int | None = None, year_end: int | None = None
	) -> list[dict[str, Any]]:
		"""Filter papers by publication year range"""
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
