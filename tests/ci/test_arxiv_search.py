"""
Tests for arXiv search functionality
TDD: Write tests first, then implement
"""

import pytest

from automated_research.arxiv_search import ArXivSearcher


@pytest.fixture
def sample_search_strategy():
	"""Sample search strategy for testing"""
	return {
		'primary_keywords': ['machine learning', 'transformer'],
		'related_keywords': ['neural network', 'attention'],
		'search_queries': [
			'machine learning AND transformer',
			'neural network AND attention mechanism',
		],
		'year_range': {'start': 2020, 'end': 2024},
	}


async def test_arxiv_searcher_initialization():
	"""Test that ArXiv searcher can be initialized"""
	searcher = ArXivSearcher()
	assert searcher is not None
	assert searcher.base_url == 'http://export.arxiv.org/api/query'


async def test_build_arxiv_query():
	"""Test building arXiv API query from search strategy"""
	searcher = ArXivSearcher()
	query = searcher.build_arxiv_query('machine learning AND transformer', year_start=2020, year_end=2024)

	assert 'machine learning' in query.lower()
	assert 'transformer' in query.lower()
	assert isinstance(query, str)


async def test_search_arxiv_returns_papers(sample_search_strategy):
	"""Test that searching arXiv returns paper results"""
	searcher = ArXivSearcher()
	papers = await searcher.search(search_strategy=sample_search_strategy, max_results=5)

	assert isinstance(papers, list)
	# May be empty if no results, but should be a list
	if len(papers) > 0:
		paper = papers[0]
		assert 'title' in paper
		assert 'authors' in paper
		assert 'abstract' in paper
		assert 'arxiv_id' in paper
		assert 'url' in paper
		assert 'published_date' in paper


async def test_parse_arxiv_entry():
	"""Test parsing a single arXiv entry"""
	searcher = ArXivSearcher()

	# Mock arXiv entry structure
	mock_entry = {
		'id': 'http://arxiv.org/abs/2301.12345v1',
		'title': 'Test Paper Title',
		'summary': 'This is a test abstract',
		'published': '2023-01-15T12:00:00Z',
		'updated': '2023-01-16T12:00:00Z',
		'authors': [
			{'name': 'Author One'},
			{'name': 'Author Two'},
		],
		'primary_category': {'term': 'cs.LG'},
		'categories': [{'term': 'cs.LG'}, {'term': 'cs.AI'}],
		'links': [
			{'href': 'http://arxiv.org/abs/2301.12345v1', 'rel': 'alternate'},
			{'href': 'http://arxiv.org/pdf/2301.12345v1', 'rel': 'related', 'type': 'application/pdf'},
		],
	}

	paper = searcher.parse_entry(mock_entry)

	assert paper['title'] == 'Test Paper Title'
	assert paper['abstract'] == 'This is a test abstract'
	assert paper['arxiv_id'] == '2301.12345'
	assert len(paper['authors']) == 2
	assert 'Author One' in paper['authors']
	assert paper['year'] == 2023
	assert 'cs.LG' in paper['categories']


async def test_deduplicate_arxiv_papers():
	"""Test deduplication of arXiv papers"""
	searcher = ArXivSearcher()

	papers = [
		{'arxiv_id': '2301.12345', 'title': 'Paper A'},
		{'arxiv_id': '2301.67890', 'title': 'Paper B'},
		{'arxiv_id': '2301.12345', 'title': 'Paper A'},  # Duplicate
	]

	unique = searcher.deduplicate_papers(papers)

	assert len(unique) == 2
	assert unique[0]['arxiv_id'] == '2301.12345'
	assert unique[1]['arxiv_id'] == '2301.67890'


async def test_filter_by_year():
	"""Test filtering papers by publication year"""
	searcher = ArXivSearcher()

	papers = [
		{'arxiv_id': '2301.001', 'year': 2023, 'title': 'Recent Paper'},
		{'arxiv_id': '1801.001', 'year': 2018, 'title': 'Old Paper'},
		{'arxiv_id': '2401.001', 'year': 2024, 'title': 'Very Recent Paper'},
	]

	filtered = searcher.filter_by_year(papers, year_start=2020, year_end=2024)

	assert len(filtered) == 2
	assert all(2020 <= p['year'] <= 2024 for p in filtered)


async def test_search_with_multiple_queries(sample_search_strategy):
	"""Test searching with multiple queries and combining results"""
	searcher = ArXivSearcher()

	# This should handle multiple queries from the strategy
	papers = await searcher.search(search_strategy=sample_search_strategy, max_results=3)

	assert isinstance(papers, list)
	# Results should be deduplicated
	if len(papers) > 1:
		arxiv_ids = [p['arxiv_id'] for p in papers]
		assert len(arxiv_ids) == len(set(arxiv_ids))  # No duplicates


async def test_extract_arxiv_id():
	"""Test extracting arXiv ID from various URL formats"""
	searcher = ArXivSearcher()

	test_cases = [
		('http://arxiv.org/abs/2301.12345v1', '2301.12345'),
		('https://arxiv.org/abs/2301.12345', '2301.12345'),
		('http://arxiv.org/abs/1234.5678v2', '1234.5678'),
		('2301.12345', '2301.12345'),  # Already clean
	]

	for input_id, expected in test_cases:
		result = searcher.extract_arxiv_id(input_id)
		assert result == expected


async def test_build_pdf_url():
	"""Test building PDF URL from arXiv ID"""
	searcher = ArXivSearcher()

	arxiv_id = '2301.12345'
	pdf_url = searcher.build_pdf_url(arxiv_id)

	assert 'pdf' in pdf_url
	assert '2301.12345' in pdf_url
	assert pdf_url.startswith('http')
