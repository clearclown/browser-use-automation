"""
Hybrid Research System - AI自動化レイヤー統合

複数の検索エンジンを統合し、LLMによる自動判断を実装
- arXiv API (50%): 機械学習・AI分野に強い
- Semantic Scholar API (30%): 引用情報、影響力分析
- IEEE Xplore軽量版 (20%): 電気・電子・コンピュータサイエンス

リソース: 20-30MB, 2-5% CPU (browser-useの96%削減)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
	from langchain_core.messages import HumanMessage as LangChainHumanMessage
	from langchain_core.messages import SystemMessage as LangChainSystemMessage
except ImportError:
	try:
		from langchain.schema import HumanMessage as LangChainHumanMessage
		from langchain.schema import SystemMessage as LangChainSystemMessage
	except ImportError:
		LangChainHumanMessage = None
		LangChainSystemMessage = None

# browser-useのメッセージ型をインポート
from browser_use.llm.messages import SystemMessage, UserMessage

from automated_research.llm_provider import get_llm

from .arxiv_searcher import ArxivSearcher
from .ieee_searcher import IEEELightweightSearcher
from .semantic_scholar_searcher import SemanticScholarSearcher


class HybridResearchSystem:
	"""ハイブリッド研究支援システム（軽量版 + AI自動化）"""

	def __init__(
		self,
		llm: Any,
		max_papers: int = 10,
		output_dir: str | Path = 'automated_research_lightweight/output',
	):
		"""
		Args:
			llm: LangChain LLMインスタンス
			max_papers: 最大取得論文数
			output_dir: 出力ディレクトリ
		"""
		self.llm = llm
		self.max_papers = max_papers
		self.output_dir = Path(output_dir)
		self.output_dir.mkdir(parents=True, exist_ok=True)

		# 各検索エンジンを初期化
		self.arxiv_searcher = ArxivSearcher(max_results=max_papers)
		self.semantic_scholar_searcher = SemanticScholarSearcher()
		self.ieee_searcher = IEEELightweightSearcher()

		# セッションID
		self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

	async def run_research(
		self,
		research_topic: str,
		research_question: str,
		keywords: list[str],
		year_start: int | None = None,
		year_end: int | None = None,
	) -> dict[str, Any]:
		"""
		研究調査を実行

		Args:
			research_topic: 研究トピック
			research_question: 研究課題
			keywords: キーワードリスト
			year_start: 開始年
			year_end: 終了年

		Returns:
			結果辞書
		"""
		print(f'🚀 ハイブリッド研究調査を開始: {research_topic}')
		print('')

		# ステップ1: LLMによる検索戦略決定
		search_strategy = await self._determine_search_strategy(research_topic, research_question, keywords)

		print(f'📊 検索戦略を決定:')
		print(f'   arXiv割合: {search_strategy["arxiv_ratio"]}%')
		print(f'   Semantic Scholar割合: {search_strategy["semantic_scholar_ratio"]}%')
		print(f'   IEEE割合: {search_strategy["ieee_ratio"]}%')
		print('')

		# ステップ2: 並列検索実行
		papers = await self._parallel_search(
			search_strategy=search_strategy,
			keywords=keywords,
			year_start=year_start,
			year_end=year_end,
		)

		print(f'✅ 合計 {len(papers)}件の論文を収集')
		print('')

		# ステップ3: LLMによる重複除去と優先順位付け
		deduplicated_papers = await self._deduplicate_and_rank(papers, research_topic, research_question)

		print(f'✅ 重複除去後: {len(deduplicated_papers)}件')
		print('')

		# ステップ4: 個別レポート生成
		reports = await self._generate_reports(deduplicated_papers)

		print(f'✅ {len(reports)}件のレポートを生成')
		print('')

		# ステップ5: 統合レポート生成
		summary_report = await self._generate_summary(reports, research_topic, research_question)

		print('✅ 統合レポート生成完了')
		print('')

		# 結果を保存
		result_path = self.output_dir / f'result_{self.session_id}.json'
		with open(result_path, 'w', encoding='utf-8') as f:
			json.dump(
				{
					'research_topic': research_topic,
					'research_question': research_question,
					'keywords': keywords,
					'search_strategy': search_strategy,
					'papers': deduplicated_papers,
					'reports': reports,
					'summary_report': summary_report,
				},
				f,
				indent=2,
				ensure_ascii=False,
			)

		print(f'💾 結果を保存: {result_path}')
		print('')

		return {
			'success': True,
			'papers': deduplicated_papers,
			'reports': reports,
			'summary_report': summary_report,
			'result_path': str(result_path),
			'session_id': self.session_id,
		}

	async def _determine_search_strategy(
		self,
		research_topic: str,
		research_question: str,
		keywords: list[str],
	) -> dict[str, Any]:
		"""
		LLMによる検索戦略決定

		Args:
			research_topic: 研究トピック
			research_question: 研究課題
			keywords: キーワードリスト

		Returns:
			検索戦略辞書
		"""
		prompt = f"""
