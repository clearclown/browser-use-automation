"""
Ochiai-style paper analysis and report generation
落合陽一式論文分析とレポート生成
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from automated_research.prompts.system_prompts import (
	FINAL_SUMMARY_PROMPT,
	OCHIAI_STYLE_ANALYSIS_PROMPT,
)
from langchain_core.messages import HumanMessage
from automated_research.llm_provider import get_llm

load_dotenv()

logger = logging.getLogger(__name__)


class OchiaiReportGenerator:
	"""落合陽一式の論文分析レポートを生成"""

	def __init__(self, llm: Any | None = None):
		self.llm = llm or get_llm(temperature=0.4)

	async def generate_paper_report(
		self, paper_info: dict[str, Any], research_context: dict[str, Any], pdf_content: str | None = None
	) -> str:
		"""
		単一の論文に対して落合陽一式レポートを生成

		Args:
			paper_info: 論文のメタデータ
			research_context: ユーザーの研究コンテキスト
			pdf_content: PDF抽出テキスト（オプション）

		Returns:
			マークダウン形式のレポート
		"""
		logger.info(f'📝 Generating Ochiai-style report for: {paper_info.get("title", "Unknown")}')

		# 論文メタデータを整形
		metadata_text = self._format_paper_metadata(paper_info)

		# PDF内容（なければメタデータのみ）
		content_text = pdf_content if pdf_content else '(PDF content not available - using metadata only)'

		# ユーザー研究コンテキストを整形
		user_research_text = self._format_research_context(research_context)

		# プロンプトを作成
		prompt = OCHIAI_STYLE_ANALYSIS_PROMPT.format(
			paper_metadata=metadata_text, paper_content=content_text, user_research=user_research_text
		)

		messages = [HumanMessage(content=prompt)]

		try:
			# LLMでレポート生成
			response = await self.llm.ainvoke(messages)
			report = response.content

			# マークダウンのコードブロックを除去
			if '```markdown' in report:
				report = report.split('```markdown')[1].split('```')[0].strip()
			elif '```' in report:
				# 最初のコードブロックを抽出
				parts = report.split('```')
				if len(parts) >= 3:
					report = parts[1].strip()

			return report

		except Exception as e:
			logger.error(f'Error generating report: {e}')
			return self._generate_fallback_report(paper_info)

	def _format_paper_metadata(self, paper_info: dict[str, Any]) -> str:
		"""論文メタデータをテキスト形式に整形"""
		parts = []

		parts.append(f'Title: {paper_info.get("title", "N/A")}')
		parts.append(f'Authors: {", ".join(paper_info.get("authors", ["N/A"]))}')
		parts.append(f'Year: {paper_info.get("year", "N/A")}')
		parts.append(f'Publication: {paper_info.get("publication", "N/A")}')
		parts.append(f'DOI: {paper_info.get("doi", "N/A")}')
		parts.append(f'URL: {paper_info.get("url", "N/A")}')

		if paper_info.get('abstract'):
			parts.append(f'\nAbstract:\n{paper_info["abstract"]}')

		return '\n'.join(parts)

	def _format_research_context(self, research_context: dict[str, Any]) -> str:
		"""研究コンテキストをテキスト形式に整形"""
		parts = []

		parts.append(f'研究テーマ: {research_context.get("research_theme", "N/A")}')
		parts.append(f'研究分野: {research_context.get("research_field", "N/A")}')

		if research_context.get('research_purpose'):
			parts.append(f'研究目的: {research_context["research_purpose"]}')

		if research_context.get('problem_statement'):
			parts.append(f'問題意識: {research_context["problem_statement"]}')

		if research_context.get('specific_technologies'):
			tech_list = ', '.join(research_context['specific_technologies'])
			parts.append(f'注目技術: {tech_list}')

		return '\n'.join(parts)

	def _generate_fallback_report(self, paper_info: dict[str, Any]) -> str:
		"""フォールバック：基本的なレポートを生成"""
		logger.warning('Falling back to basic report generation')

		title = paper_info.get('title', 'Unknown Title')
		authors = ', '.join(paper_info.get('authors', ['Unknown']))
		year = paper_info.get('year', 'Unknown')
		url = paper_info.get('url', '#')

		report = f"""## title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: Research

### 1. どんなもの？
（詳細な分析が利用できません）

### 2. 先行研究と比べてどこがすごいの？
（詳細な分析が利用できません）

### 3. 技術や手法の"キモ"はどこにある？
（詳細な分析が利用できません）

### 4. どうやって有効だと検証した？
（詳細な分析が利用できません）

