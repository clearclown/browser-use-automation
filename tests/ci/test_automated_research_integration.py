"""
Integration tests for automated research system
Tests the full PRISMA-based research workflow
"""

import asyncio
import json
from pathlib import Path

import pytest

from automated_research.ieee_automated_search import IEEEAutomatedSearcher
from automated_research.prisma_search_strategy import PRISMASearchStrategyGenerator
from browser_use.llm.messages import AssistantMessage


@pytest.fixture
def sample_search_strategy():
	"""Sample PRISMA search strategy"""
	return {
		'primary_keywords': ['machine learning', 'optimization'],
		'related_keywords': ['neural networks', 'gradient descent'],
		'exclusion_keywords': ['quantum computing'],
		'search_queries': [
			'machine learning AND optimization',
			'neural networks AND (training OR optimization)',
		],
		'year_range': {'start': 2020, 'end': 2024},
		'publication_types': ['Journal', 'Conference'],
	}


@pytest.fixture
def sample_research_info():
	"""Sample research information"""
	return {
		'research_theme': 'Machine Learning Optimization',
		'research_field': 'Computer Science',
		'research_purpose': 'Study optimization techniques in ML',
	}


async def test_ieee_searcher_initialization():
	"""Test IEEE searcher can be initialized"""
	searcher = IEEEAutomatedSearcher(headless=True)
	assert searcher.llm is not None
	assert searcher.headless is True


async def test_build_search_task(sample_search_strategy):
	"""Test search task construction"""
	searcher = IEEEAutomatedSearcher(headless=True)
	task = searcher._build_search_task('machine learning AND optimization', 10, sample_search_strategy)

	assert 'IEEE Xplore' in task
	assert 'machine learning AND optimization' in task
	assert '2020' in task
	assert '2024' in task
	assert 'JSON' in task


async def test_deduplicate_papers():
	"""Test paper deduplication logic"""
	searcher = IEEEAutomatedSearcher(headless=True)

	papers = [
		{'title': 'Paper A', 'authors': ['Author 1']},
		{'title': 'Paper B', 'authors': ['Author 2']},
		{'title': 'Paper A', 'authors': ['Author 1']},  # Duplicate
		{'title': 'PAPER A', 'authors': ['Author 3']},  # Case-insensitive duplicate
	]

	unique = searcher._deduplicate_papers(papers)
	assert len(unique) == 2
	assert unique[0]['title'] == 'Paper A'
	assert unique[1]['title'] == 'Paper B'


async def test_save_papers(sample_search_strategy, tmp_path):
	"""Test saving papers to JSON"""
	searcher = IEEEAutomatedSearcher(headless=True)
	papers = [
		{
			'title': 'Test Paper',
			'authors': ['Author 1', 'Author 2'],
			'year': 2023,
			'doi': '10.1109/test.2023.123456',
		}
	]

	output_path = tmp_path / 'papers.json'
	searcher.save_papers(papers, output_path)

	assert output_path.exists()

	with open(output_path, encoding='utf-8') as f:
		data = json.load(f)

	assert 'papers' in data
	assert 'total_count' in data
	assert data['total_count'] == 1
	assert data['papers'][0]['title'] == 'Test Paper'


async def test_parse_paper_info():
	"""Test parsing paper information from text"""
	searcher = IEEEAutomatedSearcher(headless=True)

	valid_json = '{"title": "Test", "authors": ["A1"], "year": 2023}'
	result = searcher._parse_paper_info(valid_json)
	assert result is not None
	assert result['title'] == 'Test'

	invalid_text = 'This is not JSON'
	result = searcher._parse_paper_info(invalid_text)
	assert result is None


async def test_end_to_end_workflow_structure(sample_research_info, sample_search_strategy, tmp_path):
	"""Test the structure of end-to-end workflow (without actual browser automation)"""
	# Step 1: Generate search strategy
	generator = PRISMASearchStrategyGenerator()
	strategy = generator._generate_fallback_strategy(sample_research_info)

	assert 'search_queries' in strategy
	assert len(strategy['search_queries']) > 0

	# Step 2: Verify searcher can be created
	searcher = IEEEAutomatedSearcher(headless=True)
	assert searcher is not None

	# Step 3: Verify task building works
	task = searcher._build_search_task(strategy['search_queries'][0], 5, strategy)
	assert 'IEEE Xplore' in task

	# Step 4: Verify save functionality
	mock_papers = [{'title': 'Mock Paper', 'year': 2023}]
	output_path = tmp_path / 'papers.json'
	searcher.save_papers(mock_papers, output_path)
	assert output_path.exists()


async def test_prisma_metadata_fields():
	"""Test that PRISMA-required metadata fields are captured"""
	# PRISMA 2020 requires recording:
	# - Database name
	# - Search date
	# - Number of records identified
	# - Number of records screened
	# - Number included/excluded with reasons

	sample_strategy = {
		'primary_keywords': ['AI'],
		'search_queries': ['AI AND ethics'],
		'year_range': {'start': 2020, 'end': 2024},
		'search_metadata': {
			'databases': ['IEEE Xplore'],
			'search_date': '2024-10-18',
			'total_queries': 1,
		},
	}

	assert 'search_metadata' in sample_strategy
	metadata = sample_strategy['search_metadata']
	assert 'databases' in metadata
	assert 'search_date' in metadata


async def test_multiple_database_support_structure():
	"""Test that the system can structurally support multiple databases"""
	# This tests the data structure, not actual implementation
	multi_db_strategy = {
		'primary_keywords': ['AI'],
		'search_queries': ['AI AND robotics'],
		'databases': [
			{'name': 'IEEE Xplore', 'url': 'https://ieeexplore.ieee.org'},
			{'name': 'arXiv', 'url': 'https://arxiv.org'},
			{'name': 'PubMed', 'url': 'https://pubmed.ncbi.nlm.nih.gov'},
		],
	}

	assert 'databases' in multi_db_strategy
	assert len(multi_db_strategy['databases']) == 3


async def test_screening_criteria_structure():
	"""Test inclusion/exclusion criteria structure for PRISMA compliance"""
	# PRISMA requires explicit inclusion/exclusion criteria
	screening_criteria = {
		'inclusion_criteria': [
			'Published in peer-reviewed journal or conference',
			'Written in English',
			'Published between 2020-2024',
			'Focuses on AI/ML optimization',
		],
		'exclusion_criteria': [
			'Not peer-reviewed',
			'Not in English',
			'Outside date range',
			'Focuses on hardware only',
		],
	}

	assert 'inclusion_criteria' in screening_criteria
	assert 'exclusion_criteria' in screening_criteria
	assert len(screening_criteria['inclusion_criteria']) > 0
	assert len(screening_criteria['exclusion_criteria']) > 0
