"""
Base classes for pluggable sources
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SourceCategory(str, Enum):
	"""情報源カテゴリ"""
	ACADEMIC = "academic"              # arXiv, IEEE, Semantic Scholar
	GOVERNMENT = "government"          # 各国政府
	INTERNATIONAL_ORG = "intl_org"     # UN, WHO, UNHCR
	HUMAN_RIGHTS = "human_rights"      # Amnesty, HRW
	THINK_TANK = "think_tank"          # Brookings, RAND, CFR
	NEWS = "news"                      # Reuters, AP
	GENERAL = "general"                # Perplexity (汎用)


@dataclass
class SearchResult:
	"""検索結果"""
	title: str
	url: str
	snippet: str
	source_id: str
	source_name: str
	published_date: datetime | None = None
	authors: list[str] = field(default_factory=list)
	metadata: dict[str, Any] = field(default_factory=dict)

	def to_dict(self) -> dict[str, Any]:
		return {
			'title': self.title,
			'url': self.url,
			'snippet': self.snippet,
			'source_id': self.source_id,
			'source_name': self.source_name,
			'published_date': self.published_date.isoformat() if self.published_date else None,
			'authors': self.authors,
			'metadata': self.metadata,
		}


@dataclass
class SourceInfo:
	"""ソース情報"""
	id: str
	name: str
	category: SourceCategory
	description: str
	domains: list[str] = field(default_factory=list)  # 関連ドメイン
	requires_api_key: bool = False


class BaseSource(ABC):
	"""情報源の基底クラス - これを継承して新規ソースを追加"""

	@property
	@abstractmethod
	def info(self) -> SourceInfo:
		"""ソース情報を返す"""
		pass

	@abstractmethod
	async def search(self, query: str, max_results: int = 10, **kwargs) -> list[SearchResult]:
		"""
		検索を実行

		Args:
			query: 検索クエリ
			max_results: 最大取得件数
			**kwargs: ソース固有のオプション

		Returns:
			SearchResult のリスト
		"""
		pass

	async def is_available(self) -> bool:
		"""ソースが利用可能か確認（APIキー検証等）"""
		return True

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} id={self.info.id}>"
