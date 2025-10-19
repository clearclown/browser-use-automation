"""
Tests for J-STAGE search functionality
J-STAGE is Japan's major academic publishing platform
TDD: Write tests first, then implement
"""

import pytest

from automated_research.jstage_search import JStageSearcher


@pytest.fixture
def sample_search_strategy():
	"""Sample search strategy for testing"""
	return {
		'primary_keywords': ['機械学習', 'トランスフォーマー'],
		'related_keywords': ['深層学習', 'attention'],
		'search_queries': [
			'機械学習 AND トランスフォーマー',
			'深層学習 OR attention',
		],
		'year_range': {'start': 2020, 'end': 2024},
	}


async def test_jstage_searcher_initialization():
	"""Test that J-STAGE searcher can be initialized"""
	searcher = JStageSearcher()
	assert searcher is not None
	assert 'jstage' in searcher.base_url.lower()


async def test_build_jstage_query():
	"""Test building J-STAGE search query"""
	searcher = JStageSearcher()
	query = searcher.build_jstage_query('機械学習 AND 深層学習')

	assert isinstance(query, dict)
	assert 'keyword' in query or 'text' in query


async def test_search_jstage_returns_papers(sample_search_strategy):
	"""Test that searching J-STAGE returns paper results"""
	searcher = JStageSearcher()
	papers = await searcher.search(search_strategy=sample_search_strategy, max_results=5)

	assert isinstance(papers, list)
	# May be empty if no results, but should be a list
	if len(papers) > 0:
		paper = papers[0]
		assert 'title' in paper
		assert 'authors' in paper
		assert 'url' in paper
		assert 'source' in paper
		assert paper['source'] == 'J-STAGE'


async def test_parse_jstage_article():
	"""Test parsing a J-STAGE article entry"""
	searcher = JStageSearcher()

	# Mock J-STAGE article structure
	mock_article = {
		'title': '深層学習による自然言語処理の研究',
		'authors': [{'name': '山田太郎'}, {'name': 'Taro Yamada'}],
		'journal': '情報処理学会論文誌',
		'year': 2023,
		'volume': '64',
		'issue': '3',
		'pages': '100-110',
		'doi': '10.2197/ipsjdc.2023.0001',
		'abstract': 'この研究では深層学習を用いた...',
		'url': 'https://www.jstage.jst.go.jp/article/ipsjdc/64/3/100',
	}

	paper = searcher.parse_article(mock_article)

	assert paper['title'] == '深層学習による自然言語処理の研究'
	assert len(paper['authors']) == 2
	assert '山田太郎' in paper['authors']
	assert paper['year'] == 2023
	assert paper['journal'] == '情報処理学会論文誌'
	assert paper['source'] == 'J-STAGE'


async def test_deduplicate_jstage_papers():
	"""Test deduplication of J-STAGE papers"""
	searcher = JStageSearcher()

	papers = [
		{'doi': '10.2197/test.001', 'title': 'Paper A'},
		{'doi': '10.2197/test.002', 'title': 'Paper B'},
		{'doi': '10.2197/test.001', 'title': 'Paper A'},  # Duplicate
		{'url': 'https://jstage.jst.go.jp/article/test/1/1', 'title': 'Paper C'},  # No DOI
	]

	unique = searcher.deduplicate_papers(papers)

	assert len(unique) == 3
	dois = [p.get('doi') for p in unique if p.get('doi')]
	assert len(dois) == len(set(dois))  # No duplicate DOIs


async def test_filter_japanese_content():
	"""Test filtering papers with Japanese content"""
	searcher = JStageSearcher()

	papers = [
		{'title': '日本語のタイトル', 'abstract': '日本語の要約'},
		{'title': 'English Title', 'abstract': 'English abstract'},
		{'title': '混合タイトル Mixed', 'abstract': '日本語含む contains Japanese'},
	]

	# Test detection of Japanese content
	has_japanese = [searcher.contains_japanese(p['title']) for p in papers]
	assert has_japanese == [True, False, True]


async def test_build_jstage_url():
	"""Test building J-STAGE article URL"""
	searcher = JStageSearcher()

	# From DOI
	doi = '10.2197/ipsjdc.2023.0001'
	url = searcher.build_article_url(doi=doi)
	assert 'jstage' in url.lower()
	assert doi in url or 'ipsjdc' in url

	# From article ID components
	url2 = searcher.build_article_url(journal='ipsjdc', volume='64', issue='3', page='100')
	assert 'jstage' in url2.lower()
	assert 'ipsjdc' in url2


async def test_search_with_japanese_query():
	"""Test searching with Japanese keywords"""
	searcher = JStageSearcher()

	strategy = {
		'search_queries': ['機械学習'],
		'year_range': {'start': 2020, 'end': 2024},
	}

	papers = await searcher.search(strategy, max_results=3)

	assert isinstance(papers, list)
	# Should handle Japanese queries without errors


async def test_extract_metadata_fields():
	"""Test extraction of J-STAGE specific metadata"""
	searcher = JStageSearcher()

	article = {
		'title': 'Test Article',
		'journal': 'Journal of Testing',
		'volume': '10',
		'issue': '5',
		'pages': '123-145',
		'year': 2023,
	}

	paper = searcher.parse_article(article)

	assert 'journal' in paper
	assert 'volume' in paper
	assert 'issue' in paper
	assert 'pages' in paper


async def test_handle_missing_fields():
	"""Test handling articles with missing fields"""
	searcher = JStageSearcher()

	minimal_article = {
		'title': 'Minimal Article',
	}

	paper = searcher.parse_article(minimal_article)

	assert paper['title'] == 'Minimal Article'
	assert 'authors' in paper
	assert isinstance(paper['authors'], list)
	assert 'source' in paper
