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
