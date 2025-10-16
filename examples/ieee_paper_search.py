"""
IEEE Paper Search Tool Example
Demonstrates how to search IEEE Xplore for academic papers.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
	level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def search_ieee_papers(query: str, max_results: int = 5):
	"""
	Search IEEE Xplore for papers matching the query.

	Args:
		query: Search keywords (e.g., "machine learning", "neural networks")
		max_results: Maximum number of papers to retrieve
	"""
	logger.info(f'🔍 Starting IEEE paper search for: "{query}"')

	# Create browser session
	# Note: IEEE blocks headless browsers, so use headless=False
	# Set HEADLESS=true environment variable to force headless mode
	headless = os.getenv('HEADLESS', 'false').lower() == 'true'
	profile = BrowserProfile(
		headless=headless,
		disable_security=False,
		extra_chromium_args=[
			'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
		]
	)
	browser_session = BrowserSession(browser_profile=profile)

	try:
		# Start browser
		await browser_session.start()
		logger.info('🌐 Browser session started')

		# Initialize IEEE search service
		ieee_service = IEEESearchService()

		# Perform search
		logger.info(f'📚 Searching for: "{query}"...')
		results = await ieee_service.search(query=query, max_results=max_results, browser_session=browser_session)

		# Display results
		logger.info(f'\n{"="*80}')
		logger.info(f'📊 Found {len(results)} papers:')
		logger.info(f'{"="*80}\n')

		for i, paper in enumerate(results, 1):
			logger.info(f'{i}. Title: {paper["title"]}')
			logger.info(f'   Authors: {", ".join(paper["authors"])}')
			logger.info(f'   URL: {paper["url"]}')
			logger.info('')

		# Save results to JSON file
		output_dir = Path('./papers')
		output_dir.mkdir(exist_ok=True)

		output_file = output_dir / f'search_results_{query.replace(" ", "_")}.json'
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump({'query': query, 'results': results, 'count': len(results)}, f, indent=2, ensure_ascii=False)

		logger.info(f'💾 Results saved to: {output_file}')

	except Exception as e:
		logger.error(f'❌ Error during search: {e}', exc_info=True)

	finally:
		# Clean up
		await browser_session.kill()
		logger.info('🔚 Browser session closed')


async def main():
	"""Main entry point for the IEEE paper search tool."""
	# Example queries
	queries = [
		'machine learning cybersecurity',
		'deep learning network traffic',
		'neural networks intrusion detection',
	]

	# You can also specify a single query
	single_query = os.getenv('SEARCH_QUERY', queries[0])

	logger.info('🚀 IEEE Paper Search Tool')
	logger.info('=' * 80)

	await search_ieee_papers(query=single_query, max_results=5)


if __name__ == '__main__':
	asyncio.run(main())
