"""
PRISMA-based search strategy generator
PRISMA方式に基づいた検索戦略生成
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from automated_research.prompts.system_prompts import PRISMA_SEARCH_STRATEGY_PROMPT
from browser_use.llm.messages import UserMessage
from automated_research.llm_provider import get_llm

load_dotenv()

logger = logging.getLogger(__name__)


class PRISMASearchStrategyGenerator:
	"""PRISMA方式に基づいた検索戦略を生成"""

	def __init__(self, llm: Any | None = None):
		self.llm = llm or get_llm(temperature=0.3)

	async def generate_search_strategy(self, research_info: dict[str, Any]) -> dict[str, Any]:
		"""
		研究情報からPRISMA方式の検索戦略を生成

		Args:
			research_info: ユーザーの研究情報

		Returns:
			検索戦略を含む辞書
		"""
		print('\n' + '=' * 80)
		print('📊 PRISMA方式検索戦略を生成中...')
		print('=' * 80 + '\n')

		# 研究情報をテキスト形式に整形
		research_context = self._format_research_context(research_info)

		# プロンプトを作成
		prompt = PRISMA_SEARCH_STRATEGY_PROMPT.format(research_context=research_context)

		messages = [UserMessage(content=prompt)]

		try:
			# LLMに検索戦略を生成させる
			response = await self.llm.get_response(messages)
			response_text = response.content

			# JSONを抽出
			if '```json' in response_text:
				json_text = response_text.split('```json')[1].split('```')[0].strip()
			elif '```' in response_text:
				json_text = response_text.split('```')[1].split('```')[0].strip()
			else:
				json_text = response_text.strip()

			search_strategy = json.loads(json_text)

			# 結果を表示
			self._display_search_strategy(search_strategy)

			return search_strategy

		except Exception as e:
			logger.error(f'Error generating search strategy: {e}')
			# フォールバック：基本的な検索戦略を生成
			return self._generate_fallback_strategy(research_info)

	def _format_research_context(self, research_info: dict[str, Any]) -> str:
		"""研究情報をテキスト形式に整形"""
		context_parts = []

		context_parts.append(f'研究テーマ: {research_info.get("research_theme", "N/A")}')
		context_parts.append(f'研究分野: {research_info.get("research_field", "N/A")}')

		if research_info.get('research_purpose'):
			context_parts.append(f'研究目的: {research_info["research_purpose"]}')

		if research_info.get('problem_statement'):
			context_parts.append(f'問題意識: {research_info["problem_statement"]}')

		if research_info.get('specific_technologies'):
			tech_list = ', '.join(research_info['specific_technologies'])
			context_parts.append(f'注目技術: {tech_list}')

		if research_info.get('additional_context'):
			context_parts.append(f'追加情報: {research_info["additional_context"]}')

		if research_info.get('known_papers'):
			papers_list = ', '.join(research_info['known_papers'])
			context_parts.append(f'既知の研究: {papers_list}')

		return '\n'.join(context_parts)

	def _display_search_strategy(self, strategy: dict[str, Any]) -> None:
		"""検索戦略を見やすく表示"""
		print('✅ 検索戦略を生成しました\n')

		print('【主要キーワード】')
		for keyword in strategy.get('primary_keywords', []):
			print(f'  • {keyword}')
		print()

		print('【関連キーワード】')
		for keyword in strategy.get('related_keywords', []):
			print(f'  • {keyword}')
		print()

		if strategy.get('exclusion_keywords'):
			print('【除外キーワード】')
			for keyword in strategy['exclusion_keywords']:
				print(f'  • {keyword}')
			print()

		print('【検索クエリ】')
		for i, query in enumerate(strategy.get('search_queries', []), 1):
			print(f'  {i}. {query}')
		print()

		if strategy.get('year_range'):
			year_range = strategy['year_range']
			print(f'【出版年範囲】 {year_range.get("start", "N/A")} - {year_range.get("end", "N/A")}')
			print()

		if strategy.get('publication_types'):
			print(f'【出版物タイプ】 {", ".join(strategy["publication_types"])}')
			print()

	def _generate_fallback_strategy(self, research_info: dict[str, Any]) -> dict[str, Any]:
		"""
		フォールバック：基本的な検索戦略を生成
		LLMが失敗した場合の代替策
		"""
		logger.warning('Falling back to basic search strategy generation')

		# 研究テーマから基本的なキーワードを抽出
		theme = research_info.get('research_theme', '')
		field = research_info.get('research_field', '')
		technologies = research_info.get('specific_technologies', [])

		# 基本的な検索戦略
		primary_keywords = []
		if theme:
			primary_keywords.append(theme)
		if field:
			primary_keywords.append(field)
		primary_keywords.extend(technologies[:3])

		search_queries = [' AND '.join(primary_keywords[:3])] if len(primary_keywords) >= 2 else [theme or field]

		return {
			'primary_keywords': primary_keywords,
			'related_keywords': [],
			'exclusion_keywords': [],
			'search_queries': search_queries,
			'year_range': {'start': 2018, 'end': 2024},
			'publication_types': ['Journal', 'Conference'],
		}

	def save_search_strategy(self, strategy: dict[str, Any], output_path: Path) -> None:
		"""検索戦略をJSONファイルに保存"""
		output_path.parent.mkdir(parents=True, exist_ok=True)

		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(strategy, f, indent=2, ensure_ascii=False)

		logger.info(f'Search strategy saved to: {output_path}')


async def main():
	"""テスト実行用のメイン関数"""
	# テスト用の研究情報を読み込み
	research_info_path = Path('automated_research/data/research_info.json')

	if not research_info_path.exists():
		print('⚠️  研究情報ファイルが見つかりません。')
		print('先に research_interview.py を実行してください。')
		return

	with open(research_info_path, encoding='utf-8') as f:
		research_info = json.load(f)

	# 検索戦略を生成
	generator = PRISMASearchStrategyGenerator()
	search_strategy = await generator.generate_search_strategy(research_info)

	# 保存
	output_path = Path('automated_research/data/search_strategy.json')
	generator.save_search_strategy(search_strategy, output_path)

	print(f'\n💾 検索戦略を保存しました: {output_path}')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
