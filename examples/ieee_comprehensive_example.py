"""
IEEE Paper Search - Comprehensive Example
Demonstrates all features: search, citation extraction, progress tracking.
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

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
	level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def comprehensive_demo(query: str = 'machine learning security', max_results: int = 3, output_dir: str = './papers'):
	"""Demonstrate all IEEE search features."""

	logger.info('=' * 80)
	logger.info('IEEE Paper Search - Comprehensive Demo')
	logger.info('All Features: Search + Citations + Progress Tracking')
	logger.info('=' * 80)

	# Initialize service
	ieee_service = IEEESearchService()

	# Create browser session
	# IEEE blocks headless browsers, use headless=False
	headless = os.getenv('HEADLESS', 'false').lower() == 'true'
	profile = BrowserProfile(
		headless=headless,
		disable_security=False,
		extra_chromium_args=[
			'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
		]
	)
	browser_session = BrowserSession(browser_profile=profile)
	await browser_session.start()

	try:
		# ============================================
		# FEATURE 1: Search with Progress Tracking
		# ============================================
		logger.info('\n📚 FEATURE 1: Searching IEEE Xplore with real-time progress...\n')

		def progress_callback(status: str, current: int, total: int):
			"""Display progress updates."""
			if total > 0:
				percentage = (current / total) * 100
				print(f'  📊 Progress: {status} [{current}/{total}] ({percentage:.0f}%)')
			else:
				print(f'  📊 {status}')

		# Search for papers
		results = await ieee_service.search(
			query=query, max_results=max_results, browser_session=browser_session, progress_callback=progress_callback
		)

		print(f'\n✅ Found {len(results)} papers:\n')
		for i, paper in enumerate(results, 1):
			print(f"{i}. {paper['title']}")
			print(f"   Authors: {', '.join(paper['authors'])}")
			print(f"   URL: {paper['url']}\n")

		# ============================================
		# FEATURE 2: Citation Extraction
		# ============================================
		if results:
			logger.info('\n📄 FEATURE 2: Extracting citations from first paper...\n')

			first_paper = results[0]
			print(f"Paper: {first_paper['title']}\n")

			# Extract citations from specific sections
			citations = await ieee_service.extract_citations(
				paper_url=first_paper['url'], sections=['Abstract', 'Introduction'], browser_session=browser_session
			)

			print(f'✅ Extracted {len(citations)} citations:\n')

			for i, citation in enumerate(citations, 1):
				print(f'{i}. Section: {citation.section}')
				print(f'   Text: {citation.text[:150]}...')
				print(f'   Paper: {citation.paper_title}')
				print(f'   URL: {citation.paper_url}\n')

			# ============================================
			# FEATURE 3: Save Citations with Metadata
			# ============================================
			logger.info('\n💾 FEATURE 3: Saving citations with full metadata...\n')

			output_path = Path(output_dir)
			output_path.mkdir(exist_ok=True)

			# Save citations
			citations_data = {
				'search_query': query,
				'paper_count': len(results),
				'citation_count': len(citations),
				'papers': [
					{'title': paper['title'], 'authors': paper['authors'], 'url': paper['url']} for paper in results
				],
				'citations': [
					{
						'text': c.text,
						'paper_title': c.paper_title,
						'paper_url': c.paper_url,
						'section': c.section,
						'authors': c.authors,
						'page_number': c.page_number,
						'notes': c.notes,
					}
					for c in citations
				],
			}

			output_file = output_path / f'comprehensive_demo_{query.replace(" ", "_")}.json'
			with open(output_file, 'w', encoding='utf-8') as f:
				json.dump(citations_data, f, indent=2, ensure_ascii=False)

			print(f'✅ Saved to: {output_file}')

			# Display summary
			logger.info('\n' + '=' * 80)
			logger.info('SUMMARY')
			logger.info('=' * 80)
			print(f'\n📊 Search Query: "{query}"')
			print(f'📚 Papers Found: {len(results)}')
			print(f'📝 Citations Extracted: {len(citations)}')
			print(f'💾 Output File: {output_file}')

			print('\n✅ Demo completed successfully!')
			print('\nFeatures demonstrated:')
			print('  ✅ IEEE Xplore paper search')
			print('  ✅ Real-time progress tracking')
			print('  ✅ Citation extraction with section tracking')
			print('  ✅ Full metadata preservation (title, authors, URL, page numbers)')
			print('  ✅ JSON export for further analysis')

	except Exception as e:
		logger.error(f'❌ Error during demo: {e}', exc_info=True)

	finally:
		# Clean up
		await browser_session.kill()
		logger.info('\n🔚 Browser session closed')


@click.command()
@click.option(
	'--query',
	'-q',
	default='machine learning security',
	help='Search query for IEEE Xplore',
	show_default=True,
)
@click.option(
	'--max-results',
	'-n',
	default=3,
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
	IEEE Paper Search - Comprehensive Demo

	Demonstrates all features: search, citation extraction, progress tracking.

	\b
	Features demonstrated:
	  - IEEE Xplore paper search with real-time progress
	  - Citation/excerpt extraction from papers
	  - Full metadata preservation
	  - JSON export

	\b
	Examples:
	  python ieee_comprehensive_example.py
	  python ieee_comprehensive_example.py -q "deep learning" -n 5
	  python ieee_comprehensive_example.py -q "neural networks" -o ./results
	"""
	# Set environment variables
	os.environ['HEADLESS'] = str(headless).lower()

	asyncio.run(comprehensive_demo(query=query, max_results=max_results, output_dir=output))


if __name__ == '__main__':
	main()
