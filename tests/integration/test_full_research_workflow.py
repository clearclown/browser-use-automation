"""
Integration tests for full research workflow
Tests the entire PRISMA-compliant research pipeline end-to-end
"""

import json

import pytest

from automated_research.arxiv_search import ArXivSearcher
from automated_research.government_documents_search import GovernmentDocumentsSearcher
from automated_research.jstage_search import JStageSearcher
from automated_research.multiple_reviewers import ReviewerManager, ScreeningDecision
from automated_research.prisma_flow_diagram import PRISMAFlowDiagram
from automated_research.prisma_search_strategy import PRISMASearchStrategyGenerator
from automated_research.risk_of_bias import RiskOfBiasAssessor
from automated_research.screening_criteria import ScreeningManager, generate_default_criteria


@pytest.fixture
def research_info():
	"""Sample research information"""
	return {
		'research_theme': 'AI in Healthcare',
		'research_field': 'Computer Science',
		'research_purpose': 'Systematic review of AI applications in medical diagnosis',
		'problem_statement': 'Need to understand current state of AI in healthcare',
		'specific_technologies': ['machine learning', 'deep learning', 'neural networks'],
	}


@pytest.fixture
def output_dir(tmp_path):
	"""Create output directory for integration test artifacts"""
	output = tmp_path / 'integration_test_output'
	output.mkdir()
	(output / 'data').mkdir()
	(output / 'reports').mkdir()
	return output


async def test_complete_workflow_structure(research_info, output_dir):
	"""Test the complete research workflow structure"""

	# Step 1: Generate search strategy
	strategy_gen = PRISMASearchStrategyGenerator()
	search_strategy = strategy_gen._generate_fallback_strategy(research_info)

	assert 'search_queries' in search_strategy
	assert len(search_strategy['search_queries']) > 0

	# Save strategy
	strategy_path = output_dir / 'data' / 'search_strategy.json'
	strategy_gen.save_search_strategy(search_strategy, strategy_path)
	assert strategy_path.exists()

	# Step 2: Generate screening criteria
	criteria = generate_default_criteria(research_info['research_field'], research_info['research_theme'])
	screening_manager = ScreeningManager(criteria=criteria)

	assert len(criteria.inclusion_criteria) > 0
	assert len(criteria.exclusion_criteria) > 0

	# Step 3: Search multiple databases (mock papers for integration test)
	mock_papers = [
		{
			'title': 'AI in Medical Imaging',
			'authors': ['Smith, J.', 'Doe, A.'],
			'year': 2023,
			'arxiv_id': '2301.12345',
			'source': 'arXiv',
		},
		{
			'title': 'Deep Learning for Diagnosis',
			'authors': ['Johnson, B.'],
			'year': 2022,
			'doi': '10.1234/test',
			'source': 'J-STAGE',
		},
		{'title': 'AI Policy in Healthcare', 'year': 2024, 'url': 'https://gov.example.com/ai', 'source': 'Government'},
	]

	# Step 4: Screen papers
	for i, paper in enumerate(mock_papers):
		record = screening_manager.screen_paper_automated(paper, screening_stage='title_abstract')
		screening_manager.add_record(record)

	screening_summary = screening_manager.get_screening_summary()
	assert screening_summary['total'] == len(mock_papers)

	# Step 5: Multiple reviewers
	reviewer_manager = ReviewerManager()
	reviewer_manager.add_reviewer('reviewer_1', 'Alice')
	reviewer_manager.add_reviewer('reviewer_2', 'Bob')

	for paper in mock_papers:
		paper_id = paper.get('arxiv_id') or paper.get('doi') or paper['title']
		reviewer_manager.record_decision(
			ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_1', decision='Include', reason='Relevant')
		)
		reviewer_manager.record_decision(
			ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_2', decision='Include', reason='Meets criteria')
		)

	consensus_papers = reviewer_manager.get_consensus_papers()
	assert len(consensus_papers) == len(mock_papers)

	# Step 6: Risk of bias assessment
	rob_assessor = RiskOfBiasAssessor()
	assessments = []

	for paper in mock_papers[:2]:  # Assess first 2 papers
		paper_id = paper.get('arxiv_id') or paper.get('doi') or paper['title']
		assessment = rob_assessor.create_blank_assessment(paper_id, paper['title'])

		# Assess all domains
		for domain_id in rob_assessor.domains.keys():
			rob_assessor.assess_domain(assessment, domain_id, 'Low', 'Well-designed study')

		overall = rob_assessor.calculate_overall_risk(assessment)
		assert overall == 'Low'
		assessments.append(assessment)

	# Save assessments
	for i, assessment in enumerate(assessments):
		assessment_path = output_dir / 'reports' / f'rob_assessment_{i}.json'
		rob_assessor.save_assessment(assessment, assessment_path)
		assert assessment_path.exists()

	# Step 7: Generate PRISMA flow diagram
	prisma_diagram = PRISMAFlowDiagram()

	# Add identification data
	prisma_diagram.add_database_results('arXiv', 1, '2024-10-18')
	prisma_diagram.add_database_results('J-STAGE', 1, '2024-10-18')
	prisma_diagram.add_database_results('Government Sources', 1, '2024-10-18')
	prisma_diagram.set_duplicates_removed(0)

	# Add screening data
	excluded = screening_summary.get('excluded', 0)
	if excluded > 0:
		prisma_diagram.add_screening_exclusion('Not relevant', excluded)

	# Set final included
	included = screening_summary.get('included', 0)
	prisma_diagram.set_final_included(studies=included)

	# Generate and save diagram
	mermaid_diagram = prisma_diagram.generate_mermaid_diagram()
	assert 'flowchart TD' in mermaid_diagram
	assert 'PRISMA 2020' in mermaid_diagram

	diagram_path = output_dir / 'reports' / 'prisma_flow_diagram.md'
	prisma_diagram.save_markdown_report(diagram_path)
	assert diagram_path.exists()

	# Verify the complete workflow produced expected outputs
	assert (output_dir / 'data' / 'search_strategy.json').exists()
	assert len(list((output_dir / 'reports').glob('rob_assessment_*.json'))) > 0
	assert (output_dir / 'reports' / 'prisma_flow_diagram.md').exists()


