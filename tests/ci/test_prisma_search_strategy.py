"""
Tests for PRISMA search strategy generation
"""

import json
from pathlib import Path

import pytest

from automated_research.prisma_search_strategy import PRISMASearchStrategyGenerator
from browser_use.llm.messages import AssistantMessage
from browser_use.llm.openai.chat import ChatOpenAI


@pytest.fixture
def sample_research_info():
	"""Sample research information for testing"""
	return {
		'research_theme': 'Transformer efficiency in NLP',
		'research_field': 'Natural Language Processing',
		'research_purpose': 'Improve computational efficiency of transformer models',
		'problem_statement': 'Transformers consume too much memory and compute',
		'specific_technologies': ['BERT', 'GPT', 'attention mechanisms'],
		'additional_context': 'Focus on recent architectures from 2020 onwards',
		'known_papers': ['Attention is All You Need'],
	}


@pytest.fixture
def mock_llm_response():
	"""Mock LLM response with valid PRISMA search strategy"""
	return AssistantMessage(
		content="""```json
{
	"primary_keywords": ["transformer", "attention mechanism", "natural language processing"],
	"related_keywords": ["BERT", "GPT", "efficiency", "optimization", "compression"],
	"exclusion_keywords": ["image processing", "computer vision"],
	"search_queries": [
		"(transformer OR attention) AND (efficiency OR optimization) AND NLP",
		"BERT AND (compression OR pruning OR quantization)",
		"GPT AND (inference speed OR memory reduction)"
	],
	"year_range": {"start": 2020, "end": 2024},
	"publication_types": ["Journal", "Conference"],
	"search_metadata": {
		"databases": ["IEEE Xplore"],
		"search_date": "2024-10-18",
		"total_queries": 3
	}
}
```"""
	)


async def test_prisma_generator_initialization():
	"""Test PRISMA search strategy generator can be initialized"""
	generator = PRISMASearchStrategyGenerator()
	assert generator.llm is not None
	assert isinstance(generator.llm, ChatOpenAI)


async def test_generate_search_strategy_with_mock(sample_research_info, mock_llm_response, mock_llm):
	"""Test search strategy generation with mocked LLM"""
	# Use the mock_llm fixture from conftest.py
	async def mock_get_response(messages):
		return mock_llm_response

	mock_llm.get_response = mock_get_response

	generator = PRISMASearchStrategyGenerator(llm=mock_llm)
	strategy = await generator.generate_search_strategy(sample_research_info)

	# Verify structure
	assert 'primary_keywords' in strategy
	assert 'related_keywords' in strategy
	assert 'exclusion_keywords' in strategy
	assert 'search_queries' in strategy
	assert 'year_range' in strategy
	assert 'publication_types' in strategy

	# Verify content
	assert len(strategy['primary_keywords']) > 0
	assert len(strategy['search_queries']) > 0
	assert 'start' in strategy['year_range']
	assert 'end' in strategy['year_range']


async def test_format_research_context(sample_research_info):
	"""Test research context formatting"""
	generator = PRISMASearchStrategyGenerator()
	context = generator._format_research_context(sample_research_info)

	assert 'Transformer efficiency in NLP' in context
	assert 'Natural Language Processing' in context
	assert 'BERT' in context
	assert 'Attention is All You Need' in context


async def test_generate_fallback_strategy(sample_research_info):
	"""Test fallback strategy generation when LLM fails"""
	generator = PRISMASearchStrategyGenerator()
	strategy = generator._generate_fallback_strategy(sample_research_info)

	assert isinstance(strategy, dict)
	assert 'primary_keywords' in strategy
	assert 'search_queries' in strategy
	assert len(strategy['search_queries']) > 0


async def test_save_search_strategy(sample_research_info, tmp_path):
	"""Test saving search strategy to JSON file"""
	generator = PRISMASearchStrategyGenerator()
	strategy = generator._generate_fallback_strategy(sample_research_info)

	output_path = tmp_path / 'test_strategy.json'
	generator.save_search_strategy(strategy, output_path)

	assert output_path.exists()

	# Verify content
	with open(output_path, encoding='utf-8') as f:
		loaded = json.load(f)
	assert loaded == strategy


async def test_display_search_strategy_no_crash(sample_research_info, capsys):
	"""Test that displaying search strategy doesn't crash"""
	generator = PRISMASearchStrategyGenerator()
	strategy = generator._generate_fallback_strategy(sample_research_info)

	# Should not raise
	generator._display_search_strategy(strategy)

	captured = capsys.readouterr()
	assert '主要キーワード' in captured.out or 'primary_keywords' in str(strategy)


async def test_search_strategy_with_minimal_research_info():
	"""Test with minimal research information"""
	minimal_info = {
		'research_theme': 'AI safety',
	}

	generator = PRISMASearchStrategyGenerator()
	strategy = generator._generate_fallback_strategy(minimal_info)

	assert 'primary_keywords' in strategy
	assert 'AI safety' in strategy['primary_keywords']


async def test_search_queries_use_boolean_operators(sample_research_info, mock_llm_response, mock_llm):
	"""Test that search queries use proper Boolean operators"""
	async def mock_get_response(messages):
		return mock_llm_response

	mock_llm.get_response = mock_get_response

	generator = PRISMASearchStrategyGenerator(llm=mock_llm)
	strategy = await generator.generate_search_strategy(sample_research_info)

	# Check that queries contain Boolean operators
	queries = strategy['search_queries']
	assert any('AND' in query or 'OR' in query for query in queries)


async def test_year_range_validation(sample_research_info, mock_llm_response, mock_llm):
	"""Test that year range is reasonable"""
	async def mock_get_response(messages):
		return mock_llm_response

	mock_llm.get_response = mock_get_response

	generator = PRISMASearchStrategyGenerator(llm=mock_llm)
	strategy = await generator.generate_search_strategy(sample_research_info)

	year_range = strategy['year_range']
	assert year_range['start'] <= year_range['end']
	assert year_range['start'] >= 1900
	assert year_range['end'] <= 2030