### 5. 議論はあるか？
（詳細な分析が利用できません）

### 6. 次に読むべき論文はあるか？
（詳細な分析が利用できません）

### 7. 自分の研究との関連
（詳細な分析が利用できません）

### 論文情報・リンク
- [{authors}, "{title}," {year}]({url})
"""
		return report

	async def generate_summary_report(
		self, all_reports: list[str], research_context: dict[str, Any], search_strategy: dict[str, Any]
	) -> str:
		"""
		すべてのレポートを統合して総合サマリーを生成

		Args:
			all_reports: 個別の論文レポートリスト
			research_context: 研究コンテキスト
			search_strategy: 検索戦略

		Returns:
			統合レポート（マークダウン）
		"""
		logger.info('📊 Generating comprehensive summary report...')

		# 研究テーマを取得
		research_theme = research_context.get('research_theme', 'Unknown Theme')

		# 検索戦略をテキスト形式に
		strategy_text = self._format_search_strategy(search_strategy)

		# すべてのレポートを結合
		reports_text = '\n\n---\n\n'.join(all_reports)

		# プロンプトを作成
		prompt = FINAL_SUMMARY_PROMPT.format(
			user_research=self._format_research_context(research_context),
			research_theme=research_theme,
			search_strategy=strategy_text,
			all_reports=reports_text,
			generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
			total_papers=len(all_reports),
		)

		messages = [HumanMessage(content=prompt)]

		try:
			response = await self.llm.ainvoke(messages)
			summary = response.content

			# マークダウンのコードブロックを除去
			if '```markdown' in summary:
				summary = summary.split('```markdown')[1].split('```')[0].strip()
			elif '```' in summary:
				parts = summary.split('```')
				if len(parts) >= 3:
					summary = parts[1].strip()

			return summary

		except Exception as e:
			logger.error(f'Error generating summary report: {e}')
			return self._generate_fallback_summary(research_theme, len(all_reports))

	def _format_search_strategy(self, strategy: dict[str, Any]) -> str:
		"""検索戦略をテキスト形式に整形"""
		parts = []

		if strategy.get('primary_keywords'):
			parts.append(f'主要キーワード: {", ".join(strategy["primary_keywords"])}')

		if strategy.get('search_queries'):
			parts.append('\n検索クエリ:')
			for i, query in enumerate(strategy['search_queries'], 1):
				parts.append(f'  {i}. {query}')

		return '\n'.join(parts)

	def _generate_fallback_summary(self, research_theme: str, paper_count: int) -> str:
		"""フォールバック：基本的な統合レポート"""
		return f"""# 体系的文献レビュー: {research_theme}

## エグゼクティブサマリー
合計 {paper_count} 件の論文を収集・分析しました。

（詳細な統合分析が利用できません。各論文の個別レポートを参照してください。）

---
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
総論文数: {paper_count}
"""

	def save_report(self, report: str, output_path: Path, paper_title: str | None = None) -> None:
		"""レポートをマークダウンファイルに保存"""
		output_path.parent.mkdir(parents=True, exist_ok=True)

		# ファイル名を生成（タイトルから）
		if paper_title:
			# ファイル名として安全な形式に変換
			safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in paper_title)
			safe_title = safe_title[:50]  # 長すぎる場合は切り詰め
			filename = f'{safe_title}.md'
			final_path = output_path / filename
		else:
			final_path = output_path

		with open(final_path, 'w', encoding='utf-8') as f:
			f.write(report)

		logger.info(f'Report saved to: {final_path}')


async def main():
	"""テスト実行用のメイン関数"""
	# テスト用の論文情報
	paper_info = {
		'title': 'Test Paper on Machine Learning',
		'authors': ['John Doe', 'Jane Smith'],
		'year': 2023,
		'publication': 'IEEE Transactions on AI',
		'doi': '10.1109/TEST.2023',
		'url': 'https://ieeexplore.ieee.org/document/test',
		'abstract': 'This is a test abstract for machine learning research.',
	}

	research_context = {
		'research_theme': 'Machine Learning for Healthcare',
		'research_field': 'AI',
		'research_purpose': 'To improve diagnosis accuracy',
	}

	generator = OchiaiReportGenerator()

	# 個別レポート生成
	report = await generator.generate_paper_report(paper_info, research_context)

	# 保存
	output_path = Path('automated_research/reports')
	generator.save_report(report, output_path, paper_info['title'])

	print('\n✅ レポートを生成しました')
	print(f'\nレポート内容（抜粋）:\n{report[:500]}...')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
