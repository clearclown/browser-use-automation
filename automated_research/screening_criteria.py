"""
PRISMA Screening Criteria Manager
Manages inclusion/exclusion criteria for systematic literature review
"""

import json
import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ScreeningCriteria(BaseModel):
	"""Inclusion and exclusion criteria for PRISMA screening"""

	inclusion_criteria: list[str] = Field(default_factory=list, description='List of inclusion criteria for studies')
	exclusion_criteria: list[str] = Field(default_factory=list, description='List of exclusion criteria for studies')
	language_criteria: list[str] = Field(default_factory=lambda: ['English'], description='Accepted languages')
	year_range: dict[str, int] = Field(default_factory=lambda: {'start': 2018, 'end': 2024}, description='Publication year range')
	publication_types: list[str] = Field(
		default_factory=lambda: ['Journal Article', 'Conference Paper'],
		description='Accepted publication types',
	)
	study_designs: list[str] = Field(default_factory=list, description='Accepted study designs')

	model_config = {'extra': 'forbid'}


class ScreeningRecord(BaseModel):
	"""Record of a single paper screening decision"""

	paper_id: str = Field(..., description='Unique identifier for the paper')
	title: str = Field(..., description='Paper title')
	decision: str = Field(..., description='Include, Exclude, or Uncertain')
	exclusion_reason: str | None = Field(None, description='Reason for exclusion if excluded')
	screening_stage: str = Field(..., description='title_abstract or full_text')
	screener_id: str = Field(default='automated', description='ID of person/system who screened')
	notes: str | None = Field(None, description='Additional notes')

	model_config = {'extra': 'forbid'}


class ScreeningManager:
	"""Manages screening process and records"""

	def __init__(self, criteria: ScreeningCriteria | None = None):
		self.criteria = criteria or ScreeningCriteria()
		self.screening_records: list[ScreeningRecord] = []

	def add_record(self, record: ScreeningRecord) -> None:
		"""Add a screening record"""
		self.screening_records.append(record)

	def screen_paper_automated(self, paper: dict[str, Any], screening_stage: str = 'title_abstract') -> ScreeningRecord:
		"""
		Automatically screen a paper based on criteria

		Args:
			paper: Paper metadata dict with title, year, abstract, etc.
			screening_stage: 'title_abstract' or 'full_text'

		Returns:
			ScreeningRecord with decision
		"""
		paper_id = paper.get('doi') or paper.get('url') or paper.get('title', '')[:50]
		title = paper.get('title', '')
		year = paper.get('year')

		# Check year range
		if year:
			if year < self.criteria.year_range['start'] or year > self.criteria.year_range['end']:
				return ScreeningRecord(
					paper_id=paper_id,
					title=title,
					decision='Exclude',
					exclusion_reason=f'Outside year range ({self.criteria.year_range["start"]}-{self.criteria.year_range["end"]})',
					screening_stage=screening_stage,
				)

		# Check language (if available)
		language = paper.get('language', 'English')
		if language not in self.criteria.language_criteria:
			return ScreeningRecord(
				paper_id=paper_id,
				title=title,
				decision='Exclude',
				exclusion_reason=f'Language not in criteria: {language}',
				screening_stage=screening_stage,
			)

		# Check publication type (if available)
		pub_type = paper.get('publication_type')
		if pub_type and pub_type not in self.criteria.publication_types:
			return ScreeningRecord(
				paper_id=paper_id,
				title=title,
				decision='Exclude',
				exclusion_reason=f'Publication type not in criteria: {pub_type}',
				screening_stage=screening_stage,
			)

		# If all basic criteria passed, mark as Include
		# (In a real system, this would use LLM to check content relevance)
		return ScreeningRecord(
			paper_id=paper_id,
			title=title,
			decision='Include',
			exclusion_reason=None,
			screening_stage=screening_stage,
			notes='Passed automated screening criteria',
		)

	def get_screening_summary(self) -> dict[str, Any]:
		"""Get summary statistics of screening"""
		total = len(self.screening_records)
		if total == 0:
			return {'total': 0, 'included': 0, 'excluded': 0, 'uncertain': 0, 'exclusion_reasons': {}}

		included = sum(1 for r in self.screening_records if r.decision == 'Include')
		excluded = sum(1 for r in self.screening_records if r.decision == 'Exclude')
		uncertain = sum(1 for r in self.screening_records if r.decision == 'Uncertain')

		# Count exclusion reasons
		exclusion_reasons: dict[str, int] = {}
		for record in self.screening_records:
			if record.decision == 'Exclude' and record.exclusion_reason:
				reason = record.exclusion_reason
				exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1

		return {
			'total': total,
			'included': included,
			'excluded': excluded,
			'uncertain': uncertain,
			'exclusion_reasons': exclusion_reasons,
		}

	def save_criteria(self, output_path: Path) -> None:
		"""Save screening criteria to JSON"""
		output_path.parent.mkdir(parents=True, exist_ok=True)
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(self.criteria.model_dump(), f, indent=2, ensure_ascii=False)
		logger.info(f'Screening criteria saved to: {output_path}')

	def save_records(self, output_path: Path) -> None:
		"""Save screening records to JSON"""
		output_path.parent.mkdir(parents=True, exist_ok=True)
		records_data = [r.model_dump() for r in self.screening_records]
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump({'records': records_data, 'summary': self.get_screening_summary()}, f, indent=2, ensure_ascii=False)
		logger.info(f'Screening records saved to: {output_path}')

	@classmethod
	def load_criteria(cls, criteria_path: Path) -> 'ScreeningManager':
		"""Load screening criteria from JSON"""
		with open(criteria_path, encoding='utf-8') as f:
			data = json.load(f)
		criteria = ScreeningCriteria(**data)
		return cls(criteria=criteria)


