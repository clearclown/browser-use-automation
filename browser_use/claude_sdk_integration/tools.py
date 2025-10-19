"""
Browser-use tools for Claude Agent SDK.

This module exposes browser-use actions as Claude Agent SDK tools,
allowing Claude agents to control browsers through the SDK.

Full integration with browser-use's event-driven architecture and Page API.
"""

import asyncio
import logging
import traceback
from typing import Any

from claude_agent_sdk import SdkMcpTool, create_sdk_mcp_server, tool

from browser_use.browser.events import NavigateToUrlEvent
from browser_use.browser.profile import BrowserProfile
from browser_use.browser.session import BrowserSession
from browser_use.browser.views import BrowserError

logger = logging.getLogger(__name__)


class BrowserUseToolkit:
	"""
	Toolkit for managing browser-use sessions and exposing them as Claude Agent SDK tools.

	This class manages the lifecycle of browser sessions and provides tools for:
	- Navigation (using NavigateToUrlEvent)
	- Element interaction (using Page API)
	- Content extraction (using Page.evaluate)
	- State management
	"""

	def __init__(
		self,
		browser_profile: BrowserProfile | None = None,
		headless: bool = False,
		keep_alive: bool = False,
		debug: bool = False,
	):
		"""
		Initialize the browser-use toolkit.

		Args:
			browser_profile: Custom browser profile configuration
			headless: Run browser in headless mode
			keep_alive: Keep browser alive after session ends
			debug: Enable debug logging
		"""
		self.browser_profile = browser_profile or BrowserProfile(headless=headless, keep_alive=keep_alive)
		self.session: BrowserSession | None = None
		self._lock = asyncio.Lock()
		self.debug = debug

		if debug:
			logger.setLevel(logging.DEBUG)
			logger.debug('🐛 Debug mode enabled for BrowserUseToolkit')

	async def _ensure_session(self) -> BrowserSession:
		"""Ensure browser session is initialized."""
		async with self._lock:
			if self.session is None:
				if self.debug:
					logger.debug('🔧 Creating new BrowserSession...')
				try:
					self.session = BrowserSession(browser_profile=self.browser_profile)
					await self.session.start()
					if self.debug:
						logger.debug(f'✅ BrowserSession created: {self.session.id}')
				except Exception as e:
					logger.error(f'❌ Failed to create BrowserSession: {e}')
					logger.error(traceback.format_exc())
					raise
			return self.session

	async def close(self):
		"""Close browser session and cleanup resources."""
		async with self._lock:
			if self.session:
				try:
					if self.debug:
						logger.debug(f'🔄 Stopping BrowserSession: {self.session.id}')
					await self.session.stop()
					if self.debug:
						logger.debug('✅ BrowserSession stopped')
				except Exception as e:
					logger.error(f'❌ Error stopping session: {e}')
					logger.error(traceback.format_exc())
				finally:
					self.session = None

	# Browser navigation tools
	async def navigate(self, url: str, wait_until: str = 'load') -> dict[str, Any]:
		"""
		Navigate to a URL using browser-use's event system.

		Args:
			url: The URL to navigate to
			wait_until: When to consider navigation complete ('load', 'domcontentloaded', 'networkidle')

		Returns:
			Result dict with page title and URL
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug(f'🌐 Navigating to: {url} (wait_until={wait_until})')

			# Use browser-use's event-driven navigation
			event = session.event_bus.dispatch(
				NavigateToUrlEvent(url=url, wait_until=wait_until, new_tab=False, timeout_ms=30000)  # type: ignore
			)

			# Wait for navigation to complete
			try:
				result = await asyncio.wait_for(event.event_result(raise_if_any=True), timeout=35.0)
				if self.debug:
					logger.debug(f'✅ Navigation completed: {result}')
			except asyncio.TimeoutError:
				logger.error(f'⏰ Navigation timeout for {url}')
				return {
					'content': [{'type': 'text', 'text': f'Navigation timeout: {url}'}],
					'is_error': True,
				}

			# Get current page state
			state = await session.get_browser_state_summary()

			return {
				'content': [
					{
						'type': 'text',
						'text': f'Navigated to: {state.url}\nTitle: {state.title}',
					}
				]
			}

		except BrowserError as e:
			logger.error(f'❌ Browser error during navigation: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Navigation failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error navigating to {url}: {str(e)}'}],
				'is_error': True,
			}

	async def click_element(self, selector: str) -> dict[str, Any]:
		"""
		Click an element by CSS selector using Page API.

		Args:
			selector: CSS selector for the element to click

		Returns:
			Result dict indicating success or failure
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug(f'🖱️  Clicking element: {selector}')

			# Get current page
			page = await session.must_get_current_page()

			# Use Page.evaluate to click the element
			js_code = f"""
				() => {{
					const element = document.querySelector('{selector}');
					if (element) {{
						element.click();
						return true;
					}}
					return false;
				}}
			"""

			result = await page.evaluate(js_code)

			if result == 'true':
				if self.debug:
					logger.debug(f'✅ Clicked element: {selector}')
				return {'content': [{'type': 'text', 'text': f'Clicked element: {selector}'}]}
			else:
				logger.warning(f'⚠️  Element not found: {selector}')
				return {
					'content': [{'type': 'text', 'text': f'Element not found: {selector}'}],
					'is_error': True,
				}

		except BrowserError as e:
			logger.error(f'❌ Browser error clicking element: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Click failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error clicking {selector}: {str(e)}'}],
				'is_error': True,
			}

	async def type_text(self, selector: str, text: str, clear: bool = True) -> dict[str, Any]:
		"""
		Type text into an element using Page API.

		Args:
			selector: CSS selector for the input element
			text: Text to type
			clear: Clear existing text before typing

		Returns:
			Result dict indicating success or failure
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug(f'⌨️  Typing into {selector}: "{text}"')

			page = await session.must_get_current_page()

			# Escape single quotes in text
			escaped_text = text.replace("'", "\\'")

			clear_script = "element.value = '';" if clear else ''

			js_code = f"""
				() => {{
					const element = document.querySelector('{selector}');
					if (element) {{
						{clear_script}
						element.value = '{escaped_text}';
						element.dispatchEvent(new Event('input', {{ bubbles: true }}));
						element.dispatchEvent(new Event('change', {{ bubbles: true }}));
						return true;
					}}
					return false;
				}}
			"""

			result = await page.evaluate(js_code)

			if result == 'true':
				if self.debug:
					logger.debug(f'✅ Typed text into: {selector}')
				return {'content': [{'type': 'text', 'text': f'Typed "{text}" into {selector}'}]}
			else:
				logger.warning(f'⚠️  Element not found: {selector}')
				return {
					'content': [{'type': 'text', 'text': f'Element not found: {selector}'}],
					'is_error': True,
				}

		except BrowserError as e:
			logger.error(f'❌ Browser error typing text: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Type failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error typing into {selector}: {str(e)}'}],
				'is_error': True,
			}

	async def extract_content(self, selector: str | None = None) -> dict[str, Any]:
		"""
		Extract text content from page or specific element using Page API.

		Args:
			selector: Optional CSS selector to extract from specific element

		Returns:
			Result dict with extracted content
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug(f'📄 Extracting content from: {selector or "document.body"}')

			page = await session.must_get_current_page()

			if selector:
				js_code = f"""
					() => {{
						const element = document.querySelector('{selector}');
						return element ? element.textContent : null;
					}}
				"""
			else:
				js_code = '() => document.body.textContent'

			content = await page.evaluate(js_code)

			if content and content != 'null':
				if self.debug:
					logger.debug(f'✅ Extracted {len(content)} characters')
				return {'content': [{'type': 'text', 'text': f'Extracted content:\n{content}'}]}
			else:
				logger.warning('⚠️  No content found')
				return {
					'content': [{'type': 'text', 'text': 'No content found'}],
					'is_error': True,
				}

		except BrowserError as e:
			logger.error(f'❌ Browser error extracting content: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Content extraction failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error extracting content: {str(e)}'}],
				'is_error': True,
			}

	async def get_page_state(self) -> dict[str, Any]:
		"""
		Get current page state (URL, title, tabs).

		Returns:
			Result dict with page state information
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug('📊 Getting page state...')

			state = await session.get_browser_state_summary()

			info = f"""Current Browser State:
