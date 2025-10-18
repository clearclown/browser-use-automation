"""
Risk of Bias assessment module
Based on Cochrane Risk of Bias tool (RoB 2)
"""

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class RiskOfBiasAssessment(BaseModel):
	"""Risk of bias assessment for a single study"""

	paper_id: str = Field(..., description='Unique identifier for the paper')
	title: str = Field(..., description='Paper title')
	domain_assessments: dict[str, dict[str, str]] = Field(default_factory=dict, description='Assessments for each domain')
	overall_risk: str | None = Field(None, description='Overall risk of bias')
	assessor_id: str = Field(default='automated', description='ID of the assessor')
	notes: str = Field(default='', description='Additional notes')

	model_config = {'extra': 'forbid'}

	def to_dict(self) -> dict[str, Any]:
		"""Export to dictionary"""
		return self.model_dump()


class RiskOfBiasAssessor:
	"""Assess risk of bias using Cochrane RoB 2 framework"""

	def __init__(self):
		self.domains = self._initialize_domains()
		self.valid_ratings = ['Low', 'Some concerns', 'High']

	def _initialize_domains(self) -> dict[str, dict[str, str]]:
		"""Initialize Cochrane RoB 2 domains"""
		return {
			'randomization': {
				'name': 'Randomization process',
				'description': 'Bias arising from the randomization process',
			},
			'deviations': {
				'name': 'Deviations from intended interventions',
				'description': 'Bias due to deviations from intended interventions',
			},
			'missing_data': {'name': 'Missing outcome data', 'description': 'Bias due to missing outcome data'},
			'outcome_measurement': {
				'name': 'Measurement of the outcome',
				'description': 'Bias in measurement of the outcome',
			},
			'selection_reporting': {
				'name': 'Selection of the reported result',
				'description': 'Bias in selection of the reported result',
			},
		}

	def get_domains(self) -> list[dict[str, str]]:
		"""Get list of assessment domains"""
		return list(self.domains.values())

	def create_blank_assessment(self, paper_id: str, title: str) -> RiskOfBiasAssessment:
		"""Create a blank assessment for a paper"""
		return RiskOfBiasAssessment(paper_id=paper_id, title=title, domain_assessments={})

	def assess_domain(self, assessment: RiskOfBiasAssessment, domain_id: str, rating: str, rationale: str) -> None:
		"""
		Assess a single domain

		Args:
			assessment: The assessment object
			domain_id: ID of the domain
			rating: Risk rating (Low, Some concerns, High)
			rationale: Justification for the rating
		"""
		if rating not in self.valid_ratings:
			raise ValueError(f'Invalid rating: {rating}. Must be one of {self.valid_ratings}')

		if domain_id not in self.domains:
			raise KeyError(f'Unknown domain: {domain_id}')

		assessment.domain_assessments[domain_id] = {'rating': rating, 'rationale': rationale}

	def calculate_overall_risk(self, assessment: RiskOfBiasAssessment) -> str:
		"""
		Calculate overall risk of bias

		RoB 2 algorithm:
		- High if any domain is High
		- Some concerns if any domain is Some concerns (and none are High)
		- Low only if all domains are Low
		"""
		if not assessment.domain_assessments:
			return 'Unknown'

		ratings = [d['rating'] for d in assessment.domain_assessments.values()]

		if 'High' in ratings:
			overall = 'High'
		elif 'Some concerns' in ratings:
			overall = 'Some concerns'
		else:
			overall = 'Low'

		assessment.overall_risk = overall
		return overall

	def save_assessment(self, assessment: RiskOfBiasAssessment, file_path: Path) -> None:
		"""Save assessment to JSON file"""
		file_path.parent.mkdir(parents=True, exist_ok=True)

		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump(assessment.to_dict(), f, indent=2, ensure_ascii=False)

		logger.info(f'Risk of bias assessment saved to: {file_path}')

	def load_assessment(self, file_path: Path) -> RiskOfBiasAssessment:
		"""Load assessment from JSON file"""
		with open(file_path, encoding='utf-8') as f:
			data = json.load(f)

		return RiskOfBiasAssessment(**data)
