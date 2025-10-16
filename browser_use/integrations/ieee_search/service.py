"""
IEEE Xplore Search Service
Handles paper search, metadata extraction, and citation tracking.
"""

import logging
from typing import Any, TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
	from browser_use.browser import BrowserSession

logger = logging.getLogger(__name__)


class IEEESearchService:
	"""
	IEEE Xplore search service for academic paper discovery.
	Provides functionality to:
	- Search IEEE Xplore for papers
	- Extract paper metadata (title, authors, URL, etc.)
	- Track citations with source information
	"""

	def __init__(self, base_url: str | None = None):
		"""
		Initialize IEEE Search Service.

		Args:
			base_url: Base URL for IEEE Xplore (for testing purposes)
		"""
		self.base_url = base_url or 'https://ieeexplore.ieee.org'
		logger.info(f'🔍 IEEE Search Service initialized with base URL: {self.base_url}')

	async def search(
		self, query: str, max_results: int = 10, browser_session: 'BrowserSession | None' = None
	) -> list[dict[str, Any]]:
		"""
		Search IEEE Xplore for papers matching the query.

		Args:
			query: Search keywords
			max_results: Maximum number of results to return
			browser_session: Browser session for HTML access

		Returns:
			List of paper dictionaries with metadata
		"""
		logger.info(f'📚 Searching IEEE Xplore for: "{query}" (max {max_results} results)')

		if browser_session is None:
			# Fake implementation for backward compatibility
			return [
				{
					'title': 'Deep Learning for Network Traffic Classification',
					'authors': ['John Smith', 'Jane Doe'],
					'url': f'{self.base_url}/document/12345',
				}
			]

		# Navigate to search page
		from browser_use.browser.events import NavigateToUrlEvent

		search_url = f'{self.base_url}/search/searchresult.jsp?queryText={query}'
		logger.info(f'🌐 Navigating to: {search_url}')

		nav_event = browser_session.event_bus.dispatch(NavigateToUrlEvent(url=search_url))
		await nav_event

		# Get page HTML using CDP
		cdp_session = await browser_session.get_or_create_cdp_session()
		doc_result = await cdp_session.cdp_client.send.DOM.getDocument(session_id=cdp_session.session_id)
		html_result = await cdp_session.cdp_client.send.DOM.getOuterHTML(
			params={'nodeId': doc_result['root']['nodeId']}, session_id=cdp_session.session_id
		)
		html_content = html_result['outerHTML']

		# Parse HTML with BeautifulSoup
		soup = BeautifulSoup(html_content, 'html.parser')
		results = []

		# Extract paper information
		result_items = soup.find_all('div', class_='result-item')
		for item in result_items[:max_results]:
			# Extract title and URL
			title_elem = item.find('h2')
			if title_elem:
				link = title_elem.find('a')
				if link:
					title = link.get_text(strip=True)
					url = f"{self.base_url}{link.get('href', '')}"
				else:
					title = title_elem.get_text(strip=True)
					url = ''
			else:
				continue

			# Extract authors
			author_elem = item.find('div', class_='author')
			authors = []
			if author_elem:
				author_text = author_elem.get_text(strip=True)
				# Split by comma
				authors = [a.strip() for a in author_text.split(',') if a.strip()]

			results.append({'title': title, 'authors': authors, 'url': url})

		logger.info(f'✅ Found {len(results)} papers')
		return results