URL: {state.url}
Title: {state.title}
Tabs: {len(state.tabs)} open
"""

			if self.debug:
				logger.debug(f'✅ Page state retrieved: {state.url}')

			return {'content': [{'type': 'text', 'text': info}]}

		except BrowserError as e:
			logger.error(f'❌ Browser error getting state: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Get state failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error getting page state: {str(e)}'}],
				'is_error': True,
			}

	async def scroll(self, direction: str = 'down', amount: int = 500) -> dict[str, Any]:
		"""
		Scroll the page using Page API.

		Args:
			direction: Scroll direction ('up' or 'down')
			amount: Scroll amount in pixels

		Returns:
			Result dict indicating scroll action
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug(f'📜 Scrolling {direction} by {amount}px')

			page = await session.must_get_current_page()

			scroll_amount = amount if direction == 'down' else -amount
			js_code = f'() => window.scrollBy(0, {scroll_amount})'

			await page.evaluate(js_code)

			if self.debug:
				logger.debug(f'✅ Scrolled {direction}')

			return {'content': [{'type': 'text', 'text': f'Scrolled {direction} by {amount}px'}]}

		except BrowserError as e:
			logger.error(f'❌ Browser error scrolling: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Scroll failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error scrolling: {str(e)}'}],
				'is_error': True,
			}

	async def go_back(self) -> dict[str, Any]:
		"""
		Navigate back in browser history using Page API.

		Returns:
			Result dict indicating success
		"""
		try:
			session = await self._ensure_session()

			if self.debug:
				logger.debug('⬅️  Going back in history...')

			page = await session.must_get_current_page()

			js_code = '() => window.history.back()'
			await page.evaluate(js_code)

			# Wait for navigation
			await asyncio.sleep(1)

			state = await session.get_browser_state_summary()

			if self.debug:
				logger.debug(f'✅ Navigated back to: {state.url}')

			return {'content': [{'type': 'text', 'text': f'Navigated back to: {state.url}'}]}

		except BrowserError as e:
			logger.error(f'❌ Browser error going back: {e}')
			return {
				'content': [{'type': 'text', 'text': f'Browser error: {e.message}'}],
				'is_error': True,
			}
		except Exception as e:
			logger.error(f'❌ Go back failed: {e}')
			logger.error(traceback.format_exc())
			return {
				'content': [{'type': 'text', 'text': f'Error going back: {str(e)}'}],
				'is_error': True,
			}


