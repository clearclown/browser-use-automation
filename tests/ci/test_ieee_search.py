"""
Tests for IEEE paper search integration.
Following t-wada style TDD approach.
"""

import pytest
from pytest_httpserver import HTTPServer

from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService


@pytest.fixture(scope='session')
def ieee_mock_server():
	"""Create mock IEEE Xplore server for testing."""
	server = HTTPServer()
	server.start()

	# Mock IEEE Xplore search results page
	search_results_html = """
	<!DOCTYPE html>
	<html>
	<head><title>IEEE Xplore Search Results</title></head>
	<body>
		<div class="List-results-items">
			<div class="result-item">
				<h2><a href="/document/12345">Deep Learning for Network Traffic Classification</a></h2>
				<div class="author">John Smith, Jane Doe</div>
				<div class="description">This paper presents a novel approach...</div>
			</div>
			<div class="result-item">
				<h2><a href="/document/67890">Machine Learning in Cybersecurity</a></h2>
				<div class="author">Alice Johnson</div>
				<div class="description">We propose a machine learning framework...</div>
			</div>
		</div>
	</body>
	</html>
	"""

	server.expect_request('/search/searchresult.jsp').respond_with_data(
		search_results_html,
		content_type='text/html',
	)

	# Mock paper detail page for citation extraction
	paper_detail_html = """
	<!DOCTYPE html>
	<html>
	<head><title>Deep Learning for Network Traffic Classification - IEEE Xplore</title></head>
	<body>
		<div class="document">
			<h1>Deep Learning for Network Traffic Classification</h1>
			<div class="authors">John Smith, Jane Doe</div>
			<div class="abstract-text">
				<h2>Abstract</h2>
				<p>This paper presents a novel approach to network traffic classification using deep learning.
				Our method achieves 95% accuracy on benchmark datasets.</p>
			</div>
			<div class="document-main">
				<h2>I. Introduction</h2>
				<p>Network security is a critical concern in modern systems.
				Machine learning techniques have shown promise in detecting anomalies.</p>

				<h2>II. Methodology</h2>
				<p>We propose a convolutional neural network architecture specifically designed
				for analyzing network traffic patterns. The key innovation is the use of
				attention mechanisms to focus on critical packet features.</p>
			</div>
		</div>
	</body>
	</html>
	"""

	server.expect_request('/document/12345').respond_with_data(
		paper_detail_html,
		content_type='text/html',
	)

	yield server
	server.stop()


@pytest.fixture(scope='session')
def ieee_base_url(ieee_mock_server):
	"""Return base URL for mock IEEE server."""
	return f'http://{ieee_mock_server.host}:{ieee_mock_server.port}'


@pytest.fixture(scope='module')
async def browser_session():
	"""Create browser session for tests."""
	profile = BrowserProfile(headless=True, disable_security=True)
	session = BrowserSession(browser_profile=profile)
	await session.start()
	yield session
	await session.kill()


class TestIEEESearchBasicFunctionality:
	"""Test basic IEEE search functionality."""

	async def test_search_returns_papers(self, browser_session: BrowserSession, ieee_base_url):
		"""Test that searching IEEE Xplore returns a list of papers."""
		# Arrange
		service = IEEESearchService(base_url=ieee_base_url)
		query = 'machine learning'

		# Act
		results = await service.search(query=query, max_results=10, browser_session=browser_session)

		# Assert
		assert results is not None
		assert len(results) > 0
		assert results[0]['title'] is not None

	async def test_extract_multiple_papers_from_html(self, browser_session: BrowserSession, ieee_base_url):
		"""Test extracting multiple papers with full metadata from HTML (triangulation)."""
		# Arrange
		service = IEEESearchService(base_url=ieee_base_url)
		query = 'deep learning'

		# Act
		results = await service.search(query=query, max_results=10, browser_session=browser_session)

		# Assert - should extract both papers from mock HTML
		assert len(results) == 2

		# First paper
		assert results[0]['title'] == 'Deep Learning for Network Traffic Classification'
		assert results[0]['authors'] == ['John Smith', 'Jane Doe']
		assert '/document/12345' in results[0]['url']

		# Second paper
		assert results[1]['title'] == 'Machine Learning in Cybersecurity'
		assert results[1]['authors'] == ['Alice Johnson']
		assert '/document/67890' in results[1]['url']


class TestCitationExtraction:
	"""Test citation and excerpt extraction from papers."""

	async def test_extract_citations_from_paper(self, browser_session: BrowserSession, ieee_base_url):
		"""Test extracting citations/excerpts from a paper with section tracking."""
		# Arrange
		service = IEEESearchService(base_url=ieee_base_url)
		paper_url = f'{ieee_base_url}/document/12345'

		# Act
		citations = await service.extract_citations(
			paper_url=paper_url,
			sections=['Abstract', 'Introduction', 'Methodology'],
			browser_session=browser_session,
		)

		# Assert
		assert len(citations) >= 2

		# Check abstract citation
		abstract_citation = next((c for c in citations if c.section == 'Abstract'), None)
		assert abstract_citation is not None
		assert 'novel approach' in abstract_citation.text
		assert abstract_citation.paper_url == paper_url
		assert abstract_citation.paper_title == 'Deep Learning for Network Traffic Classification'

		# Check methodology citation
		method_citation = next((c for c in citations if c.section == 'Methodology'), None)
		assert method_citation is not None
		assert 'attention mechanisms' in method_citation.text
