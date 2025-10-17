"""
HTLL & AIM Research Paper Search
Searches for papers related to:
1. Autonomous Intersection Management (AIM) and V2X
2. High Throughput Low Latency (HTLL) streaming data processing
3. FCFS intersection control algorithms
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


async def search_multiple_queries(queries: list[dict], max_results_per_query: int = 10):
	"""
	Search IEEE Xplore for multiple queries and save results.

	Args:
		queries: List of dictionaries with 'name' and 'query' keys
		max_results_per_query: Maximum number of papers to retrieve per query
	"""
	logger.info(f'🔍 Starting multi-query IEEE paper search')
	logger.info(f'📊 Queries to search: {len(queries)}')
	logger.info(f'📄 Max results per query: {max_results_per_query}')

	# Create browser session
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

		# Store all results
		all_results = {}

		# Perform searches for each query
		for i, query_info in enumerate(queries, 1):
			query_name = query_info['name']
			query_text = query_info['query']

			logger.info(f'\n{"="*80}')
			logger.info(f'📚 [{i}/{len(queries)}] Searching: {query_name}')
			logger.info(f'🔎 Query: "{query_text}"')
			logger.info(f'{"="*80}\n')

			# Perform search
			results = await ieee_service.search(
				query=query_text,
				max_results=max_results_per_query,
				browser_session=browser_session
			)

			# Store results
			all_results[query_name] = {
				'query': query_text,
				'count': len(results),
				'papers': results
			}

			# Display results
			logger.info(f'✅ Found {len(results)} papers for "{query_name}":')
			for j, paper in enumerate(results, 1):
				logger.info(f'  {j}. {paper["title"][:100]}...')
				logger.info(f'     Authors: {", ".join(paper["authors"][:3])}{"..." if len(paper["authors"]) > 3 else ""}')
			logger.info('')

			# Wait a bit between queries to avoid rate limiting
			if i < len(queries):
				logger.info('⏳ Waiting 3 seconds before next query...')
				await asyncio.sleep(3)

		# Save all results to JSON file
		output_dir = Path('./papers')
		output_dir.mkdir(exist_ok=True)

		output_file = output_dir / 'htll_aim_research_papers.json'
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(all_results, f, indent=2, ensure_ascii=False)

		logger.info(f'\n{"="*80}')
		logger.info(f'💾 All results saved to: {output_file}')
		logger.info(f'📊 Total queries: {len(queries)}')
		logger.info(f'📄 Total papers found: {sum(r["count"] for r in all_results.values())}')
		logger.info(f'{"="*80}\n')

		return all_results

	except Exception as e:
		logger.error(f'❌ Error during search: {e}', exc_info=True)

	finally:
		# Clean up
		await browser_session.kill()
		logger.info('🔚 Browser session closed')


async def main():
	"""
	Main function to search for HTLL & AIM research papers.
	"""
	logger.info('🚀 HTLL & AIM Research Paper Search Tool')
	logger.info('=' * 80)

	# Define search queries related to the research
	queries = [
		{
			'name': 'AIM_V2X_Intersection',
			'query': 'autonomous intersection management V2X'
		},
		{
			'name': 'FCFS_Intersection_Control',
			'query': 'FCFS first come first served intersection control'
		},
		{
			'name': 'Streaming_Kafka_Flink',
			'query': 'real-time streaming data processing Kafka Flink'
		},
		{
			'name': 'HTLL_Architecture',
			'query': 'high throughput low latency architecture real-time'
		},
		{
			'name': 'V2X_Traffic_Management',
			'query': 'V2X vehicle-to-everything traffic management system'
		},
		{
			'name': 'Apache_Druid_Analytics',
			'query': 'Apache Druid real-time analytics database'
		},
		{
			'name': 'AIM_Collision_Avoidance',
			'query': 'autonomous intersection collision avoidance algorithm'
		},
		{
			'name': 'Stream_Processing_Performance',
			'query': 'stream processing performance comparison PostgreSQL'
		}
	]

	# Search and save results
	results = await main_search(queries, max_results_per_query=5)

	# Generate summary report
	generate_report(results)


async def main_search(queries: list[dict], max_results_per_query: int = 5):
	"""Execute the multi-query search."""
	return await search_multiple_queries(queries, max_results_per_query)


def generate_report(results: dict):
	"""
	Generate a markdown report from search results.

	Args:
		results: Dictionary of search results
	"""
	output_dir = Path('./papers')
	report_file = output_dir / 'htll_aim_research_report.md'

	with open(report_file, 'w', encoding='utf-8') as f:
		f.write('# HTLL & AIM Research Paper Report\n\n')
		f.write('## 研究概要\n\n')
		f.write('この研究は、HTLLアーキテクチャ（High Throughput, Low Latency）を用いた')
		f.write('自律交差点管理システム（AIM: Autonomous Intersection Management）の')
		f.write('リアルタイムビッグデータ処理における有用性を検証するものです。\n\n')

		f.write('### 主要技術スタック\n\n')
		f.write('- **Apache Kafka**: 高スループットメッセージング\n')
		f.write('- **Apache Flink**: リアルタイムストリーム処理\n')
		f.write('- **Apache Druid**: リアルタイム分析データベース\n')
		f.write('- **V2X通信**: 車両間・路車間通信\n')
		f.write('- **FCFSアルゴリズム**: 先着順交差点制御\n\n')

		f.write('---\n\n')

		total_papers = 0
		for query_name, query_data in results.items():
			f.write(f'## {query_name.replace("_", " ")}\n\n')
			f.write(f'**検索クエリ**: `{query_data["query"]}`\n\n')
			f.write(f'**論文数**: {query_data["count"]}\n\n')

			if query_data['papers']:
				f.write('### 検索結果\n\n')
				for i, paper in enumerate(query_data['papers'], 1):
					f.write(f'#### {i}. {paper["title"]}\n\n')
					f.write(f'- **著者**: {", ".join(paper["authors"])}\n')
					f.write(f'- **URL**: [{paper["url"]}]({paper["url"]})\n\n')
					total_papers += 1

			f.write('---\n\n')

		f.write(f'\n## 統計\n\n')
		f.write(f'- **総検索クエリ数**: {len(results)}\n')
		f.write(f'- **総論文数**: {total_papers}\n')
		f.write(f'- **検索日時**: {asyncio.get_event_loop().time()}\n')

	logger.info(f'📝 Report generated: {report_file}')


if __name__ == '__main__':
	asyncio.run(main())
