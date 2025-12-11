"""
Source Registry - ソースの登録・管理・検索
"""

import asyncio
import logging
from typing import Any

from .base import BaseSource, SearchResult, SourceCategory, SourceInfo

logger = logging.getLogger(__name__)


class SourceRegistry:
	"""
	情報源レジストリ

	使い方:
		registry = SourceRegistry()
		registry.register(PerplexitySource(api_key="..."))
		registry.register(UNHCRSource())

		# 全ソースで検索
		results = await registry.search("climate refugees")

		# 特定ソースで検索
		results = await registry.search("human rights", source_ids=["amnesty", "hrw"])

		# カテゴリで検索
		results = await registry.search_by_category("migration", SourceCategory.INTERNATIONAL_ORG)
	"""

	def __init__(self):
		self._sources: dict[str, BaseSource] = {}

	def register(self, source: BaseSource) -> None:
		"""ソースを登録"""
		source_id = source.info.id
		if source_id in self._sources:
			logger.warning(f"Source '{source_id}' already registered, overwriting")
		self._sources[source_id] = source
		logger.info(f"Registered source: {source_id} ({source.info.name})")

	def unregister(self, source_id: str) -> bool:
		"""ソースを削除"""
		if source_id in self._sources:
			del self._sources[source_id]
			return True
		return False

	def get(self, source_id: str) -> BaseSource | None:
		"""IDでソースを取得"""
		return self._sources.get(source_id)

	def list_sources(self) -> list[SourceInfo]:
		"""登録済みソース一覧"""
		return [s.info for s in self._sources.values()]

	def get_by_category(self, category: SourceCategory) -> list[BaseSource]:
		"""カテゴリでソースを取得"""
		return [s for s in self._sources.values() if s.info.category == category]

	async def search(
		self,
		query: str,
		source_ids: list[str] | None = None,
		max_results_per_source: int = 10,
		**kwargs,
	) -> dict[str, list[SearchResult]]:
		"""
		検索を実行

		Args:
			query: 検索クエリ
			source_ids: 使用するソースID（Noneで全ソース）
			max_results_per_source: ソースあたりの最大結果数

		Returns:
			{source_id: [SearchResult, ...]} の辞書
		"""
		if source_ids:
			sources = [self._sources[sid] for sid in source_ids if sid in self._sources]
		else:
			sources = list(self._sources.values())

		if not sources:
			logger.warning("No sources available for search")
			return {}

		# 並列検索
		async def _search_one(source: BaseSource) -> tuple[str, list[SearchResult]]:
			try:
				results = await source.search(query, max_results=max_results_per_source, **kwargs)
				return source.info.id, results
			except Exception as e:
				logger.error(f"Search failed for {source.info.id}: {e}")
				return source.info.id, []

		tasks = [_search_one(s) for s in sources]
		results_list = await asyncio.gather(*tasks)

		return {sid: results for sid, results in results_list}

	async def search_by_category(
		self,
		query: str,
		category: SourceCategory,
		max_results_per_source: int = 10,
		**kwargs,
	) -> dict[str, list[SearchResult]]:
		"""カテゴリ内のソースで検索"""
		sources = self.get_by_category(category)
		source_ids = [s.info.id for s in sources]
		return await self.search(query, source_ids=source_ids, max_results_per_source=max_results_per_source, **kwargs)

	def __len__(self) -> int:
		return len(self._sources)

	def __contains__(self, source_id: str) -> bool:
		return source_id in self._sources
