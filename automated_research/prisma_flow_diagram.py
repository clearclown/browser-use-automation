"""
PRISMA 2020 Flow Diagram Generator
Generates a PRISMA flow diagram from search and screening data
"""

import json
from datetime import datetime
from pathlib import Path


class PRISMAFlowDiagram:
	"""Generate PRISMA 2020 compliant flow diagram"""

	def __init__(self):
		self.data = {
			'identification': {
				'databases': {},
				'other_sources': {},
				'total_identified': 0,
				'duplicates_removed': 0,
			},
			'screening': {
				'records_screened': 0,
				'records_excluded': 0,
				'exclusion_reasons': {},
			},
			'eligibility': {
				'reports_sought': 0,
				'reports_not_retrieved': 0,
				'reports_assessed': 0,
				'reports_excluded': 0,
				'exclusion_reasons': {},
			},
			'included': {
				'studies_included': 0,
				'reports_included': 0,
			},
		}

	def add_database_results(self, database_name: str, count: int, search_date: str | None = None) -> None:
		"""Add results from a database search"""
		self.data['identification']['databases'][database_name] = {
			'count': count,
			'search_date': search_date or datetime.now().strftime('%Y-%m-%d'),
		}
		self._recalculate_totals()

	def add_other_source_results(self, source_name: str, count: int) -> None:
		"""Add results from other sources (e.g., citation searching, hand searching)"""
		self.data['identification']['other_sources'][source_name] = count
		self._recalculate_totals()

	def set_duplicates_removed(self, count: int) -> None:
		"""Set the number of duplicate records removed"""
		self.data['identification']['duplicates_removed'] = count

	def add_screening_exclusion(self, reason: str, count: int) -> None:
		"""Add title/abstract screening exclusion with reason"""
		self.data['screening']['exclusion_reasons'][reason] = count
		self._recalculate_screening()

	def add_eligibility_exclusion(self, reason: str, count: int) -> None:
		"""Add full-text eligibility exclusion with reason"""
		self.data['eligibility']['exclusion_reasons'][reason] = count
		self._recalculate_eligibility()

	def set_reports_not_retrieved(self, count: int) -> None:
		"""Set number of reports sought but not retrieved"""
		self.data['eligibility']['reports_not_retrieved'] = count

	def set_final_included(self, studies: int, reports: int | None = None) -> None:
		"""Set final number of included studies and reports"""
		self.data['included']['studies_included'] = studies
		self.data['included']['reports_included'] = reports or studies

	def _recalculate_totals(self) -> None:
		"""Recalculate total identified records"""
		db_total = sum(db['count'] for db in self.data['identification']['databases'].values())
		other_total = sum(self.data['identification']['other_sources'].values())
		self.data['identification']['total_identified'] = db_total + other_total

	def _recalculate_screening(self) -> None:
		"""Recalculate screening totals"""
		total_identified = self.data['identification']['total_identified']
		duplicates = self.data['identification']['duplicates_removed']
		self.data['screening']['records_screened'] = total_identified - duplicates
		self.data['screening']['records_excluded'] = sum(self.data['screening']['exclusion_reasons'].values())

	def _recalculate_eligibility(self) -> None:
		"""Recalculate eligibility totals"""
		screened = self.data['screening']['records_screened']
		excluded = self.data['screening']['records_excluded']
		self.data['eligibility']['reports_sought'] = screened - excluded
		self.data['eligibility']['reports_excluded'] = sum(self.data['eligibility']['exclusion_reasons'].values())
		self.data['eligibility']['reports_assessed'] = (
			self.data['eligibility']['reports_sought'] - self.data['eligibility']['reports_not_retrieved']
		)

	def generate_mermaid_diagram(self) -> str:
		"""Generate Mermaid.js flowchart for PRISMA diagram"""
		# Recalculate all totals
		self._recalculate_totals()
		self._recalculate_screening()
		self._recalculate_eligibility()

		d = self.data

		# Build database identification boxes
		db_boxes = []
		for db_name, db_info in d['identification']['databases'].items():
			db_boxes.append(f'  DB_{db_name.replace(" ", "_")}["Records from {db_name}<br/>n = {db_info["count"]}"]')

		other_boxes = []
		for source_name, count in d['identification']['other_sources'].items():
			other_boxes.append(f'  OTHER_{source_name.replace(" ", "_")}["Records from {source_name}<br/>n = {count}"]')

		mermaid = f"""flowchart TD
	%% PRISMA 2020 Flow Diagram

	%% Identification
{chr(10).join(db_boxes) if db_boxes else '  DB[Records identified from databases<br/>n = 0]'}
{chr(10).join(other_boxes) if other_boxes else ''}

	IDENTIFIED["Records identified<br/>n = {d['identification']['total_identified']}"]
	DUPLICATES["Duplicate records removed<br/>n = {d['identification']['duplicates_removed']}"]

	%% Screening
	SCREENED["Records screened<br/>n = {d['screening']['records_screened']}"]
	SCREEN_EXCLUDED["Records excluded<br/>n = {d['screening']['records_excluded']}"]

	%% Eligibility
	SOUGHT["Reports sought for retrieval<br/>n = {d['eligibility']['reports_sought']}"]
	NOT_RETRIEVED["Reports not retrieved<br/>n = {d['eligibility']['reports_not_retrieved']}"]
	ASSESSED["Reports assessed for eligibility<br/>n = {d['eligibility']['reports_assessed']}"]
	ELIG_EXCLUDED["Reports excluded<br/>n = {d['eligibility']['reports_excluded']}"]

	%% Included
	INCLUDED["Studies included in review<br/>n = {d['included']['studies_included']}<br/>Reports: {d['included']['reports_included']}"]

	%% Connections
"""

		# Add connections from databases
		if db_boxes:
			for db_name in d['identification']['databases'].keys():
				mermaid += f'  DB_{db_name.replace(" ", "_")} --> IDENTIFIED\n'
		if other_boxes:
			for source_name in d['identification']['other_sources'].keys():
				mermaid += f'  OTHER_{source_name.replace(" ", "_")} --> IDENTIFIED\n'

		mermaid += """  IDENTIFIED --> DUPLICATES
  DUPLICATES --> SCREENED
  SCREENED --> SCREEN_EXCLUDED
  SCREENED --> SOUGHT
  SOUGHT --> NOT_RETRIEVED
  SOUGHT --> ASSESSED
  ASSESSED --> ELIG_EXCLUDED
  ASSESSED --> INCLUDED
"""

		return mermaid

	def generate_markdown_report(self) -> str:
		"""Generate a markdown report with PRISMA flow diagram and details"""
		mermaid_diagram = self.generate_mermaid_diagram()
		d = self.data

		report = f"""# PRISMA 2020 Flow Diagram

## Search Flow

```mermaid
{mermaid_diagram}```

## Detailed Breakdown

### Identification

**Database Searches:**
"""

		for db_name, db_info in d['identification']['databases'].items():
			report += f'\n- **{db_name}**: {db_info["count"]} records (searched: {db_info["search_date"]})'

		if d['identification']['other_sources']:
			report += '\n\n**Other Sources:**\n'
			for source_name, count in d['identification']['other_sources'].items():
				report += f'\n- **{source_name}**: {count} records'

		report += f"""

**Total Records Identified:** {d['identification']['total_identified']}
**Duplicate Records Removed:** {d['identification']['duplicates_removed']}

### Screening

**Records Screened (title/abstract):** {d['screening']['records_screened']}
**Records Excluded:** {d['screening']['records_excluded']}
"""

		if d['screening']['exclusion_reasons']:
			report += '\n**Exclusion Reasons:**\n'
			for reason, count in d['screening']['exclusion_reasons'].items():
				report += f'\n- {reason}: {count} records'

		report += f"""

### Eligibility Assessment

**Reports Sought for Retrieval:** {d['eligibility']['reports_sought']}
**Reports Not Retrieved:** {d['eligibility']['reports_not_retrieved']}
**Reports Assessed (full-text):** {d['eligibility']['reports_assessed']}
**Reports Excluded:** {d['eligibility']['reports_excluded']}
"""

		if d['eligibility']['exclusion_reasons']:
			report += '\n**Exclusion Reasons:**\n'
			for reason, count in d['eligibility']['exclusion_reasons'].items():
				report += f'\n- {reason}: {count} reports'

		report += f"""

### Included

**Studies Included in Review:** {d['included']['studies_included']}
**Total Reports:** {d['included']['reports_included']}

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*PRISMA 2020 compliant flow diagram*
"""

		return report

	def save_data(self, output_path: Path) -> None:
		"""Save PRISMA data to JSON file"""
		output_path.parent.mkdir(parents=True, exist_ok=True)
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(self.data, f, indent=2, ensure_ascii=False)

	def save_markdown_report(self, output_path: Path) -> None:
		"""Save markdown report with PRISMA diagram"""
		output_path.parent.mkdir(parents=True, exist_ok=True)
		report = self.generate_markdown_report()
		with open(output_path, 'w', encoding='utf-8') as f:
			f.write(report)


