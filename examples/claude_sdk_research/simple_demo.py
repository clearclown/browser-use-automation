"""
Simple demo of Claude Agent SDK + browser-use integration

This example shows basic browser automation using Claude Agent SDK with browser-use tools.

Requirements:
- ANTHROPIC_API_KEY environment variable

Usage:
	python simple_demo.py
"""

import asyncio
import os
import sys

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock

from browser_use.claude_sdk_integration import create_browser_mcp_server


async def simple_browser_demo():
	"""
	Simple demo: Navigate to a website and extract information.
	"""

	# Check for API key
	if not os.getenv('ANTHROPIC_API_KEY'):
		print('❌ Error: ANTHROPIC_API_KEY environment variable not set')
		sys.exit(1)

	# Configure Claude Agent with browser-use tools
	options = ClaudeAgentOptions(
		system_prompt="""You are a helpful browser automation assistant.
You have access to browser tools to navigate websites and extract information.
Be concise and efficient in your responses.""",
		mcp_servers=create_browser_mcp_server('browser-use'),
		permission_mode='bypassPermissions',
		model='claude-sonnet-4-5',
	)

	# Example 1: Simple navigation
	print('=' * 60)
	print('🌐 Example 1: Navigate to a website and get page info')
	print('=' * 60)

	prompt1 = """Navigate to https://example.com and tell me:
1. The page title
2. The main heading
3. A brief summary of what the page says"""

	async for msg in query(prompt1, options):
		if isinstance(msg, AssistantMessage):
			for block in msg.content:
				if isinstance(block, TextBlock):
					print(block.text)

	print('\n')

	# Example 2: Search and extract
	print('=' * 60)
	print('🔍 Example 2: Search and extract information')
	print('=' * 60)

	prompt2 = """Go to https://www.python.org and:
1. Find the latest Python version number
2. Extract the download link for that version
3. Tell me what's new in that version (if visible on the page)"""

	async for msg in query(prompt2, options):
		if isinstance(msg, AssistantMessage):
			for block in msg.content:
				if isinstance(block, TextBlock):
					print(block.text)

	print('\n✅ Demo complete!')


async def interactive_mode():
	"""
	Interactive mode: Chat with Claude and use browser tools.
	"""

	# Check for API key
	if not os.getenv('ANTHROPIC_API_KEY'):
		print('❌ Error: ANTHROPIC_API_KEY environment variable not set')
		sys.exit(1)

	print('=' * 60)
	print('💬 Interactive Browser Mode')
	print('=' * 60)
	print('Ask Claude to browse websites and extract information.')
	print('Type "exit" to quit.\n')

	# Configure Claude Agent with browser-use tools
	options = ClaudeAgentOptions(
		system_prompt="""You are a helpful browser automation assistant.
You have access to browser tools to navigate websites and extract information.
When asked to browse a website:
1. Navigate to the URL
2. Extract relevant information
3. Provide a clear, structured answer

Be helpful and efficient!""",
		mcp_servers=create_browser_mcp_server('browser-use'),
		permission_mode='bypassPermissions',
		model='claude-sonnet-4-5',
	)

	while True:
		# Get user input
		user_input = input('\n👤 You: ').strip()

		if user_input.lower() in ['exit', 'quit', 'q']:
			print('👋 Goodbye!')
			break

		if not user_input:
			continue

		# Send to Claude
		print('\n🤖 Claude:')
		async for msg in query(user_input, options):
			if isinstance(msg, AssistantMessage):
				for block in msg.content:
					if isinstance(block, TextBlock):
						print(block.text)


async def main():
	"""Main entry point."""
	print('\n🚀 Claude Agent SDK + browser-use Demo\n')
	print('Choose a mode:')
	print('1. Run preset demos (simple_browser_demo)')
	print('2. Interactive mode (chat with Claude)')
	print('3. Exit')

	choice = input('\nEnter choice (1/2/3): ').strip()

	if choice == '1':
		await simple_browser_demo()
	elif choice == '2':
		await interactive_mode()
	elif choice == '3':
		print('👋 Goodbye!')
	else:
		print('❌ Invalid choice')


if __name__ == '__main__':
	asyncio.run(main())
