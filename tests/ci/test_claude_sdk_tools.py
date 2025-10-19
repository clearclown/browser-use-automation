"""
Tests for Claude Agent SDK integration with browser-use.

These tests verify that the browser-use tools are properly exposed
as Claude Agent SDK tools.
"""

import pytest

from browser_use.claude_sdk_integration import (
	BrowserUseToolkit,
	create_browser_mcp_server,
	get_browser_tools,
)


class TestBrowserUseToolkit:
	"""Test the BrowserUseToolkit class."""

	@pytest.fixture
	async def toolkit(self):
		"""Create a toolkit instance."""
		tk = BrowserUseToolkit(headless=True)
		yield tk
		await tk.close()

	async def test_toolkit_initialization(self):
		"""Test that toolkit can be initialized."""
		toolkit = BrowserUseToolkit(headless=True, keep_alive=False)
		assert toolkit.session is None
		assert toolkit.browser_profile is not None
		await toolkit.close()

	async def test_toolkit_session_creation(self, toolkit):
		"""Test that session is created on first use."""
		session = await toolkit._ensure_session()
		assert session is not None
		assert toolkit.session is not None

	async def test_navigate(self, toolkit):
		"""Test navigation functionality."""
		result = await toolkit.navigate('https://example.com')
		assert 'content' in result
		assert len(result['content']) > 0
		assert result['content'][0]['type'] == 'text'
		assert 'example.com' in result['content'][0]['text'].lower()

	async def test_get_page_state(self, toolkit):
		"""Test getting page state."""
		# First navigate somewhere
		await toolkit.navigate('https://example.com')

		# Then get state
		result = await toolkit.get_page_state()
		assert 'content' in result
		assert 'URL' in result['content'][0]['text']
		assert 'Title' in result['content'][0]['text']

	async def test_extract_content(self, toolkit):
		"""Test content extraction."""
		# Navigate to a page
		await toolkit.navigate('https://example.com')

		# Extract content
		result = await toolkit.extract_content()
		assert 'content' in result
		# Should extract some text from example.com
		assert len(result['content'][0]['text']) > 0

	async def test_scroll(self, toolkit):
		"""Test scrolling."""
		await toolkit.navigate('https://example.com')

		# Scroll down
		result = await toolkit.scroll('down', 500)
		assert 'content' in result
		assert 'Scrolled' in result['content'][0]['text']

		# Scroll up
		result = await toolkit.scroll('up', 300)
		assert 'content' in result
		assert 'Scrolled' in result['content'][0]['text']

	async def test_error_handling_invalid_url(self, toolkit):
		"""Test error handling for invalid URL."""
		result = await toolkit.navigate('not-a-valid-url')
		assert 'is_error' in result
		assert result['is_error'] is True


class TestBrowserTools:
	"""Test the exported browser tools for Claude Agent SDK."""

	def test_get_browser_tools(self):
		"""Test that get_browser_tools returns a list of tools."""
		tools = get_browser_tools()
		assert isinstance(tools, list)
		assert len(tools) > 0

		# Check that we have the expected tools
		tool_names = [tool.name for tool in tools]
		assert 'browser_navigate' in tool_names
		assert 'browser_click' in tool_names
		assert 'browser_type' in tool_names
		assert 'browser_extract' in tool_names
		assert 'browser_get_state' in tool_names
		assert 'browser_scroll' in tool_names
		assert 'browser_go_back' in tool_names

	def test_create_browser_mcp_server(self):
		"""Test MCP server creation."""
		mcp_config = create_browser_mcp_server('test-browser')
		assert isinstance(mcp_config, dict)
		assert 'test-browser' in mcp_config


class TestToolIntegration:
	"""Test individual tool functions via BrowserUseToolkit."""

	@pytest.fixture
	async def toolkit(self):
		"""Create a toolkit instance for integration tests."""
		from browser_use.claude_sdk_integration import BrowserUseToolkit

		tk = BrowserUseToolkit(headless=True, keep_alive=False)
		yield tk
		await tk.close()

	async def test_browser_navigate_integration(self, toolkit):
		"""Test browser navigate via toolkit."""
		result = await toolkit.navigate('https://example.com', 'load')
		assert 'content' in result
		assert isinstance(result['content'], list)
		assert len(result['content']) > 0

	async def test_browser_get_state_integration(self, toolkit):
		"""Test browser get_state via toolkit."""
		# First navigate
		await toolkit.navigate('https://example.com', 'load')

		# Then get state
		result = await toolkit.get_page_state()
		assert 'content' in result
		assert isinstance(result['content'], list)

	async def test_browser_scroll_integration(self, toolkit):
		"""Test browser scroll via toolkit."""
		# Navigate first
		await toolkit.navigate('https://example.com', 'load')

		# Scroll
		result = await toolkit.scroll('down', 500)
		assert 'content' in result
