"""
Tests for Risk of Bias assessment functionality
Based on Cochrane Risk of Bias tool (RoB 2)
TDD: Write tests first, then implement
"""

import pytest

from automated_research.risk_of_bias import RiskOfBiasAssessor


@pytest.fixture
def sample_paper():
	"""Sample paper for risk of bias assessment"""
	return {
		'title': 'Randomized Controlled Trial of AI in Healthcare',
		'abstract': 'This RCT evaluated the effectiveness of AI...',
		'year': 2023,
		'study_design': 'Randomized Controlled Trial',
	}


async def test_rob_assessor_initialization():
	"""Test that risk of bias assessor can be initialized"""
	assessor = RiskOfBiasAssessor()
	assert assessor is not None
	assert len(assessor.domains) > 0


async def test_get_assessment_domains():
	"""Test getting assessment domains (Cochrane RoB 2 domains)"""
	assessor = RiskOfBiasAssessor()
	domains = assessor.get_domains()

	assert isinstance(domains, list)
	assert len(domains) >= 5  # RoB 2 has 5 main domains

	# Check for standard RoB 2 domains
	domain_names = [d['name'] for d in domains]
	assert 'Randomization' in ' '.join(domain_names)
	assert 'Deviations' in ' '.join(domain_names) or 'Intervention' in ' '.join(domain_names)


async def test_create_blank_assessment():
	"""Test creating a blank assessment for a paper"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment(paper_id='paper_001', title='Test Paper')

	assert assessment.paper_id == 'paper_001'
	assert assessment.title == 'Test Paper'
	assert isinstance(assessment.domain_assessments, dict)  # Blank assessment starts empty


async def test_assess_domain():
	"""Test assessing a single domain"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment('paper_001', 'Test')

	# Assess randomization domain
	assessor.assess_domain(
		assessment=assessment,
		domain_id='randomization',
		rating='Low',
		rationale='Proper randomization sequence generation and allocation concealment',
	)

	domain_assessment = assessment.domain_assessments.get('randomization')
	assert domain_assessment is not None
	assert domain_assessment['rating'] == 'Low'
	assert 'randomization' in domain_assessment['rationale'].lower()


async def test_overall_risk_calculation():
	"""Test calculating overall risk of bias"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment('paper_001', 'Test')

	# Assess all domains as Low risk
	for domain_id in assessor.domains.keys():
		assessor.assess_domain(assessment, domain_id, 'Low', 'Good methodology')

	overall = assessor.calculate_overall_risk(assessment)
	assert overall == 'Low'

	# Change one to High risk
	first_domain = list(assessor.domains.keys())[0]
	assessor.assess_domain(assessment, first_domain, 'High', 'Major issues')

	overall = assessor.calculate_overall_risk(assessment)
	assert overall == 'High'  # Any High = overall High


async def test_risk_ratings_validation():
	"""Test that only valid risk ratings are accepted"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment('paper_001', 'Test')

	valid_ratings = ['Low', 'Some concerns', 'High']
	for rating in valid_ratings:
		# Should not raise
		assessor.assess_domain(assessment, list(assessor.domains.keys())[0], rating, 'Test')

	# Invalid rating should raise or be rejected
	try:
		assessor.assess_domain(assessment, list(assessor.domains.keys())[0], 'Invalid', 'Test')
		# If it doesn't raise, check it wasn't stored
		assert assessment.domain_assessments[list(assessor.domains.keys())[0]]['rating'] != 'Invalid'
	except (ValueError, KeyError):
		pass  # Expected


async def test_export_assessment_to_dict():
	"""Test exporting assessment to dictionary"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment('paper_001', 'Test Paper')

	assessor.assess_domain(assessment, list(assessor.domains.keys())[0], 'Low', 'Good')

	exported = assessment.to_dict()

	assert isinstance(exported, dict)
	assert 'paper_id' in exported
	assert 'domain_assessments' in exported
	assert 'overall_risk' in exported


async def test_save_load_assessment(tmp_path):
	"""Test saving and loading assessment"""
	assessor = RiskOfBiasAssessor()
	assessment = assessor.create_blank_assessment('paper_001', 'Test Paper')
	assessor.assess_domain(assessment, list(assessor.domains.keys())[0], 'Low', 'Good')

	# Save
	file_path = tmp_path / 'assessment.json'
	assessor.save_assessment(assessment, file_path)

	assert file_path.exists()

	# Load
	loaded = assessor.load_assessment(file_path)
	assert loaded.paper_id == 'paper_001'
	assert loaded.title == 'Test Paper'
