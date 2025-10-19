"""
Claude Agent SDK integration for browser-use.

This module provides integration between browser-use and Claude Agent SDK,
allowing Claude agents to control browsers through SDK tools.
"""

from browser_use.claude_sdk_integration.tools import (
	BrowserUseToolkit,
	create_browser_mcp_server,
	get_browser_tools,
)

__all__ = [
	'BrowserUseToolkit',
	'create_browser_mcp_server',
	'get_browser_tools',
]
