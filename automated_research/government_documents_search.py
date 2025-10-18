"""
Government documents search module
Supports searching official government publications and policy documents
from multiple countries and international organizations
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class GovernmentDocumentsSearcher:
	"""Search government documents from multiple sources"""

	def __init__(self):
		self.sources = self._initialize_sources()

	def _initialize_sources(self) -> dict[str, dict[str, Any]]:
		"""Initialize available government document sources"""
		return {
			'usa_gov': {
				'id': 'usa_gov',
				'name': 'USA.gov',
				'country': 'USA',
				'url': 'https://www.usa.gov',
				'search_url': 'https://search.usa.gov/search',
				'description': 'Official US Government portal',
			},
			'japan_gov': {
				'id': 'japan_gov',
				'name': 'e-Gov (Japan)',
				'country': 'Japan',
				'url': 'https://www.e-gov.go.jp',
				'description': 'Japanese government portal',
			},
			'uk_gov': {
				'id': 'uk_gov',
				'name': 'GOV.UK',
				'country': 'UK',
				'url': 'https://www.gov.uk',
				'search_url': 'https://www.gov.uk/api/search.json',
				'description': 'UK Government official website',
			},
			'eu': {
				'id': 'eu',
				'name': 'EUR-Lex',
				'organization': 'European Union',
				'url': 'https://eur-lex.europa.eu',
				'description': 'EU law and publications',
			},
			'who': {
				'id': 'who',
				'name': 'World Health Organization',
				'organization': 'WHO',
				'url': 'https://www.who.int',
				'description': 'WHO publications and guidelines',
			},
			'un': {
				'id': 'un',
				'name': 'United Nations',
				'organization': 'UN',
				'url': 'https://www.un.org',
				'description': 'UN documents and resolutions',
			},
		}

	def get_available_sources(self) -> list[dict[str, Any]]:
		"""Get list of available government sources"""
		return list(self.sources.values())

	def get_supported_countries(self) -> list[str]:
		"""Get list of supported countries"""
		countries = []
		for source in self.sources.values():
			if 'country' in source:
				countries.append(source['country'])
			if 'organization' in source:
				countries.append(source['organization'])
		return list(set(countries))

	async def search_source(self, source_id: str, query: str, max_results: int = 10) -> list[dict[str, Any]]:
		"""
		Search a specific government source

		Args:
			source_id: ID of the source to search
			query: Search query
			max_results: Maximum number of results

		Returns:
			List of documents
		"""
		if source_id not in self.sources:
			logger.error(f'Unknown source: {source_id}')
			return []

		source = self.sources[source_id]
		logger.info(f'Searching {source["name"]} for: {query}')

		# In production, this would use browser automation or specific APIs
		# For now, return empty list in tests
		logger.info(f'Government document search requires specific API/browser automation (source: {source_id})')
		return []

	async def search_all_sources(
		self, search_strategy: dict[str, Any], max_results_per_source: int = 5
	) -> list[dict[str, Any]]:
		"""
		Search all available government sources

		Args:
			search_strategy: PRISMA search strategy
			max_results_per_source: Max results per source

		Returns:
			Combined list of documents
		"""
		all_documents = []
		search_queries = search_strategy.get('search_queries', [])

		if not search_queries:
			logger.warning('No search queries found')
			return all_documents

		# Use first query for government docs
		primary_query = search_queries[0]

		# Search each source
		for source_id in self.sources.keys():
			try:
				documents = await self.search_source(source_id, primary_query, max_results_per_source)
				if documents:
					all_documents.extend(documents)
			except Exception as e:
				logger.error(f'Error searching {source_id}: {e}')
				continue

		# Deduplicate
		unique_documents = self.deduplicate_documents(all_documents)

		# Filter by year if specified
		year_range = search_strategy.get('year_range', {})
		if year_range:
			unique_documents = self._filter_by_year(
				unique_documents, year_range.get('start'), year_range.get('end')
			)

		logger.info(f'Total government documents found: {len(unique_documents)}')
		return unique_documents

	def parse_document(self, document: dict[str, Any]) -> dict[str, Any]:
		"""
		Parse a government document into standardized format

		Args:
			document: Raw document data

		Returns:
			Standardized document dict
		"""
		# Extract year from published_date
		year = document.get('year')
		if not year:
			published_date = document.get('published_date', '')
			year = self._extract_year_from_date(published_date)

		# Detect document type if not provided
		document_type = document.get('document_type', '')
		if not document_type:
			document_type = self.detect_document_type(document.get('title', ''))

		# Build source string
		source_parts = []
		if document.get('agency'):
			source_parts.append(document['agency'])
		if document.get('country'):
			source_parts.append(document['country'])
		elif document.get('organization'):
			source_parts.append(document['organization'])

		if not source_parts:
			source_parts.append('Government Document')

		return {
			'title': document.get('title', ''),
			'url': document.get('url', ''),
			'published_date': document.get('published_date', ''),
			'year': year,
			'agency': document.get('agency', ''),
			'country': document.get('country', ''),
			'organization': document.get('organization', ''),
			'document_type': document_type,
			'abstract': document.get('abstract', ''),
			'source': ' - '.join(source_parts),
		}

	def detect_document_type(self, title: str) -> str:
		"""
		Detect government document type from title

		Args:
			title: Document title

		Returns:
			Document type
		"""
		title_lower = title.lower()

		type_patterns = [
			(r'executive order', 'Executive Order'),
			(r'presidential\s+(action|memorandum|directive)', 'Presidential Document'),
			(r'public\s+comment', 'Public Comment'),  # Before regulation to avoid false matches
			(r'(annual|quarterly|monthly)\s+report', 'Report'),
			(r'white paper', 'White Paper'),
			(r'policy\s+(brief|paper|statement)', 'Policy Paper'),
			(r'regulation', 'Regulation'),
			(r'bill|act\s+of', 'Legislation'),
			(r'hearing|testimony', 'Hearing'),
			(r'guidelines?', 'Guidelines'),
			(r'strategy|roadmap', 'Strategic Document'),
			(r'budget', 'Budget Document'),
		]

		for pattern, doc_type in type_patterns:
			if re.search(pattern, title_lower):
				return doc_type

		return 'Government Document'

	def filter_by_type(self, documents: list[dict[str, Any]], allowed_types: list[str]) -> list[dict[str, Any]]:
		"""
		Filter documents by document type

		Args:
			documents: List of documents
			allowed_types: List of allowed document types

		Returns:
			Filtered documents
		"""
		return [doc for doc in documents if doc.get('document_type') in allowed_types]

	def deduplicate_documents(self, documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""
		Remove duplicate documents based on URL

		Args:
			documents: List of documents

		Returns:
			Deduplicated list
		"""
		seen_urls = set()
		unique_documents = []

		for doc in documents:
			url = doc.get('url', '')
			if not url:
				# If no URL, check title
				title = doc.get('title', '').lower().strip()
				if title and title not in seen_urls:
					seen_urls.add(title)
					unique_documents.append(doc)
				continue

			if url not in seen_urls:
				seen_urls.add(url)
				unique_documents.append(doc)

		return unique_documents

	def extract_agency(self, url: str) -> str:
		"""
		Extract government agency from URL

		Args:
			url: URL of the document

		Returns:
			Agency name
		"""
		url_lower = url.lower()

		# USA agencies
		agency_patterns = {
			'whitehouse.gov': 'White House',
			'fda.gov': 'FDA',
			'cdc.gov': 'CDC',
			'nih.gov': 'NIH',
			'nsf.gov': 'NSF',
			'nasa.gov': 'NASA',
			'doe.gov': 'Department of Energy',
			'defense.gov': 'Department of Defense',
			'state.gov': 'Department of State',
			# Japan
			'mhlw.go.jp': 'MHLW',  # Ministry of Health, Labour and Welfare
			'mext.go.jp': 'MEXT',  # Ministry of Education
			'meti.go.jp': 'METI',  # Ministry of Economy
			# UK
			'gov.uk': 'UK Government',
			# EU
			'europa.eu': 'European Union',
			# WHO
			'who.int': 'WHO',
		}

		for pattern, agency in agency_patterns.items():
			if pattern in url_lower:
				return agency

		# Try to extract domain
		match = re.search(r'https?://(?:www\.)?([^/]+)', url)
		if match:
			domain = match.group(1)
			return domain.split('.')[0].upper()

		return 'Government Agency'

	def _filter_by_year(
		self, documents: list[dict[str, Any]], year_start: int | None = None, year_end: int | None = None
	) -> list[dict[str, Any]]:
		"""Filter documents by year range"""
		if not year_start and not year_end:
			return documents

		filtered = []
		for doc in documents:
			year = doc.get('year')
			if year is None:
				continue

			if year_start and year < year_start:
				continue
			if year_end and year > year_end:
				continue

			filtered.append(doc)

		return filtered

	def _extract_year_from_date(self, date_string: str) -> int | None:
		"""Extract year from date string"""
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