def generate_default_criteria(research_field: str, research_theme: str) -> ScreeningCriteria:
	"""Generate default screening criteria based on research field"""
	# Base criteria that apply to most systematic reviews
	inclusion = [
		'Peer-reviewed publication (journal article or conference paper)',
		f'Directly addresses {research_theme}',
		'Reports original research or systematic review',
		'Provides empirical data or theoretical framework',
	]

	exclusion = [
		'Not peer-reviewed (blog posts, white papers, etc.)',
		'Not in English',
		'Outside specified publication year range',
		'Editorial, commentary, or opinion piece without original research',
		'Duplicate publication of same study',
	]

	# Field-specific additions
	if research_field.lower() in ['computer science', 'engineering', 'ai', 'machine learning']:
		inclusion.extend(['Describes methodology or algorithm clearly', 'Includes performance evaluation'])
		exclusion.append('Purely theoretical without implementation details')

	elif research_field.lower() in ['medicine', 'healthcare', 'biology']:
		inclusion.extend(['Describes study design and sample', 'Reports clinical or experimental outcomes'])
		exclusion.extend(['Case report with n<5', 'No ethical approval mentioned for human subjects'])

	return ScreeningCriteria(
		inclusion_criteria=inclusion,
		exclusion_criteria=exclusion,
		language_criteria=['English'],
		year_range={'start': 2018, 'end': 2024},
		publication_types=['Journal Article', 'Conference Paper'],
	)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	# Example usage
	criteria = generate_default_criteria('Computer Science', 'Transformer efficiency in NLP')

	manager = ScreeningManager(criteria=criteria)

	# Example papers to screen
	papers = [
		{'title': 'Efficient Transformers', 'year': 2023, 'language': 'English', 'publication_type': 'Conference Paper'},
		{'title': 'Old Study', 'year': 2015, 'language': 'English'},  # Will be excluded
		{'title': 'German Paper', 'year': 2023, 'language': 'German'},  # Will be excluded
	]

	for paper in papers:
		record = manager.screen_paper_automated(paper)
		manager.add_record(record)
		print(f'{paper["title"]}: {record.decision}')
		if record.exclusion_reason:
			print(f'  Reason: {record.exclusion_reason}')

	# Save results
	criteria_path = Path('automated_research/data/screening_criteria.json')
	records_path = Path('automated_research/data/screening_records.json')

	manager.save_criteria(criteria_path)
	manager.save_records(records_path)

	summary = manager.get_screening_summary()
	print(f'\nScreening Summary: {summary}')
