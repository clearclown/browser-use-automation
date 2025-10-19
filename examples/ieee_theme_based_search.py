"""
IEEE Theme-Based Paper Search Tool
Searches IEEE Xplore for multiple research themes and organizes results by theme.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

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

# Define research themes
RESEARCH_THEMES = {
	'machine_learning': {
		'query': 'machine learning',
		'description': 'Machine Learning & AI fundamentals',
	},
	'cybersecurity': {
		'query': 'cybersecurity threat detection',
		'description': 'Cybersecurity & Threat Detection',
	},
	'blockchain': {
		'query': 'blockchain distributed systems',
		'description': 'Blockchain & Distributed Systems',
	},
	'iot': {
		'query': 'internet of things sensor networks',
		'description': 'IoT & Sensor Networks',
	},
	'quantum_computing': {
		'query': 'quantum computing algorithms',
		'description': 'Quantum Computing & Algorithms',
	},
}


async def search_theme(
	theme_name: str, theme_config: dict[str, str], max_results: int, output_dir: Path, browser_session: BrowserSession
) -> dict[str, Any]:
	"""
	Search IEEE Xplore for papers in a specific theme.

	Args:
		theme_name: Theme identifier (e.g., "machine_learning")
		theme_config: Theme configuration with query and description
		max_results: Maximum number of papers to retrieve
		output_dir: Base output directory
		browser_session: Active browser session

	Returns:
		Dictionary with theme results
	"""
	query = theme_config['query']
	description = theme_config['description']

	logger.info(f'\n{"=" * 80}')
	logger.info(f'📚 Theme: {description}')
	logger.info(f'🔍 Query: "{query}"')
	logger.info(f'{"=" * 80}')

	# Create theme-specific directory
	theme_dir = output_dir / theme_name
	theme_dir.mkdir(parents=True, exist_ok=True)

	# Initialize IEEE search service
	ieee_service = IEEESearchService()

	try:
		# Perform search
		results = await ieee_service.search(query=query, max_results=max_results, browser_session=browser_session)

		# Display results
		logger.info(f'✅ Found {len(results)} papers for theme: {description}')

		for i, paper in enumerate(results, 1):
			logger.info(f'  {i}. {paper["title"][:80]}...')

		# Save results to theme directory
		output_file = theme_dir / 'search_results.json'
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(
				{'theme': theme_name, 'description': description, 'query': query, 'results': results, 'count': len(results)},
				f,
				indent=2,
				ensure_ascii=False,
			)

		logger.info(f'💾 Results saved to: {output_file}')

		return {'theme': theme_name, 'description': description, 'count': len(results), 'success': True}

	except Exception as e:
		logger.error(f'❌ Error searching theme "{description}": {e}')
		return {'theme': theme_name, 'description': description, 'count': 0, 'success': False, 'error': str(e)}


async def run_theme_based_search(themes: list[str] | None = None, max_results: int = 3, output_dir: str = './papers'):
	"""
	Run theme-based IEEE paper search.

	Args:
		themes: List of theme names to search (None = all themes)
		max_results: Maximum number of papers per theme
		output_dir: Base output directory
	"""
	logger.info('🚀 IEEE Theme-Based Paper Search Tool')
	logger.info('=' * 80)

	# Determine which themes to search
	if themes:
		selected_themes = {k: v for k, v in RESEARCH_THEMES.items() if k in themes}
	else:
		selected_themes = RESEARCH_THEMES

	logger.info(f'📊 Searching {len(selected_themes)} themes:')
	for theme_name, config in selected_themes.items():
		logger.info(f'  - {config["description"]}')
	logger.info('')

	# Create output directory
	base_output_dir = Path(output_dir)
	base_output_dir.mkdir(parents=True, exist_ok=True)

	# Create browser session
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
		logger.info('🌐 Browser session started\n')

		# Search each theme
		all_results = []
		for theme_name, theme_config in selected_themes.items():
			result = await search_theme(theme_name, theme_config, max_results, base_output_dir, browser_session)
			all_results.append(result)

		# Save summary
		summary_file = base_output_dir / 'search_summary.json'
		with open(summary_file, 'w', encoding='utf-8') as f:
			json.dump({'themes': all_results, 'total_themes': len(all_results)}, f, indent=2, ensure_ascii=False)

		# Print summary
		logger.info(f'\n{"=" * 80}')
		logger.info('📊 Search Summary:')
		logger.info(f'{"=" * 80}')

		total_papers = sum(r['count'] for r in all_results)
		successful_themes = sum(1 for r in all_results if r['success'])

		logger.info(f'✅ Successfully searched: {successful_themes}/{len(all_results)} themes')
		logger.info(f'📚 Total papers found: {total_papers}')
		logger.info(f'💾 Summary saved to: {summary_file}')

		for result in all_results:
			status = '✅' if result['success'] else '❌'
			logger.info(f'  {status} {result["description"]}: {result["count"]} papers')

	except Exception as e:
		logger.error(f'❌ Error during theme-based search: {e}', exc_info=True)

	finally:
		# Clean up
		await browser_session.kill()
		logger.info('\n🔚 Browser session closed')


@click.command()
@click.option(
	'--themes',
	'-t',
	multiple=True,
	type=click.Choice(list(RESEARCH_THEMES.keys()), case_sensitive=False),
	help='Specific themes to search (can be specified multiple times)',
)
@click.option(
	'--max-results',
	'-n',
	default=3,
	type=int,
	help='Maximum number of papers per theme',
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
@click.option(
	'--list-themes',
	is_flag=True,
	help='List available themes and exit',
)
def main(themes: tuple[str, ...], max_results: int, output: str, list_themes: bool):
	"""
	IEEE Theme-Based Paper Search Tool

	Search IEEE Xplore for multiple research themes and organize results.

	Examples:

	\b
	  # Search all themes (default)
	  python ieee_theme_based_search.py

	\b
	  # Search specific themes
	  python ieee_theme_based_search.py -t machine_learning -t cybersecurity

	\b
	  # Search with custom number of results per theme
	  python ieee_theme_based_search.py -n 5

	\b
	  # List available themes
	  python ieee_theme_based_search.py --list-themes
	"""
	if list_themes:
		logger.info('Available research themes:')
		for theme_name, config in RESEARCH_THEMES.items():
			logger.info(f"  - {theme_name}: {config['description']} ('{config['query']}')")
		return

	# Convert tuple to list (or None for all themes)
	theme_list = list(themes) if themes else None

	asyncio.run(run_theme_based_search(themes=theme_list, max_results=max_results, output_dir=output))


if __name__ == '__main__':
	main()
