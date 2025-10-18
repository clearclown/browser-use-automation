"""
Tests for government documents search functionality
Supports multiple government sources: USA, Japan, EU, WHO, etc.
TDD: Write tests first, then implement
"""

import pytest

from automated_research.government_documents_search import GovernmentDocumentsSearcher


@pytest.fixture
def sample_search_strategy():
	"""Sample search strategy for testing"""
	return {
		'primary_keywords': ['AI policy', 'artificial intelligence'],
		'search_queries': [
			'AI policy AND regulation',
			'artificial intelligence AND governance',
		],
		'year_range': {'start': 2020, 'end': 2024},
	}


async def test_government_searcher_initialization():
	"""Test that government documents searcher can be initialized"""
	searcher = GovernmentDocumentsSearcher()
	assert searcher is not None
	assert len(searcher.sources) > 0
	assert 'usa_gov' in searcher.sources or 'japan_gov' in searcher.sources


async def test_get_available_sources():
	"""Test getting list of available government sources"""
	searcher = GovernmentDocumentsSearcher()
	sources = searcher.get_available_sources()

	assert isinstance(sources, list)
	assert len(sources) > 0

	# Check source structure
	if len(sources) > 0:
		source = sources[0]
		assert 'id' in source
		assert 'name' in source
		assert 'country' in source or 'organization' in source
		assert 'url' in source


async def test_search_usa_gov():
	"""Test searching USA government documents"""
	searcher = GovernmentDocumentsSearcher()

	# Mock search on USA.gov or relevant API
	documents = await searcher.search_source(
		source_id='usa_gov', query='artificial intelligence', max_results=5
	)

	assert isinstance(documents, list)
	if len(documents) > 0:
		doc = documents[0]
		assert 'title' in doc
		assert 'url' in doc
		assert 'source' in doc
		assert 'government' in doc['source'].lower() or 'usa' in doc['source'].lower()


async def test_search_japan_gov():
	"""Test searching Japanese government documents"""
	searcher = GovernmentDocumentsSearcher()

	documents = await searcher.search_source(
		source_id='japan_gov', query='人工知能', max_results=5
	)

	assert isinstance(documents, list)
	if len(documents) > 0:
		doc = documents[0]
		assert 'title' in doc
		assert 'url' in doc
		assert 'source' in doc


async def test_search_who():
	"""Test searching WHO (World Health Organization) documents"""
	searcher = GovernmentDocumentsSearcher()

	documents = await searcher.search_source(
		source_id='who', query='pandemic preparedness', max_results=5
	)

	assert isinstance(documents, list)
	if len(documents) > 0:
		doc = documents[0]
		assert 'title' in doc
		assert 'url' in doc
		assert 'who' in doc['source'].lower() or 'health' in doc['source'].lower()


async def test_search_all_sources(sample_search_strategy):
	"""Test searching across all available government sources"""
	searcher = GovernmentDocumentsSearcher()

	documents = await searcher.search_all_sources(
		search_strategy=sample_search_strategy, max_results_per_source=3
	)

	assert isinstance(documents, list)
	# May be empty, but should be a list
	if len(documents) > 0:
		doc = documents[0]
		assert 'title' in doc
		assert 'source' in doc
		assert 'url' in doc


async def test_parse_government_document():
	"""Test parsing a government document entry"""
	searcher = GovernmentDocumentsSearcher()

	mock_document = {
		'title': 'National AI Strategy 2024',
		'url': 'https://www.gov.example.com/ai-strategy-2024',
		'published_date': '2024-03-15',
		'agency': 'Department of Technology',
		'country': 'USA',
		'document_type': 'Policy Paper',
		'abstract': 'This document outlines...',
	}

	parsed = searcher.parse_document(mock_document)

	assert parsed['title'] == 'National AI Strategy 2024'
	assert parsed['year'] == 2024
	assert 'gov' in parsed['source'].lower() or 'department' in parsed['source'].lower()
	assert parsed['document_type'] == 'Policy Paper'


async def test_detect_document_type():
	"""Test automatic detection of government document types"""
	searcher = GovernmentDocumentsSearcher()

	test_cases = [
		('Executive Order on AI', 'Executive Order'),
		('Annual Report FY2024', 'Report'),
		('Public Comment on Regulation', 'Public Comment'),
		('Congressional Hearing Transcript', 'Hearing'),
		('White Paper: AI Governance', 'White Paper'),
	]

	for title, expected_type in test_cases:
		detected = searcher.detect_document_type(title)
		assert expected_type.lower() in detected.lower()


async def test_filter_by_document_type():
	"""Test filtering documents by type"""
	searcher = GovernmentDocumentsSearcher()

	documents = [
		{'title': 'Report on AI', 'document_type': 'Report'},
		{'title': 'Executive Order', 'document_type': 'Executive Order'},
		{'title': 'Another Report', 'document_type': 'Report'},
		{'title': 'Policy Paper', 'document_type': 'Policy Paper'},
	]

	reports_only = searcher.filter_by_type(documents, ['Report'])
	assert len(reports_only) == 2
	assert all(d['document_type'] == 'Report' for d in reports_only)


async def test_deduplicate_government_docs():
	"""Test deduplication of government documents"""
	searcher = GovernmentDocumentsSearcher()

	documents = [
		{'url': 'https://gov.example/doc1', 'title': 'Doc 1'},
		{'url': 'https://gov.example/doc2', 'title': 'Doc 2'},
		{'url': 'https://gov.example/doc1', 'title': 'Doc 1'},  # Duplicate
	]

	unique = searcher.deduplicate_documents(documents)
	assert len(unique) == 2


async def test_extract_agency_from_url():
	"""Test extracting government agency from URL"""
	searcher = GovernmentDocumentsSearcher()

	test_cases = [
		('https://www.whitehouse.gov/ai-policy/', 'White House'),
		('https://www.fda.gov/medical-devices/ai', 'FDA'),
		('https://www.mhlw.go.jp/content/ai.pdf', 'MHLW'),  # Japan Ministry
	]

	for url, expected_agency in test_cases:
		agency = searcher.extract_agency(url)
		assert expected_agency.lower() in agency.lower()


async def test_build_source_metadata():
	"""Test building metadata for government sources"""
	searcher = GovernmentDocumentsSearcher()

	sources = searcher.get_available_sources()
	assert len(sources) > 0

	for source in sources:
		assert 'id' in source
		assert 'name' in source
		assert 'url' in source
		# Should have either country or organization
		assert 'country' in source or 'organization' in source


async def test_multiCountry_support():
	"""Test that searcher supports multiple countries"""
	searcher = GovernmentDocumentsSearcher()

	countries = searcher.get_supported_countries()
	assert isinstance(countries, list)
	assert len(countries) >= 2  # At least USA and Japan

	# Common countries
	expected_countries = ['USA', 'Japan', 'EU', 'UK']
	for country in expected_countries:
		# At least some of these should be supported
		pass  # Just check it returns a list


async def test_search_with_date_range():
	"""Test searching with date range filtering"""
	searcher = GovernmentDocumentsSearcher()

	strategy = {
		'search_queries': ['AI policy'],
		'year_range': {'start': 2022, 'end': 2024},
	}

	documents = await searcher.search_all_sources(strategy, max_results_per_source=3)

	assert isinstance(documents, list)
	# If documents are returned, they should be within date range
	for doc in documents:
		if 'year' in doc and doc['year']:
			assert 2022 <= doc['year'] <= 2024