def create_example_diagram() -> PRISMAFlowDiagram:
	"""Create an example PRISMA flow diagram"""
	diagram = PRISMAFlowDiagram()

	# Identification
	diagram.add_database_results('IEEE Xplore', 450, '2024-10-18')
	diagram.add_database_results('PubMed', 230, '2024-10-18')
	diagram.add_database_results('arXiv', 120, '2024-10-18')
	diagram.add_other_source_results('Citation searching', 25)
	diagram.set_duplicates_removed(180)

	# Screening
	diagram.add_screening_exclusion('Not relevant to topic', 320)
	diagram.add_screening_exclusion('Not in English', 45)
	diagram.add_screening_exclusion('Wrong publication type', 30)

	# Eligibility
	diagram.set_reports_not_retrieved(8)
	diagram.add_eligibility_exclusion('Insufficient data', 35)
	diagram.add_eligibility_exclusion('Not peer-reviewed', 12)
	diagram.add_eligibility_exclusion('Duplicate publication', 5)

	# Included
	diagram.set_final_included(studies=30, reports=33)

	return diagram


if __name__ == '__main__':
	# Create example diagram
	diagram = create_example_diagram()

	# Save data
	data_path = Path('automated_research/data/prisma_flow_data.json')
	diagram.save_data(data_path)
	print(f'Saved PRISMA data to: {data_path}')

	# Save markdown report
	report_path = Path('automated_research/reports/prisma_flow_diagram.md')
	diagram.save_markdown_report(report_path)
	print(f'Saved PRISMA report to: {report_path}')

	print('\nMermaid diagram:')
	print(diagram.generate_mermaid_diagram())