async def test_multi_database_integration(research_info):
	"""Test integration of multiple database searchers"""

	search_strategy = {
		'search_queries': ['AI AND healthcare'],
		'year_range': {'start': 2020, 'end': 2024},
	}

	# Initialize all searchers
	arxiv_searcher = ArXivSearcher()
	jstage_searcher = JStageSearcher()
	gov_searcher = GovernmentDocumentsSearcher()

	# All searchers should be initialized successfully
	assert arxiv_searcher is not None
	assert jstage_searcher is not None
	assert gov_searcher is not None

	# Verify they have compatible interfaces
	assert hasattr(arxiv_searcher, 'search')
	assert hasattr(jstage_searcher, 'search')
	assert hasattr(gov_searcher, 'search_all_sources')


async def test_reviewer_rob_integration(output_dir):
	"""Test integration between reviewer decisions and RoB assessment"""

	# Create reviewers and make decisions
	reviewer_manager = ReviewerManager()
	reviewer_manager.add_reviewer('reviewer_1', 'Alice')

	papers_to_assess = ['paper_001', 'paper_002', 'paper_003']

	for paper_id in papers_to_assess:
		reviewer_manager.record_decision(
			ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_1', decision='Include', reason='Quality study')
		)

	# Get included papers
	included_papers = [d.paper_id for d in reviewer_manager.decisions if d.decision == 'Include']
	assert len(included_papers) == 3

	# Perform RoB assessment on included papers
	rob_assessor = RiskOfBiasAssessor()
	rob_assessments = {}

	for paper_id in included_papers:
		assessment = rob_assessor.create_blank_assessment(paper_id, f'Title of {paper_id}')

		# Quick assessment
		for domain_id in list(rob_assessor.domains.keys())[:2]:  # Assess first 2 domains
			rob_assessor.assess_domain(assessment, domain_id, 'Some concerns', 'Unclear methodology')

		rob_assessments[paper_id] = assessment

	assert len(rob_assessments) == 3

	# Export reviewer decisions
	csv_path = output_dir / 'reviewer_decisions.csv'
	reviewer_manager.export_to_csv(csv_path)
	assert csv_path.exists()