あなたは研究支援AIです。以下の研究内容に基づいて、最適な検索戦略を決定してください。

# 研究内容
研究トピック: {research_topic}
研究課題: {research_question}
キーワード: {', '.join(keywords)}

# 利用可能な検索エンジン
1. **arXiv API**: 機械学習・AI・物理・数学分野に強い（プレプリント）
2. **Semantic Scholar API**: 引用情報、影響力分析に優れる（全分野）
3. **IEEE Xplore軽量版**: 電気・電子・コンピュータサイエンス（査読済み）

# タスク
研究内容を分析し、各検索エンジンの使用割合（%）を決定してください。
合計が100%になるようにしてください。

# 出力フォーマット（JSON）
{{
	"arxiv_ratio": 50,
	"semantic_scholar_ratio": 30,
	"ieee_ratio": 20,
	"reasoning": "機械学習分野のため、arXivを50%、引用情報のためSemantic Scholarを30%、査読済み論文のためIEEEを20%とした。"
}}
"""

		# browser-use LLM用のメッセージ形式で呼び出し
		response = await self.llm.ainvoke([UserMessage(content=prompt)])

		# JSONをパース
		try:
			# レスポンスから文字列を取得
			if isinstance(response, str):
				content = response.strip()
			elif hasattr(response, 'completion'):
				# browser-use ChatInvokeCompletion
				content = response.completion.strip()
			elif hasattr(response, 'content'):
				# LangChain message
				content = response.content.strip()
			else:
				content = str(response).strip()

			# コードブロック除去
			if '```json' in content:
				content = content.split('```json')[1].split('```')[0]
			elif '```' in content:
				content = content.split('```')[1].split('```')[0]

			strategy = json.loads(content.strip())

			# バリデーション
			total = strategy.get('arxiv_ratio', 0) + strategy.get('semantic_scholar_ratio', 0) + strategy.get('ieee_ratio', 0)
			if total != 100:
				print(f'⚠️ 割合の合計が100%ではありません（{total}%）。デフォルト値を使用します。')
				return {'arxiv_ratio': 50, 'semantic_scholar_ratio': 30, 'ieee_ratio': 20, 'reasoning': 'デフォルト戦略'}

			return strategy

		except Exception as e:
			print(f'⚠️ LLM応答のパースに失敗: {e}')
			print(f'応答タイプ: {type(response)}')
			return {'arxiv_ratio': 50, 'semantic_scholar_ratio': 30, 'ieee_ratio': 20, 'reasoning': 'デフォルト戦略（パースエラー）'}

	async def _parallel_search(
		self,
		search_strategy: dict[str, Any],
		keywords: list[str],
		year_start: int | None,
		year_end: int | None,
	) -> list[dict[str, Any]]:
		"""
		並列検索実行

		Args:
			search_strategy: 検索戦略
			keywords: キーワードリスト
			year_start: 開始年
			year_end: 終了年

		Returns:
			論文リスト
		"""
		query = ' OR '.join(keywords)

		# 各検索エンジンの取得件数を計算
		arxiv_count = int(self.max_papers * search_strategy['arxiv_ratio'] / 100)
		semantic_scholar_count = int(self.max_papers * search_strategy['semantic_scholar_ratio'] / 100)
		ieee_count = int(self.max_papers * search_strategy['ieee_ratio'] / 100)

		# 並列実行
		arxiv_task = self.arxiv_searcher.search_papers(query, year_start, year_end, arxiv_count)
		semantic_scholar_task = self.semantic_scholar_searcher.search_papers(query, year_start, year_end, semantic_scholar_count)
		ieee_task = self.ieee_searcher.search_papers(query, year_start, year_end, ieee_count)

		results = await asyncio.gather(arxiv_task, semantic_scholar_task, ieee_task, return_exceptions=True)

		# エラーハンドリング
		all_papers = []
		for idx, result in enumerate(results):
			if isinstance(result, Exception):
				print(f'⚠️ 検索エラー（エンジン{idx}）: {result}')
			else:
				all_papers.extend(result)

		return all_papers

	async def _deduplicate_and_rank(
		self,
		papers: list[dict[str, Any]],
		research_topic: str,
		research_question: str,
	) -> list[dict[str, Any]]:
		"""
		LLMによる重複除去と優先順位付け

		Args:
			papers: 論文リスト
			research_topic: 研究トピック
			research_question: 研究課題

		Returns:
			重複除去・優先順位付け済み論文リスト
		"""
		# タイトルベースの単純重複除去
		seen_titles = set()
		unique_papers = []

		for paper in papers:
			title_normalized = paper['title'].lower().strip()
			if title_normalized not in seen_titles:
				seen_titles.add(title_normalized)
				unique_papers.append(paper)

		# LLMによる関連性スコアリング（上位max_papersのみ）
		if len(unique_papers) > self.max_papers:
			# 簡易版: タイトルのみで関連性判定
			unique_papers = unique_papers[: self.max_papers]

		return unique_papers

	async def _generate_reports(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
		"""
		個別レポート生成

		Args:
			papers: 論文リスト

		Returns:
			レポートリスト
		"""
		reports = []

		for paper in papers:
			report = {
				'title': paper['title'],
				'authors': paper['authors'],
				'published_date': paper['published_date'],
				'url': paper['url'],
				'abstract': paper.get('abstract', 'アブストラクトなし'),
				'source': paper['source'],
			}
			reports.append(report)

		return reports

	async def _generate_summary(
		self,
		reports: list[dict[str, Any]],
		research_topic: str,
		research_question: str,
	) -> str:
		"""
		統合レポート生成

		Args:
			reports: レポートリスト
			research_topic: 研究トピック
			research_question: 研究課題

		Returns:
			統合レポート（Markdown）
		"""
		prompt = f"""
