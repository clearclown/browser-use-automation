"""
IEEE Paper Search Tool Example
Demonstrates how to search IEEE Xplore for academic papers.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

import click
from dotenv import load_dotenv

from browser_use.browser import BrowserSession
from browser_use.browser.profile import BrowserProfile
from browser_use.integrations.ieee_search import IEEESearchService

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
		],
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
		logger.info(f'\n{"=" * 80}')
		logger.info(f'📊 Found {len(results)} papers:')
		logger.info(f'{"=" * 80}\n')

		for i, paper in enumerate(results, 1):
			logger.info(f'{i}. Title: {paper["title"]}')
			logger.info(f'   Authors: {", ".join(paper["authors"])}')
			logger.info(f'   URL: {paper["url"]}')
			logger.info('')

		# Save results to JSON file
		output_dir = Path(os.getenv('OUTPUT_DIR', './papers'))
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


@click.command()
@click.option(
	'--query',
	'-q',
	default='machine learning cybersecurity',
	help='Search query for IEEE Xplore',
	show_default=True,
)
@click.option(
	'--max-results',
	'-n',
	default=5,
	type=int,
	help='Maximum number of papers to retrieve',
	show_default=True,
)
@click.option(
	'--headless/--no-headless',
	default=False,
	help='Run browser in headless mode (may be blocked by IEEE)',
	show_default=True,
)
@click.option(
	'--output',
	'-o',
	type=click.Path(dir_okay=True, file_okay=False),
	default='./papers',
	help='Output directory for results',
	show_default=True,
)
def main(query: str, max_results: int, headless: bool, output: str):
	"""
	IEEE Paper Search Tool

	Search IEEE Xplore for academic papers and save results to JSON.

	Examples:

	\b
	  # Basic search
	  python ieee_paper_search.py --query "deep learning"

	\b
	  # Search with custom number of results
	  python ieee_paper_search.py -q "neural networks" -n 10

	\b
	  # Specify output directory
	  python ieee_paper_search.py -q "machine learning" -o ./my_papers
	"""
	logger.info('🚀 IEEE Paper Search Tool')
	logger.info('=' * 80)

	# Override headless setting if HEADLESS env var is set
	if os.getenv('HEADLESS'):
		headless = os.getenv('HEADLESS', 'false').lower() == 'true'

	# Set environment variable for search function
	os.environ['HEADLESS'] = str(headless).lower()
	os.environ['OUTPUT_DIR'] = output

	asyncio.run(search_ieee_papers(query=query, max_results=max_results))


if __name__ == '__main__':
	main()