# Global toolkit instance (can be customized)
_global_toolkit: BrowserUseToolkit | None = None


def get_global_toolkit(headless: bool = False, keep_alive: bool = False, debug: bool = False) -> BrowserUseToolkit:
	"""Get or create global browser toolkit instance."""
	global _global_toolkit
	if _global_toolkit is None:
		_global_toolkit = BrowserUseToolkit(headless=headless, keep_alive=keep_alive, debug=debug)
	return _global_toolkit


# Define Claude Agent SDK tools
@tool(
	name='browser_navigate',
	description='Navigate to a URL in the browser',
	input_schema={'url': str, 'wait_until': str},
)
async def browser_navigate_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Navigate to a URL."""
	toolkit = get_global_toolkit()
	return await toolkit.navigate(args['url'], args.get('wait_until', 'load'))


@tool(
	name='browser_click',
	description='Click an element on the page using CSS selector',
	input_schema={'selector': str},
)
async def browser_click_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Click an element."""
	toolkit = get_global_toolkit()
	return await toolkit.click_element(args['selector'])


@tool(
	name='browser_type',
	description='Type text into an input element using CSS selector',
	input_schema={'selector': str, 'text': str, 'clear': bool},
)
async def browser_type_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Type text into an element."""
	toolkit = get_global_toolkit()
	return await toolkit.type_text(args['selector'], args['text'], args.get('clear', True))


@tool(
	name='browser_extract',
	description='Extract text content from the page or a specific element',
	input_schema={'selector': str},
)
async def browser_extract_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Extract content from page."""
	toolkit = get_global_toolkit()
	return await toolkit.extract_content(args.get('selector'))


@tool(
	name='browser_get_state',
	description='Get current browser state (URL, title, tabs)',
	input_schema={},
)
async def browser_get_state_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Get current browser state."""
	toolkit = get_global_toolkit()
	return await toolkit.get_page_state()


@tool(
	name='browser_scroll',
	description='Scroll the page up or down',
	input_schema={'direction': str, 'amount': int},
)
async def browser_scroll_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Scroll the page."""
	toolkit = get_global_toolkit()
	return await toolkit.scroll(args.get('direction', 'down'), args.get('amount', 500))


@tool(
	name='browser_go_back',
	description='Navigate back in browser history',
	input_schema={},
)
async def browser_go_back_tool(args: dict[str, Any]) -> dict[str, Any]:
	"""Go back in history."""
	toolkit = get_global_toolkit()
	return await toolkit.go_back()


def get_browser_tools() -> list[SdkMcpTool]:
	"""
	Get list of all browser-use tools for Claude Agent SDK.

	Returns:
		List of SdkMcpTool instances
	"""
	return [
		browser_navigate_tool,
		browser_click_tool,
		browser_type_tool,
		browser_extract_tool,
		browser_get_state_tool,
		browser_scroll_tool,
		browser_go_back_tool,
	]


def create_browser_mcp_server(name: str = 'browser-use', debug: bool = False) -> dict[str, Any]:
	"""
	Create an MCP server configuration for browser-use tools.

	Args:
		name: Name of the MCP server
		debug: Enable debug logging

	Returns:
		MCP server configuration dict for use in ClaudeAgentOptions
	"""
	# Initialize global toolkit with debug setting
	get_global_toolkit(debug=debug)

	return {
		name: create_sdk_mcp_server(
			name=name,
			tools=get_browser_tools(),
		)
	}
