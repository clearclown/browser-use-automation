"""
Perplexity API Source - 汎用Web検索 + ドメイン絞り込み
"""

import logging
import os
from datetime import datetime
from typing import Any, Literal

import httpx

from .base import BaseSource, SearchResult, SourceCategory, SourceInfo

logger = logging.getLogger(__name__)


class PerplexitySource(BaseSource):
	"""
	Perplexity Sonar API を使った汎用検索

	特徴:
	- リアルタイムWeb検索
	- ドメインフィルタリング対応
	- 引用元URL付き

	使い方:
		source = PerplexitySource(api_key="pplx-...")

		# 汎用検索
		results = await source.search("climate change policy")

		# 特定ドメインに絞る
		results = await source.search(
			"refugee statistics",
			domain_filter=["unhcr.org", "iom.int"]
		)
	"""

	API_URL = "https://api.perplexity.ai/chat/completions"

	def __init__(
		self,
		api_key: str | None = None,
		model: str = "sonar",  # "sonar" or "sonar-pro"
	):
		self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
		self.model = model
		self._client = httpx.AsyncClient(timeout=60.0)

	@property
	def info(self) -> SourceInfo:
		return SourceInfo(
			id="perplexity",
			name="Perplexity Sonar",
			category=SourceCategory.GENERAL,
			description="AI-powered web search with real-time results and citations",
			requires_api_key=True,
		)

	async def is_available(self) -> bool:
		return bool(self.api_key)

	async def search(
		self,
		query: str,
		max_results: int = 10,
		domain_filter: list[str] | None = None,
		recency_filter: Literal["month", "week", "day", "hour"] | None = None,
		**kwargs,
	) -> list[SearchResult]:
		"""
		Perplexity APIで検索

		Args:
			query: 検索クエリ
			max_results: 最大結果数（Perplexityは内部で制限）
			domain_filter: 絞り込むドメインリスト
			recency_filter: 期間フィルタ
		"""
		if not self.api_key:
			logger.error("Perplexity API key not set")
			return []

		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
		}

		# システムプロンプト: 検索結果を構造化して返すよう指示
		system_prompt = """You are a research assistant. Search for information and return results in a structured format.
For each relevant source found, provide:
- Title
- URL
- Brief summary (2-3 sentences)

Focus on authoritative and primary sources."""

		payload: dict[str, Any] = {
			"model": self.model,
			"messages": [
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": f"Search and summarize key sources about: {query}"},
			],
			"return_citations": True,
			"return_related_questions": False,
		}

		if domain_filter:
			payload["search_domain_filter"] = domain_filter

		if recency_filter:
			payload["search_recency_filter"] = recency_filter

		try:
			response = await self._client.post(self.API_URL, json=payload, headers=headers)
			response.raise_for_status()
			data = response.json()

			return self._parse_response(data)

		except httpx.HTTPStatusError as e:
			logger.error(f"Perplexity API error: {e.response.status_code} - {e.response.text}")
			return []
		except Exception as e:
			logger.error(f"Perplexity search failed: {e}")
			return []

	def _parse_response(self, data: dict[str, Any]) -> list[SearchResult]:
		"""APIレスポンスをSearchResultに変換"""
		results = []

		# citations から URL と内容を抽出
		citations = data.get("citations", [])
		content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

		for i, url in enumerate(citations):
			# URL からタイトルを推測（実際のタイトルはコンテンツから抽出が必要）
			title = self._extract_title_from_url(url)

			results.append(SearchResult(
				title=title,
				url=url,
				snippet=f"Citation {i + 1} from Perplexity search",
				source_id=self.info.id,
				source_name=self.info.name,
				metadata={"full_response": content if i == 0 else None},
			))

		return results

	def _extract_title_from_url(self, url: str) -> str:
		"""URLからタイトルを推測"""
		from urllib.parse import urlparse
		parsed = urlparse(url)
		path = parsed.path.strip("/").split("/")[-1] if parsed.path else ""
		# ファイル名やパスから読みやすいタイトルを生成
		title = path.replace("-", " ").replace("_", " ").replace(".html", "").replace(".pdf", "")
		return title.title() if title else parsed.netloc

	async def close(self):
		await self._client.aclose()
