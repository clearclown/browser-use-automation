"""
Multiple reviewers module
Supports independent screening by multiple reviewers with agreement calculation
"""

import csv
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ScreeningDecision(BaseModel):
	"""A single screening decision by a reviewer"""

	paper_id: str = Field(..., description='Paper identifier')
	reviewer_id: str = Field(..., description='Reviewer identifier')
	decision: str = Field(..., description='Include, Exclude, or Uncertain')
	reason: str = Field(default='', description='Reason for the decision')

	model_config = {'extra': 'forbid'}


class ReviewerManager:
	"""Manage multiple reviewers and their screening decisions"""

	def __init__(self):
		self.reviewers: dict[str, dict[str, str]] = {}
		self.decisions: list[ScreeningDecision] = []

	def add_reviewer(self, reviewer_id: str, name: str) -> None:
		"""Add a reviewer"""
		self.reviewers[reviewer_id] = {'id': reviewer_id, 'name': name}
		logger.info(f'Added reviewer: {name} ({reviewer_id})')

	def record_decision(self, decision: ScreeningDecision) -> None:
		"""Record a screening decision"""
		self.decisions.append(decision)

	def get_decisions_for_paper(self, paper_id: str) -> list[ScreeningDecision]:
		"""Get all decisions for a specific paper"""
		return [d for d in self.decisions if d.paper_id == paper_id]

	def calculate_cohen_kappa(self, reviewer1_id: str, reviewer2_id: str) -> float:
		"""
		Calculate Cohen's kappa for inter-rater agreement

		Args:
			reviewer1_id: ID of first reviewer
			reviewer2_id: ID of second reviewer

		Returns:
			Cohen's kappa coefficient (-1 to 1)
		"""
		# Get papers reviewed by both
		r1_decisions = {d.paper_id: d.decision for d in self.decisions if d.reviewer_id == reviewer1_id}
		r2_decisions = {d.paper_id: d.decision for d in self.decisions if d.reviewer_id == reviewer2_id}

		common_papers = set(r1_decisions.keys()) & set(r2_decisions.keys())

		if not common_papers:
			return 0.0

		# Calculate agreement
		agreements = sum(1 for pid in common_papers if r1_decisions[pid] == r2_decisions[pid])
		total = len(common_papers)

		observed_agreement = agreements / total

		# Calculate expected agreement (simplified, assumes binary decision)
		r1_include_rate = sum(1 for pid in common_papers if r1_decisions[pid] == 'Include') / total
		r2_include_rate = sum(1 for pid in common_papers if r2_decisions[pid] == 'Include') / total

		expected_agreement = r1_include_rate * r2_include_rate + (1 - r1_include_rate) * (1 - r2_include_rate)

		# Cohen's kappa
		if expected_agreement == 1:
			return 1.0

		kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)
		return kappa

	def get_conflicts(self) -> list[dict[str, Any]]:
		"""Get papers with conflicting decisions"""
		conflicts = []
		papers = {d.paper_id for d in self.decisions}

		for paper_id in papers:
			decisions = self.get_decisions_for_paper(paper_id)
			if len(decisions) < 2:
				continue

			# Check if all decisions agree
			unique_decisions = {d.decision for d in decisions}
			if len(unique_decisions) > 1:
				conflicts.append(
					{'paper_id': paper_id, 'decisions': [d.model_dump() for d in decisions], 'reviewers': len(decisions)}
				)

		return conflicts

	def resolve_by_majority(self, paper_id: str) -> str | None:
		"""Resolve conflicts by majority vote"""
		decisions = self.get_decisions_for_paper(paper_id)

		if not decisions:
			return None

		# Count votes
		vote_counts: dict[str, int] = {}
		for decision in decisions:
			vote_counts[decision.decision] = vote_counts.get(decision.decision, 0) + 1

		# Find majority
		max_votes = max(vote_counts.values())
		majority_decisions = [dec for dec, count in vote_counts.items() if count == max_votes]

		if len(majority_decisions) == 1:
			return majority_decisions[0]

		# Tie - could implement tie-breaking logic
		return None

	def get_consensus_papers(self) -> list[str]:
		"""Get papers where all reviewers agreed"""
		consensus_papers = []
		papers = {d.paper_id for d in self.decisions}

		for paper_id in papers:
			decisions = self.get_decisions_for_paper(paper_id)
			if len(decisions) < 2:
				continue

			# Check if all agree
			unique_decisions = {d.decision for d in decisions}
			if len(unique_decisions) == 1:
				consensus_papers.append(paper_id)

		return consensus_papers

	def export_to_csv(self, file_path: Path) -> None:
		"""Export all decisions to CSV"""
		file_path.parent.mkdir(parents=True, exist_ok=True)

		with open(file_path, 'w', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(['paper_id', 'reviewer_id', 'decision', 'reason'])

			for decision in self.decisions:
				writer.writerow([decision.paper_id, decision.reviewer_id, decision.decision, decision.reason])

		logger.info(f'Decisions exported to: {file_path}')

	def get_reviewer_statistics(self, reviewer_id: str) -> dict[str, int]:
		"""Get screening statistics for a reviewer"""
		reviewer_decisions = [d for d in self.decisions if d.reviewer_id == reviewer_id]

		stats = {
			'total_screened': len(reviewer_decisions),
			'included': sum(1 for d in reviewer_decisions if d.decision == 'Include'),
			'excluded': sum(1 for d in reviewer_decisions if d.decision == 'Exclude'),
			'uncertain': sum(1 for d in reviewer_decisions if d.decision == 'Uncertain'),
		}

		return stats