async def test_screening_criteria_and_prisma_flow(research_info, output_dir):
	"""Test integration of screening criteria with PRISMA flow diagram"""

	# Generate criteria
	criteria = generate_default_criteria(research_info['research_field'], research_info['research_theme'])
	screening_manager = ScreeningManager(criteria=criteria)

	# Mock papers with varying characteristics
	test_papers = [
		{'title': 'AI in Healthcare 2023', 'year': 2023, 'language': 'English'},
		{'title': 'Old AI Study', 'year': 2015, 'language': 'English'},  # Will be excluded
		{'title': 'German AI Study', 'year': 2023, 'language': 'German'},  # Will be excluded
		{'title': 'Recent AI Research', 'year': 2024, 'language': 'English'},
		{'title': 'Another Recent Study', 'year': 2022, 'language': 'English'},
	]

	# Screen all papers
	for paper in test_papers:
		record = screening_manager.screen_paper_automated(paper)
		screening_manager.add_record(record)

	# Get summary
	summary = screening_manager.get_screening_summary()

	# Create PRISMA flow with actual screening data
	prisma_diagram = PRISMAFlowDiagram()
	prisma_diagram.add_database_results('Test Database', len(test_papers), '2024-10-18')
	prisma_diagram.set_duplicates_removed(0)

	# Add screening exclusions based on actual reasons
	for reason, count in summary['exclusion_reasons'].items():
		prisma_diagram.add_screening_exclusion(reason, count)

	prisma_diagram.set_final_included(studies=summary['included'])

	# Generate report
	report = prisma_diagram.generate_markdown_report()
	assert 'PRISMA 2020' in report
	assert str(summary['total']) in report
	assert str(summary['included']) in report

	# Save
	report_path = output_dir / 'integrated_prisma_report.md'
	prisma_diagram.save_markdown_report(report_path)
	assert report_path.exists()

	# Verify content
	with open(report_path) as f:
		content = f.read()
		assert 'Records Screened' in content
		assert 'Records Excluded' in content


async def test_complete_data_persistence(research_info, output_dir):
	"""Test that all data can be saved and loaded"""

	# Generate and save search strategy
	strategy_gen = PRISMASearchStrategyGenerator()
	strategy = strategy_gen._generate_fallback_strategy(research_info)
	strategy_path = output_dir / 'search_strategy.json'
	strategy_gen.save_search_strategy(strategy, strategy_path)

	# Generate and save screening criteria
	criteria = generate_default_criteria('Computer Science', 'AI Research')
	criteria_path = output_dir / 'screening_criteria.json'
	screening_manager = ScreeningManager(criteria=criteria)
	screening_manager.save_criteria(criteria_path)

	# Save RoB assessment
	rob_assessor = RiskOfBiasAssessor()
	assessment = rob_assessor.create_blank_assessment('test_paper', 'Test Paper Title')
	rob_assessor.assess_domain(assessment, list(rob_assessor.domains.keys())[0], 'Low', 'Good')
	rob_path = output_dir / 'rob_assessment.json'
	rob_assessor.save_assessment(assessment, rob_path)

	# Save PRISMA flow
	prisma = PRISMAFlowDiagram()
	prisma.add_database_results('Test DB', 10, '2024-10-18')
	prisma_data_path = output_dir / 'prisma_data.json'
	prisma.save_data(prisma_data_path)

	# Verify all files exist
	assert strategy_path.exists()
	assert criteria_path.exists()
	assert rob_path.exists()
	assert prisma_data_path.exists()

	# Load and verify
	with open(strategy_path) as f:
		loaded_strategy = json.load(f)
		assert 'search_queries' in loaded_strategy

	loaded_screening = ScreeningManager.load_criteria(criteria_path)
	assert len(loaded_screening.criteria.inclusion_criteria) > 0

	loaded_assessment = rob_assessor.load_assessment(rob_path)
	assert loaded_assessment.paper_id == 'test_paper'

	with open(prisma_data_path) as f:
		loaded_prisma = json.load(f)
		assert 'identification' in loaded_prisma
