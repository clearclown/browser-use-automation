"""
IEEE Xplore Search Service
Handles paper search, metadata extraction, and citation tracking.
"""

import logging
import re
import tempfile
from pathlib import Path
from typing import Any, Callable, TYPE_CHECKING

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from browser_use.integrations.ieee_search.views import Citation

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
		self,
		query: str,
		max_results: int = 10,
		browser_session: 'BrowserSession | None' = None,
		progress_callback: Callable[[str, int, int], None] | None = None,
	) -> list[dict[str, Any]]:
		"""
		Search IEEE Xplore for papers matching the query.

		Args:
			query: Search keywords
			max_results: Maximum number of results to return
			browser_session: Browser session for HTML access
			progress_callback: Optional callback function(status: str, current: int, total: int)

		Returns:
			List of paper dictionaries with metadata
		"""
		logger.info(f'📚 Searching IEEE Xplore for: "{query}" (max {max_results} results)')

		# Report initial progress
		if progress_callback:
			progress_callback(f'Searching IEEE Xplore for "{query}"', 0, max_results)

		if browser_session is None:
			raise ValueError('browser_session is required for IEEE search')

		# Navigate to search page
		from browser_use.browser.events import NavigateToUrlEvent

		search_url = f'{self.base_url}/search/searchresult.jsp?queryText={query}'
		logger.info(f'🌐 Navigating to: {search_url}')

		nav_event = browser_session.event_bus.dispatch(NavigateToUrlEvent(url=search_url))
		await nav_event

		# Wait for JavaScript to load content (IEEE is a SPA)
		import asyncio
		await asyncio.sleep(5)

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

		# Extract paper information - IEEE uses custom elements like <xpl-results-item>
		# Each result is in a div with class "List-results-items"
		result_containers = soup.find_all('div', class_='List-results-items')

		for container in result_containers[:max_results]:
			# Find the title link - it's in <h3><a href="/document/ID/">
			title_elem = container.find('h3')
			if not title_elem:
				continue

			link = title_elem.find('a')
			if not link:
				continue

			# Get text with separator to preserve spaces
			title = link.get_text(separator=' ', strip=True)

			href = link.get('href', '')
			if href.startswith('/'):
				url = f'{self.base_url}{href}'
			else:
				url = href

			# Extract authors - they're in <xpl-authors-name-list> custom element
			authors = []
			author_list = container.find('xpl-authors-name-list')
			if author_list:
				# Find all author links within the author list
				author_links = author_list.find_all('a')
				for author_link in author_links:
					author_name = author_link.get_text(strip=True)
					if author_name and author_name != ';':
						authors.append(author_name)

			results.append({'title': title, 'authors': authors, 'url': url})

		logger.info(f'✅ Found {len(results)} papers')

		# Report completion
		if progress_callback:
			progress_callback(f'Found {len(results)} papers', len(results), max_results)

		return results

	async def extract_citations(
		self,
		paper_url: str,
		sections: list[str] | None = None,
		browser_session: 'BrowserSession | None' = None,
		use_pdf: bool = True,
	) -> list[Citation]:
		"""
		Extract citations/excerpts from a paper with source tracking.

		Args:
			paper_url: URL of the paper to extract from
			sections: List of section names to extract (e.g., ['Abstract', 'Introduction'])
			browser_session: Browser session for HTML access
			use_pdf: If True, download and extract from PDF for full text (default: True)

		Returns:
			List of Citation objects with text, section, and metadata
		"""
		if browser_session is None:
			raise ValueError('browser_session is required for citation extraction')

		logger.info(f'📄 Extracting citations from: {paper_url}')

		# Navigate to paper page
		from browser_use.browser.events import NavigateToUrlEvent

		nav_event = browser_session.event_bus.dispatch(NavigateToUrlEvent(url=paper_url))
		await nav_event

		# Wait for JavaScript to load content (IEEE is a SPA)
		import asyncio
		await asyncio.sleep(5)

		# Get page HTML using CDP
		cdp_session = await browser_session.get_or_create_cdp_session()
		doc_result = await cdp_session.cdp_client.send.DOM.getDocument(session_id=cdp_session.session_id)
		html_result = await cdp_session.cdp_client.send.DOM.getOuterHTML(
			params={'nodeId': doc_result['root']['nodeId']}, session_id=cdp_session.session_id
		)
		html_content = html_result['outerHTML']

		# Parse HTML with BeautifulSoup
		soup = BeautifulSoup(html_content, 'html.parser')
		citations = []

		# Extract paper metadata
		# Title might be in different locations - try various selectors
		title_elem = soup.find('h1', class_='document-title')
		if not title_elem:
			title_elem = soup.find('h1')
		paper_title = title_elem.get_text(separator=' ', strip=True) if title_elem else 'Unknown'

		# Authors on detail page are in <xpl-authors-name-list> custom element
		authors = []
		author_list = soup.find('xpl-authors-name-list')
		if author_list:
			author_links = author_list.find_all('a')
			for author_link in author_links:
				author_name = author_link.get_text(strip=True)
				if author_name and author_name not in [';', ',']:
					authors.append(author_name)
		elif soup.find('div', class_='authors'):
			# Fallback for older format
			authors_elem = soup.find('div', class_='authors')
			author_text = authors_elem.get_text(strip=True)
			authors = [a.strip() for a in author_text.split(',') if a.strip()]

		# Extract abstract - IEEE uses class="abstract-text" for desktop
		# and "abstract-mobile-div" for mobile
		abstract_container = soup.find('div', class_='abstract-text')
		if not abstract_container:
			# Try mobile version
			abstract_container = soup.find('div', class_='abstract-mobile-div')

		if abstract_container and (sections is None or 'Abstract' in sections):
			# Find the div with xplmathjax attribute (contains actual text)
			abstract_div = abstract_container.find('div', attrs={'xplmathjax': ''})
			if not abstract_div:
				# Try span for mobile
				abstract_div = abstract_container.find('span', attrs={'xplmathjax': ''})

			if abstract_div:
				abstract_text = abstract_div.get_text(separator=' ', strip=True)
				# Remove common suffixes like "<>" or trailing dots
				abstract_text = abstract_text.replace('<>', '').strip()

				if abstract_text and len(abstract_text) > 20:  # Minimum length check
					citations.append(
						Citation(
							text=abstract_text,
							paper_title=paper_title,
							paper_url=paper_url,
							section='Abstract',
							authors=authors,
						)
					)

		# Extract sections from main document
		main_doc = soup.find('div', class_='document-main')
		if main_doc:
			# Find all h2 headings (sections)
			for heading in main_doc.find_all('h2'):
				section_title = heading.get_text(strip=True)

				# Check if this section is requested
				if sections is not None:
					# Match section names (e.g., "I. Introduction" matches "Introduction")
					matched = False
					for requested in sections:
						if requested.lower() in section_title.lower():
							matched = True
							break
					if not matched:
						continue

				# Extract section content (paragraphs following the heading)
				section_text = []
				for sibling in heading.find_next_siblings():
					if sibling.name == 'h2':
						break
					if sibling.name == 'p':
						section_text.append(sibling.get_text(strip=True))

				if section_text:
					# Determine clean section name
					clean_section = section_title
					if 'Introduction' in section_title:
						clean_section = 'Introduction'
					elif 'Methodology' in section_title or 'Method' in section_title:
						clean_section = 'Methodology'
					elif 'Conclusion' in section_title:
						clean_section = 'Conclusion'
					elif 'Results' in section_title:
						clean_section = 'Results'

					citations.append(
						Citation(
							text=' '.join(section_text),
							paper_title=paper_title,
							paper_url=paper_url,
							section=clean_section,
							authors=authors,
						)
					)

		# Try PDF extraction if enabled and no sections found from HTML
		if use_pdf and len(citations) < 2:  # HTML usually only has abstract
			logger.info('📥 HTML extraction limited, trying PDF extraction...')

			# Find PDF link from the page
			# IEEE PDF links are like: /stamp/stamp.jsp?tp=&arnumber=XXXXX
			pdf_links = soup.find_all('a', href=re.compile(r'/stamp/stamp\.jsp'))
			if pdf_links:
				pdf_link = pdf_links[0].get('href')
				if not pdf_link.startswith('http'):
					pdf_url = f'{self.base_url}{pdf_link}'
				else:
					pdf_url = pdf_link

				logger.info(f'📄 Found PDF link: {pdf_url}')

				# Download and extract from PDF
				pdf_citations = await self.download_and_extract_pdf(
					pdf_url, paper_title, authors, sections, browser_session
				)

				# Merge PDF citations with HTML citations
				# Prefer PDF sections over HTML abstract if available
				if pdf_citations:
					# Remove abstract from HTML citations if we have PDF sections
					citations = [c for c in citations if c.section != 'Abstract' or not pdf_citations]
					citations.extend(pdf_citations)

		logger.info(f'✅ Extracted {len(citations)} citations from {len(sections or [])} sections')
		return citations

	async def download_and_extract_pdf(
		self,
		pdf_url: str,
		paper_title: str,
		authors: list[str],
		sections: list[str] | None = None,
		browser_session: 'BrowserSession | None' = None,
	) -> list[Citation]:
		"""
		Download PDF and extract text from specific sections.

		Args:
			pdf_url: URL of the PDF file
			paper_title: Title of the paper
			authors: List of author names
			sections: List of section names to extract (e.g., ['Introduction', 'Methodology'])
			browser_session: Browser session for downloading (uses browser cookies for authentication)

		Returns:
			List of Citation objects with text from PDF
		"""
		if not browser_session:
			logger.warning('⚠️ Browser session required for PDF download')
			return []

		logger.info(f'📥 Downloading PDF from: {pdf_url}')

		try:
			import asyncio
			from browser_use.browser.events import NavigateToUrlEvent, FileDownloadedEvent

			# Create a future to wait for download completion
			download_future: asyncio.Future[str] = asyncio.Future()

			def download_handler(event: FileDownloadedEvent):
				"""Handle file download event."""
				# Check if this is our PDF
				if event.url == pdf_url or pdf_url in event.url:
					logger.debug(f'📥 Received download event for: {event.file_name}')
					if not download_future.done():
						download_future.set_result(event.path)

			# Subscribe to download events
			browser_session.event_bus.on(FileDownloadedEvent, download_handler)

			try:
				# Navigate to PDF URL (this will trigger browser download)
				logger.debug(f'🌐 Navigating to PDF URL: {pdf_url}')
				nav_event = browser_session.event_bus.dispatch(NavigateToUrlEvent(url=pdf_url))
				await nav_event

				# Wait for download to complete (with timeout)
				try:
					pdf_path_str = await asyncio.wait_for(download_future, timeout=30.0)
					pdf_path = Path(pdf_path_str)
					logger.info(f'✅ PDF downloaded successfully: {pdf_path.name} ({pdf_path.stat().st_size} bytes)')
				except asyncio.TimeoutError:
					logger.warning('⚠️ PDF download timed out after 30 seconds')
					logger.info('💡 This paper may require IEEE subscription or institutional access')
					return []

			finally:
				# Unsubscribe from download events
				# Note: bubus does not have unsubscribe - event handlers persist
				pass

			# Extract text from downloaded PDF
			citations = self._extract_text_from_pdf(pdf_path, pdf_url, paper_title, authors, sections)

			# Clean up downloaded file
			if pdf_path.exists():
				pdf_path.unlink()
				logger.debug(f'🗑️ Cleaned up temporary PDF: {pdf_path.name}')

			return citations

		except Exception as e:
			logger.error(f'❌ Failed to download/parse PDF: {e}')
			logger.info('💡 Note: Some IEEE papers may require subscription or institutional access')
			return []

	def _extract_text_from_pdf(
		self, pdf_path: Path, paper_url: str, paper_title: str, authors: list[str], sections: list[str] | None
	) -> list[Citation]:
		"""
		Extract text from PDF file and split by sections.

		Args:
			pdf_path: Path to PDF file
			paper_url: URL of the paper
			paper_title: Title of the paper
			authors: List of author names
			sections: List of section names to extract

		Returns:
			List of Citation objects with extracted text
		"""
		logger.info(f'📄 Parsing PDF: {pdf_path}')

		try:
			reader = PdfReader(pdf_path)
			citations = []

			# Extract full text from all pages
			full_text = ''
			page_texts = []

			for i, page in enumerate(reader.pages, 1):
				page_text = page.extract_text()
				page_texts.append((i, page_text))
				full_text += f'\n{page_text}'

			logger.info(f'📊 Extracted text from {len(reader.pages)} pages')

			# Try to split text by sections
			# Common section headers in IEEE papers
			section_patterns = [
				r'^(I+\.?\s+)?INTRODUCTION\s*$',
				r'^(I+\.?\s+)?ABSTRACT\s*$',
				r'^(I+\.?\s+)?RELATED\s+WORK\s*$',
				r'^(I+\.?\s+)?METHODOLOGY\s*$',
				r'^(I+\.?\s+)?METHOD\s*$',
				r'^(I+\.?\s+)?EXPERIMENTS?\s*$',
				r'^(I+\.?\s+)?RESULTS?\s*$',
				r'^(I+\.?\s+)?DISCUSSION\s*$',
				r'^(I+\.?\s+)?CONCLUSION\s*$',
				r'^(I+\.?\s+)?REFERENCES?\s*$',
			]

			# Split text into lines and find section headers
			lines = full_text.split('\n')
			current_section = None
			section_content = {}

			for line in lines:
				line_upper = line.strip().upper()

				# Check if line matches any section pattern
				matched_section = None
				for pattern in section_patterns:
					if re.match(pattern, line_upper, re.IGNORECASE):
						# Extract clean section name
						if 'INTRODUCTION' in line_upper:
							matched_section = 'Introduction'
						elif 'ABSTRACT' in line_upper:
							matched_section = 'Abstract'
						elif 'RELATED' in line_upper:
							matched_section = 'Related Work'
						elif 'METHOD' in line_upper:
							matched_section = 'Methodology'
						elif 'EXPERIMENT' in line_upper:
							matched_section = 'Experiments'
						elif 'RESULT' in line_upper:
							matched_section = 'Results'
						elif 'DISCUSSION' in line_upper:
							matched_section = 'Discussion'
						elif 'CONCLUSION' in line_upper:
							matched_section = 'Conclusion'
						elif 'REFERENCE' in line_upper:
							matched_section = 'References'
						break

				if matched_section:
					current_section = matched_section
					if current_section not in section_content:
						section_content[current_section] = []
					logger.info(f'  📌 Found section: {current_section}')
				elif current_section and line.strip():
					# Add line to current section
					section_content[current_section].append(line)

			# Create citations from extracted sections
			for section_name, content_lines in section_content.items():
				# Check if this section is requested
				if sections is None or section_name in sections:
					section_text = ' '.join(content_lines).strip()

					# Skip if too short or if it's the references section
					if len(section_text) > 50 and section_name != 'References':
						citations.append(
							Citation(
								text=section_text,
								paper_title=paper_title,
								paper_url=paper_url,
								section=section_name,
								authors=authors,
							)
						)

			logger.info(f'✅ Extracted {len(citations)} sections from PDF')
			return citations

		except Exception as e:
			logger.error(f'❌ Failed to parse PDF: {e}', exc_info=True)
			return []
