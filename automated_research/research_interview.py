"""
Interactive research interview system
対話型研究ヒアリングシステム
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from browser_use.llm.openai.chat import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)


class ResearchInterviewer:
	"""ユーザーの研究内容をヒアリングするインタラクティブシステム"""

	def __init__(self, llm: ChatOpenAI | None = None):
		self.llm = llm or ChatOpenAI(model='gpt-4o', temperature=0.7)
		self.conversation_history: list[dict[str, str]] = []

	async def conduct_interview(self) -> dict[str, Any]:
		"""
		対話形式でユーザーの研究内容をヒアリング

		Returns:
			研究情報を含む辞書
		"""
		print('\n' + '=' * 80)
		print('🔬 研究テーマ自動分析システム')
		print('=' * 80)
		print('\nどんな内容について検索しますか？あなたの研究はなんですか？')
		print('あなたの研究について自由に語ってください。')
		print('（詳しければ詳しいほど、より適切な文献検索が可能になります）')
		print('\n' + '-' * 80 + '\n')

		# ユーザーの初期入力を取得
		user_initial_input = input('あなた: ').strip()

		if not user_initial_input:
			print('⚠️  入力が空です。研究内容を入力してください。')
			return await self.conduct_interview()

		# 研究情報を格納する辞書
		research_info = {
			'initial_description': user_initial_input,
			'research_theme': '',
			'research_purpose': '',
			'research_field': '',
			'specific_technologies': [],
			'problem_statement': '',
			'known_papers': [],
			'additional_context': '',
		}

		print('\n📝 あなたの研究内容を分析しています...\n')

		# LLMに研究内容を分析させ、追加質問を生成
		analysis_prompt = f"""
ユーザーが以下のように研究内容を説明しました：

「{user_initial_input}」

この説明から以下の情報を抽出してください：
1. 研究テーマの仮説
2. 研究分野の推定
3. 明確化が必要な点（2-3個の具体的な質問）

JSON形式で以下の構造で出力してください：
{{
	"inferred_theme": "推定される研究テーマ",
	"inferred_field": "推定される研究分野",
	"clarification_questions": [
		"質問1",
		"質問2",
		"質問3"
	]
}}
"""

		# LLMを使って分析
		from browser_use.llm.messages import UserMessage

		messages = [UserMessage(content=analysis_prompt)]

		try:
			response = await self.llm.get_response(messages)
			response_text = response.content

			# JSONを抽出（マークダウンコードブロックを除去）
			if '```json' in response_text:
				json_text = response_text.split('```json')[1].split('```')[0].strip()
			elif '```' in response_text:
				json_text = response_text.split('```')[1].split('```')[0].strip()
			else:
				json_text = response_text.strip()

			analysis = json.loads(json_text)

			research_info['research_theme'] = analysis.get('inferred_theme', '')
			research_info['research_field'] = analysis.get('inferred_field', '')

			print(f'推定される研究テーマ: {analysis.get("inferred_theme", "不明")}')
			print(f'推定される研究分野: {analysis.get("inferred_field", "不明")}\n')

			# 追加の質問をする
			print('より適切な検索のため、いくつか質問させてください：\n')

			clarification_questions = analysis.get('clarification_questions', [])

			for i, question in enumerate(clarification_questions, 1):
				print(f'質問 {i}: {question}')
				answer = input('あなた: ').strip()

				if answer:
					# 質問に応じて情報を格納
					if i == 1:
						research_info['research_purpose'] = answer
					elif i == 2:
						research_info['problem_statement'] = answer
					elif i == 3:
						research_info['additional_context'] = answer

				print()

			# 特定の技術・キーワードを確認
			print('質問: 特に注目している技術、手法、キーワードがあれば教えてください')
			print('     （複数ある場合はカンマ区切りで入力）')
			tech_input = input('あなた: ').strip()

			if tech_input:
				research_info['specific_technologies'] = [t.strip() for t in tech_input.split(',') if t.strip()]

			print()

			# 既知の論文・研究者
			print('質問: すでに知っている重要な論文や研究者はいますか？')
			print('     （任意：スキップする場合は Enter を押してください）')
			papers_input = input('あなた: ').strip()

			if papers_input:
				research_info['known_papers'] = [p.strip() for p in papers_input.split(',') if p.strip()]

		except Exception as e:
			logger.error(f'Error during interview analysis: {e}')
			# エラーが発生した場合は基本情報のみで続行
			research_info['research_theme'] = user_initial_input
			research_info['research_field'] = '未分類'

		print('\n' + '=' * 80)
		print('✅ ヒアリング完了！')
		print('=' * 80)
		print('\n収集した研究情報:')
		print(f'- 研究テーマ: {research_info["research_theme"]}')
		print(f'- 研究分野: {research_info["research_field"]}')
		if research_info['specific_technologies']:
			print(f'- 注目技術: {", ".join(research_info["specific_technologies"])}')
		print()

		return research_info

	def save_research_info(self, research_info: dict[str, Any], output_path: Path) -> None:
		"""研究情報をJSONファイルに保存"""
		output_path.parent.mkdir(parents=True, exist_ok=True)

		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(research_info, f, indent=2, ensure_ascii=False)

		logger.info(f'Research info saved to: {output_path}')


async def main():
	"""テスト実行用のメイン関数"""
	interviewer = ResearchInterviewer()
	research_info = await interviewer.conduct_interview()

	# 保存
	output_path = Path('automated_research/data/research_info.json')
	interviewer.save_research_info(research_info, output_path)

	print(f'\n💾 研究情報を保存しました: {output_path}')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
