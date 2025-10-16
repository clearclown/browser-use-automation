"""
IEEE Paper Search - Interactive Chat Interface
Allows users to search and extract citations interactively.
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
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IEEEChatInterface:
	"""Interactive chat interface for IEEE paper search."""

	def __init__(self):
		self.service = IEEESearchService()
		self.browser_session: BrowserSession | None = None
		self.current_results = []
		self.citations_db = []

	async def start_browser(self):
		"""Initialize browser session."""
		if self.browser_session is None:
			logger.info('🌐 Starting browser session...')
			# IEEE blocks headless browsers, use headless=False
			import os
			headless = os.getenv('HEADLESS', 'false').lower() == 'true'
			profile = BrowserProfile(
				headless=headless,
				disable_security=False,
				extra_chromium_args=[
					'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
				]
			)
			self.browser_session = BrowserSession(browser_profile=profile)
			await self.browser_session.start()
			logger.info('✅ Browser ready')

	async def stop_browser(self):
		"""Stop browser session."""
		if self.browser_session:
			await self.browser_session.kill()
			self.browser_session = None
			logger.info('🔚 Browser stopped')

	def progress_callback(self, status: str, current: int, total: int):
		"""Display progress information."""
		if total > 0:
			percentage = (current / total) * 100
			print(f'  📊 {status} [{current}/{total}] ({percentage:.0f}%)')
		else:
			print(f'  📊 {status}')

	async def search_papers(self, query: str, max_results: int = 5):
		"""Search for papers and display results."""
		await self.start_browser()

		logger.info(f'\n🔍 Searching for: "{query}"')
		self.current_results = await self.service.search(
			query=query,
			max_results=max_results,
			browser_session=self.browser_session,
			progress_callback=self.progress_callback,
		)

		print(f'\n📚 Found {len(self.current_results)} papers:\n')
		for i, paper in enumerate(self.current_results, 1):
			print(f"{i}. {paper['title']}")
			print(f"   Authors: {', '.join(paper['authors'])}")
			print(f"   URL: {paper['url']}\n")

		return self.current_results

	async def extract_citations_from_paper(self, paper_index: int, sections: list[str] | None = None):
		"""Extract citations from a specific paper."""
		if not self.current_results or paper_index < 1 or paper_index > len(self.current_results):
			print('❌ Invalid paper number')
			return

		paper = self.current_results[paper_index - 1]
		logger.info(f'\n📄 Extracting citations from: {paper["title"]}')

		citations = await self.service.extract_citations(
			paper_url=paper['url'], sections=sections, browser_session=self.browser_session
		)

		print(f'\n✅ Extracted {len(citations)} citations:\n')
		for i, citation in enumerate(citations, 1):
			print(f'{i}. [{citation.section}]')
			print(f'   {citation.text[:200]}...\n')

		# Save to citations database
		self.citations_db.extend(citations)

		return citations

	def save_citations(self, filename: str = 'citations.json'):
		"""Save all collected citations to file."""
		output_dir = Path(os.getenv('OUTPUT_DIR', './papers'))
		output_dir.mkdir(exist_ok=True)

		output_file = output_dir / filename

		citations_data = [
			{
				'text': c.text,
				'paper_title': c.paper_title,
				'paper_url': c.paper_url,
				'section': c.section,
				'authors': c.authors,
				'page_number': c.page_number,
			}
			for c in self.citations_db
		]

		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(citations_data, f, indent=2, ensure_ascii=False)

		print(f'\n💾 Saved {len(self.citations_db)} citations to: {output_file}')

	async def run_interactive(self):
		"""Run interactive chat loop."""
		print('=' * 80)
		print('IEEE Paper Search - Interactive Chat Interface')
		print('=' * 80)
		print('\nCommands:')
		print('  search <query> [max_results]  - Search for papers')
		print('  extract <paper_number> [sections]  - Extract citations from a paper')
		print('  list                          - List current search results')
		print('  citations                     - Show all collected citations')
		print('  save [filename]               - Save citations to JSON file')
		print('  quit / exit                   - Exit')
		print()

		try:
			while True:
				user_input = input('🔎 > ').strip()

				if not user_input:
					continue

				parts = user_input.split()
				command = parts[0].lower()

				if command in ['quit', 'exit']:
					print('\n👋 Goodbye!')
					break

				elif command == 'search':
					if len(parts) < 2:
						print('❌ Usage: search <query> [max_results]')
						continue

					query = ' '.join(parts[1:-1]) if len(parts) > 2 and parts[-1].isdigit() else ' '.join(parts[1:])
					max_results = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 5

					await self.search_papers(query, max_results)

				elif command == 'extract':
					if len(parts) < 2:
						print('❌ Usage: extract <paper_number> [sections]')
						continue

					paper_num = int(parts[1])
					sections = parts[2:] if len(parts) > 2 else None

					await self.extract_citations_from_paper(paper_num, sections)

				elif command == 'list':
					if not self.current_results:
						print('❌ No search results. Use "search" first.')
						continue

					print(f'\n📚 Current search results ({len(self.current_results)} papers):\n')
					for i, paper in enumerate(self.current_results, 1):
						print(f"{i}. {paper['title']}")

				elif command == 'citations':
					print(f'\n📝 Collected citations: {len(self.citations_db)}\n')
					for i, citation in enumerate(self.citations_db, 1):
						print(f'{i}. [{citation.section}] {citation.paper_title}')
						print(f'   {citation.text[:100]}...\n')

				elif command == 'save':
					filename = parts[1] if len(parts) > 1 else 'citations.json'
					self.save_citations(filename)

				else:
					print(f'❌ Unknown command: {command}')
					print('Use "search", "extract", "list", "citations", "save", or "quit"')

		except KeyboardInterrupt:
			print('\n\n👋 Interrupted. Exiting...')

		finally:
			await self.stop_browser()


@click.command()
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
	help='Output directory for saved citations',
	show_default=True,
)
def main(headless: bool, output: str):
	"""
	IEEE Paper Search - Interactive Chat Interface

	Interactive command-line interface for searching IEEE Xplore
	and extracting citations from papers.

	\b
	Available commands in chat:
	  search <query> [max_results]  - Search for papers
	  extract <paper_number> [sections]  - Extract citations
	  list - Show current search results
	  citations - Show collected citations
	  save [filename] - Save citations to JSON
	  quit / exit - Exit the program

	\b
	Examples:
	  python ieee_chat_interface.py
	  python ieee_chat_interface.py --no-headless
	  python ieee_chat_interface.py -o ./my_citations
	"""
	# Set environment variables
	os.environ['HEADLESS'] = str(headless).lower()
	os.environ['OUTPUT_DIR'] = output

	chat = IEEEChatInterface()
	asyncio.run(chat.run_interactive())


if __name__ == '__main__':
	main()
