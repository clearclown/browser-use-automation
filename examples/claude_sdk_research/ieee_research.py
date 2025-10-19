"""
IEEE Research Assistant using Claude Agent SDK + browser-use

This example demonstrates how to use Claude Agent SDK with browser-use
to create a research assistant that can search and extract papers from IEEE Xplore.

Requirements:
- ANTHROPIC_API_KEY environment variable
- browser-use with claude-agent-sdk dependency

Usage:
	python ieee_research.py "machine learning robotics"
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock

from browser_use.claude_sdk_integration import create_browser_mcp_server


async def research_ieee(search_query: str, limit: int = 10, save_to_file: str | None = None) -> dict:
	"""
	Search IEEE Xplore for papers and extract structured data.

	Args:
		search_query: Search terms for IEEE Xplore
		limit: Maximum number of papers to extract
		save_to_file: Optional filename to save results as JSON

	Returns:
		Dictionary with search results
	"""

	# Configure Claude Agent with browser-use tools and ieee-researcher subagent
	options = ClaudeAgentOptions(
		# System prompt for the main orchestrator
		system_prompt="""You are a research assistant helping to find academic papers on IEEE Xplore.

Your task is to:
1. Use browser tools to navigate IEEE Xplore
2. Search for papers matching the user's query
3. Extract structured data from search results
4. Return results in JSON format

Be thorough but efficient. Extract key metadata: title, authors, year, DOI, abstract.""",
		# MCP server providing browser-use tools
		mcp_servers=create_browser_mcp_server('browser-use'),
		# Permission mode - auto-accept tool usage
		permission_mode='bypassPermissions',
		# Set working directory to project root to access .claude/
		cwd=Path(__file__).parent.parent.parent,
		# Enable project-level settings (reads .claude/CLAUDE.md, agents, commands)
		setting_sources=['project'],
		# Model selection
		model='claude-sonnet-4-5',
	)

	# Construct the research prompt
	prompt = f"""Search IEEE Xplore for papers related to: "{search_query}"

Instructions:
1. Navigate to https://ieeexplore.ieee.org/
2. Use the search functionality to find papers matching the query
3. Extract up to {limit} papers with the following information:
   - Title
   - Authors
   - Publication year
   - DOI or article number
   - Abstract (first 200 chars)
   - URL

4. Return results as JSON in this format:
{{
	"query": "{search_query}",
	"total_found": <number>,
	"papers": [
		{{
			"title": "...",
			"authors": ["..."],
			"year": 2024,
			"doi": "...",
			"abstract": "...",
			"url": "..."
		}}
	]
}}

Be efficient and extract clean, structured data."""

	print(f'\n🔍 Searching IEEE Xplore for: "{search_query}"')
	print(f'📊 Limit: {limit} papers\n')

	results = []
	full_text = ''

	# Execute query with Claude Agent SDK
	async for msg in query(prompt, options):
		if isinstance(msg, AssistantMessage):
			# Process assistant's response
			for block in msg.content:
				if isinstance(block, TextBlock):
					text = block.text
					full_text += text + '\n'
					print(text)

		elif isinstance(msg, ResultMessage):
			# Final result - extract cost and status
			print('\n✅ Research complete!')
			print(f'💰 Cost: ${msg.total_cost_usd:.4f}')
			print(f'⏱️  Duration: {msg.duration_ms / 1000:.1f}s')

	# Try to extract JSON from the response
	try:
		# Look for JSON block in the response
		import re

		json_match = re.search(r'```json\s*(\{.*?\})\s*```', full_text, re.DOTALL)
		if json_match:
			result_data = json.loads(json_match.group(1))
		else:
			# Try to find raw JSON
			json_match = re.search(r'\{[^{}]*"papers"[^{}]*\[[^\]]*\][^{}]*\}', full_text, re.DOTALL)
			if json_match:
				result_data = json.loads(json_match.group(0))
			else:
				result_data = {'query': search_query, 'papers': [], 'error': 'Could not extract JSON from response'}

		# Save to file if requested
		if save_to_file:
			output_path = Path(save_to_file)
			output_path.write_text(json.dumps(result_data, indent=2))
			print(f'\n💾 Results saved to: {output_path}')

		return result_data

	except json.JSONDecodeError as e:
		print(f'\n⚠️ Warning: Could not parse JSON response: {e}')
		return {'query': search_query, 'papers': [], 'error': str(e), 'raw_response': full_text}


async def main():
	"""Main entry point."""
	# Check for API key
	if not os.getenv('ANTHROPIC_API_KEY'):
		print('❌ Error: ANTHROPIC_API_KEY environment variable not set')
		sys.exit(1)

	# Parse command line arguments
	if len(sys.argv) < 2:
		print('Usage: python ieee_research.py "search query" [--limit N] [--save filename.json]')
		print('\nExample:')
		print('  python ieee_research.py "machine learning robotics" --limit 20 --save results.json')
		sys.exit(1)

	search_query = sys.argv[1]
	limit = 10
	save_file = None

	# Parse optional arguments
	for i in range(2, len(sys.argv)):
		if sys.argv[i] == '--limit' and i + 1 < len(sys.argv):
			limit = int(sys.argv[i + 1])
		elif sys.argv[i] == '--save' and i + 1 < len(sys.argv):
			save_file = sys.argv[i + 1]

	# Run research
	results = await research_ieee(search_query, limit=limit, save_to_file=save_file)

	# Print summary
	print('\n' + '=' * 60)
	print('📚 RESEARCH SUMMARY')
	print('=' * 60)
	print(f'Query: {results.get("query", "N/A")}')
	print(f'Papers found: {len(results.get("papers", []))}')

	if results.get('papers'):
		print('\nTop 3 papers:')
		for i, paper in enumerate(results['papers'][:3], 1):
			print(f'\n{i}. {paper.get("title", "N/A")}')
			print(f'   Authors: {", ".join(paper.get("authors", []))}')
			print(f'   Year: {paper.get("year", "N/A")}')
			print(f'   DOI: {paper.get("doi", "N/A")}')


if __name__ == '__main__':
	asyncio.run(main())