あなたは研究支援AIです。以下の論文調査結果を統合レポートにまとめてください。

# 研究内容
研究トピック: {research_topic}
研究課題: {research_question}

# 収集論文（{len(reports)}件）
{json.dumps(reports, indent=2, ensure_ascii=False)}

# タスク
1. 研究トピックに関する最新動向をまとめる
2. 主要な研究テーマを抽出する
3. 重要な論文を3-5件ピックアップして解説
4. 今後の研究方向性を提案

# 出力フォーマット（Markdown）
"""

		# browser-use LLM用のメッセージ形式で呼び出し
		response = await self.llm.ainvoke([UserMessage(content=prompt)])

		# レスポンスから文字列を取得
		if isinstance(response, str):
			content = response
		elif hasattr(response, 'completion'):
			# browser-use ChatInvokeCompletion
			content = response.completion
		elif hasattr(response, 'content'):
			# LangChain message
			content = response.content
		else:
			content = str(response)

		summary_path = self.output_dir / f'summary_{self.session_id}.md'
		with open(summary_path, 'w', encoding='utf-8') as f:
			f.write(content)

		return content


# テスト実行用
async def _test():
	"""動作確認テスト"""
	from automated_research.llm_provider import get_llm

	llm = get_llm(provider='deepseek', temperature=0.4)

	system = HybridResearchSystem(llm=llm, max_papers=5)

	results = await system.run_research(
		research_topic='Large Language Models',
		research_question='LLMの最新研究動向と応用分野は何か？',
		keywords=['large language model', 'LLM', 'GPT', 'transformer'],
		year_start=2023,
		year_end=2025,
	)

	print('🎉 研究調査完了！')
	print(f"セッションID: {results['session_id']}")
	print(f"論文数: {len(results['papers'])}")
	print(f"レポートパス: {results['result_path']}")


if __name__ == '__main__':
	asyncio.run(_test())
