"""
Tests for multiple reviewers functionality
Supports independent screening by multiple reviewers with agreement calculation
TDD: Write tests first, then implement
"""

import pytest

from automated_research.multiple_reviewers import ReviewerManager, ScreeningDecision


@pytest.fixture
def sample_papers():
	"""Sample papers for screening"""
	return [
		{'id': 'paper_001', 'title': 'Paper 1'},
		{'id': 'paper_002', 'title': 'Paper 2'},
		{'id': 'paper_003', 'title': 'Paper 3'},
	]


async def test_reviewer_manager_initialization():
	"""Test that reviewer manager can be initialized"""
	manager = ReviewerManager()
	assert manager is not None
	assert len(manager.reviewers) == 0


async def test_add_reviewer():
	"""Test adding reviewers"""
	manager = ReviewerManager()
	manager.add_reviewer(reviewer_id='reviewer_1', name='Alice')
	manager.add_reviewer(reviewer_id='reviewer_2', name='Bob')

	assert len(manager.reviewers) == 2
	assert 'reviewer_1' in manager.reviewers
	assert manager.reviewers['reviewer_1']['name'] == 'Alice'


async def test_record_screening_decision():
	"""Test recording a screening decision"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')

	decision = ScreeningDecision(
		paper_id='paper_001', reviewer_id='reviewer_1', decision='Include', reason='Meets criteria'
	)

	manager.record_decision(decision)

	decisions = manager.get_decisions_for_paper('paper_001')
	assert len(decisions) == 1
	assert decisions[0].decision == 'Include'


async def test_multiple_reviewers_same_paper():
	"""Test multiple reviewers screening the same paper"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')
	manager.add_reviewer('reviewer_2', 'Bob')

	# Alice includes
	manager.record_decision(
		ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_1', decision='Include', reason='Good study')
	)

	# Bob excludes
	manager.record_decision(
		ScreeningDecision(
			paper_id='paper_001', reviewer_id='reviewer_2', decision='Exclude', reason='Poor methodology'
		)
	)

	decisions = manager.get_decisions_for_paper('paper_001')
	assert len(decisions) == 2


async def test_calculate_agreement_cohen_kappa():
	"""Test calculating Cohen's kappa for inter-rater agreement"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')
	manager.add_reviewer('reviewer_2', 'Bob')

	# Perfect agreement
	for paper_id in ['paper_001', 'paper_002', 'paper_003']:
		manager.record_decision(ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_1', decision='Include'))
		manager.record_decision(ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_2', decision='Include'))

	kappa = manager.calculate_cohen_kappa('reviewer_1', 'reviewer_2')
	assert kappa == 1.0  # Perfect agreement

	# Complete disagreement
	manager2 = ReviewerManager()
	manager2.add_reviewer('reviewer_1', 'Alice')
	manager2.add_reviewer('reviewer_2', 'Bob')

	for i, paper_id in enumerate(['paper_001', 'paper_002']):
		decision1 = 'Include' if i % 2 == 0 else 'Exclude'
		decision2 = 'Exclude' if i % 2 == 0 else 'Include'
		manager2.record_decision(ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_1', decision=decision1))
		manager2.record_decision(ScreeningDecision(paper_id=paper_id, reviewer_id='reviewer_2', decision=decision2))

	kappa2 = manager2.calculate_cohen_kappa('reviewer_1', 'reviewer_2')
	assert kappa2 < 0.5  # Low agreement


async def test_resolve_conflicts():
	"""Test conflict resolution between reviewers"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')
	manager.add_reviewer('reviewer_2', 'Bob')
	manager.add_reviewer('reviewer_3', 'Charlie')  # Third reviewer for tie-breaking

	# Conflicting decisions
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_1', decision='Include'))
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_2', decision='Exclude'))

	conflicts = manager.get_conflicts()
	assert len(conflicts) > 0
	assert 'paper_001' in [c['paper_id'] for c in conflicts]

	# Resolve with third reviewer
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_3', decision='Include'))
	resolved = manager.resolve_by_majority('paper_001')
	assert resolved == 'Include'  # 2 Include vs 1 Exclude


async def test_get_papers_by_consensus():
	"""Test getting papers that reached consensus"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')
	manager.add_reviewer('reviewer_2', 'Bob')

	# Consensus: Include
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_1', decision='Include'))
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_2', decision='Include'))

	# Conflict
	manager.record_decision(ScreeningDecision(paper_id='paper_002', reviewer_id='reviewer_1', decision='Include'))
	manager.record_decision(ScreeningDecision(paper_id='paper_002', reviewer_id='reviewer_2', decision='Exclude'))

	consensus_papers = manager.get_consensus_papers()
	assert 'paper_001' in consensus_papers
	assert 'paper_002' not in consensus_papers


async def test_export_decisions_to_csv(tmp_path):
	"""Test exporting decisions to CSV for analysis"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')
	manager.add_reviewer('reviewer_2', 'Bob')

	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_1', decision='Include'))
	manager.record_decision(ScreeningDecision(paper_id='paper_001', reviewer_id='reviewer_2', decision='Include'))

	csv_path = tmp_path / 'decisions.csv'
	manager.export_to_csv(csv_path)

	assert csv_path.exists()


async def test_screening_statistics():
	"""Test getting screening statistics"""
	manager = ReviewerManager()
	manager.add_reviewer('reviewer_1', 'Alice')

	for i in range(10):
		decision = 'Include' if i < 5 else 'Exclude'
		manager.record_decision(ScreeningDecision(paper_id=f'paper_{i:03d}', reviewer_id='reviewer_1', decision=decision))

	stats = manager.get_reviewer_statistics('reviewer_1')

	assert stats['total_screened'] == 10
	assert stats['included'] == 5
	assert stats['excluded'] == 5
