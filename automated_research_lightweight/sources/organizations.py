"""
Pre-configured organization sources
Perplexity APIのドメインフィルタを活用した各種組織ソース
"""

import os
from typing import Literal

from .base import BaseSource, SearchResult, SourceCategory, SourceInfo
from .perplexity import PerplexitySource


class DomainFilteredSource(BaseSource):
	"""
	Perplexityのドメインフィルタを使った特定組織ソース

	新規組織の追加:
		class MyOrgSource(DomainFilteredSource):
			SOURCE_ID = "my_org"
			SOURCE_NAME = "My Organization"
			CATEGORY = SourceCategory.THINK_TANK
			DESCRIPTION = "..."
			DOMAINS = ["myorg.org", "myorg.com"]
	"""

	SOURCE_ID: str = ""
	SOURCE_NAME: str = ""
	CATEGORY: SourceCategory = SourceCategory.GENERAL
	DESCRIPTION: str = ""
	DOMAINS: list[str] = []

	def __init__(self, perplexity_api_key: str | None = None):
		self._api_key = perplexity_api_key or os.getenv("PERPLEXITY_API_KEY")
		self._perplexity: PerplexitySource | None = None

	def _get_perplexity(self) -> PerplexitySource:
		if self._perplexity is None:
			self._perplexity = PerplexitySource(api_key=self._api_key)
		return self._perplexity

	@property
	def info(self) -> SourceInfo:
		return SourceInfo(
			id=self.SOURCE_ID,
			name=self.SOURCE_NAME,
			category=self.CATEGORY,
			description=self.DESCRIPTION,
			domains=self.DOMAINS,
			requires_api_key=True,
		)

	async def is_available(self) -> bool:
		return bool(self._api_key)

	async def search(
		self,
		query: str,
		max_results: int = 10,
		recency_filter: Literal["month", "week", "day", "hour"] | None = None,
		**kwargs,
	) -> list[SearchResult]:
		perplexity = self._get_perplexity()
		results = await perplexity.search(
			query=query,
			max_results=max_results,
			domain_filter=self.DOMAINS,
			recency_filter=recency_filter,
		)
		# ソース情報を上書き
		for r in results:
			r.source_id = self.SOURCE_ID
			r.source_name = self.SOURCE_NAME
		return results


# ============================================================
# 国際機関 (International Organizations)
# ============================================================

class UNHCRSource(DomainFilteredSource):
	"""国連難民高等弁務官事務所"""
	SOURCE_ID = "unhcr"
	SOURCE_NAME = "UNHCR"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "UN Refugee Agency - refugee statistics, reports, and policy documents"
	DOMAINS = ["unhcr.org", "data.unhcr.org", "globalcompactrefugees.org"]


class IOMSource(DomainFilteredSource):
	"""国際移住機関"""
	SOURCE_ID = "iom"
	SOURCE_NAME = "IOM"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "International Organization for Migration - migration data and research"
	DOMAINS = ["iom.int", "migrationdataportal.org"]


class WHOSource(DomainFilteredSource):
	"""世界保健機関"""
	SOURCE_ID = "who"
	SOURCE_NAME = "WHO"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "World Health Organization - health guidelines, research, and statistics"
	DOMAINS = ["who.int", "apps.who.int"]


class WorldBankSource(DomainFilteredSource):
	"""世界銀行"""
	SOURCE_ID = "worldbank"
	SOURCE_NAME = "World Bank"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "World Bank - development data, research, and reports"
	DOMAINS = ["worldbank.org", "data.worldbank.org", "documents.worldbank.org"]


class OECDSource(DomainFilteredSource):
	"""経済協力開発機構"""
	SOURCE_ID = "oecd"
	SOURCE_NAME = "OECD"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "Organisation for Economic Co-operation and Development"
	DOMAINS = ["oecd.org", "oecd-ilibrary.org", "data.oecd.org"]


class UNSource(DomainFilteredSource):
	"""国連本部"""
	SOURCE_ID = "un"
	SOURCE_NAME = "United Nations"
	CATEGORY = SourceCategory.INTERNATIONAL_ORG
	DESCRIPTION = "United Nations - resolutions, reports, and official documents"
	DOMAINS = ["un.org", "undocs.org", "documents-dds-ny.un.org"]


# ============================================================
# 人権団体 (Human Rights Organizations)
# ============================================================

class AmnestySource(DomainFilteredSource):
	"""アムネスティ・インターナショナル"""
	SOURCE_ID = "amnesty"
	SOURCE_NAME = "Amnesty International"
	CATEGORY = SourceCategory.HUMAN_RIGHTS
	DESCRIPTION = "Human rights research, reports, and campaigns"
	DOMAINS = ["amnesty.org", "amnesty.org.uk", "amnestyusa.org"]


class HRWSource(DomainFilteredSource):
	"""ヒューマン・ライツ・ウォッチ"""
	SOURCE_ID = "hrw"
	SOURCE_NAME = "Human Rights Watch"
	CATEGORY = SourceCategory.HUMAN_RIGHTS
	DESCRIPTION = "Human rights investigations and advocacy"
	DOMAINS = ["hrw.org"]


class ICRCSource(DomainFilteredSource):
	"""赤十字国際委員会"""
	SOURCE_ID = "icrc"
	SOURCE_NAME = "ICRC"
	CATEGORY = SourceCategory.HUMAN_RIGHTS
	DESCRIPTION = "International Committee of the Red Cross - humanitarian law and protection"
	DOMAINS = ["icrc.org"]


# ============================================================
# シンクタンク (Think Tanks)
# ============================================================

class BrookingsSource(DomainFilteredSource):
	"""ブルッキングス研究所"""
	SOURCE_ID = "brookings"
	SOURCE_NAME = "Brookings Institution"
	CATEGORY = SourceCategory.THINK_TANK
	DESCRIPTION = "Public policy research organization"
	DOMAINS = ["brookings.edu"]


class RANDSource(DomainFilteredSource):
	"""RAND研究所"""
	SOURCE_ID = "rand"
	SOURCE_NAME = "RAND Corporation"
	CATEGORY = SourceCategory.THINK_TANK
	DESCRIPTION = "Research and analysis for public policy"
	DOMAINS = ["rand.org"]


class CFRSource(DomainFilteredSource):
	"""外交問題評議会"""
	SOURCE_ID = "cfr"
	SOURCE_NAME = "Council on Foreign Relations"
	CATEGORY = SourceCategory.THINK_TANK
	DESCRIPTION = "Foreign policy and international affairs"
	DOMAINS = ["cfr.org"]


class ChathamHouseSource(DomainFilteredSource):
	"""チャタムハウス"""
	SOURCE_ID = "chatham_house"
	SOURCE_NAME = "Chatham House"
	CATEGORY = SourceCategory.THINK_TANK
	DESCRIPTION = "Royal Institute of International Affairs"
	DOMAINS = ["chathamhouse.org"]


class CarnegieSource(DomainFilteredSource):
	"""カーネギー国際平和基金"""
	SOURCE_ID = "carnegie"
	SOURCE_NAME = "Carnegie Endowment"
	CATEGORY = SourceCategory.THINK_TANK
	DESCRIPTION = "Carnegie Endowment for International Peace"
	DOMAINS = ["carnegieendowment.org", "carnegie.ru", "carnegieeurope.eu"]


# ============================================================
# 政府機関 (Government)
# ============================================================

class USGovSource(DomainFilteredSource):
	"""米国政府"""
	SOURCE_ID = "us_gov"
	SOURCE_NAME = "U.S. Government"
	CATEGORY = SourceCategory.GOVERNMENT
	DESCRIPTION = "U.S. federal government publications and data"
	DOMAINS = ["gov", "state.gov", "whitehouse.gov", "congress.gov", "gao.gov"]


class EUSource(DomainFilteredSource):
	"""EU"""
	SOURCE_ID = "eu"
	SOURCE_NAME = "European Union"
	CATEGORY = SourceCategory.GOVERNMENT
	DESCRIPTION = "EU institutions, law, and publications"
	DOMAINS = ["europa.eu", "eur-lex.europa.eu", "ec.europa.eu"]


class UKGovSource(DomainFilteredSource):
	"""英国政府"""
	SOURCE_ID = "uk_gov"
	SOURCE_NAME = "UK Government"
	CATEGORY = SourceCategory.GOVERNMENT
	DESCRIPTION = "UK government publications and statistics"
	DOMAINS = ["gov.uk", "parliament.uk"]


class JapanGovSource(DomainFilteredSource):
	"""日本政府"""
	SOURCE_ID = "japan_gov"
	SOURCE_NAME = "日本政府"
	CATEGORY = SourceCategory.GOVERNMENT
	DESCRIPTION = "Japanese government ministries and agencies"
	DOMAINS = ["go.jp", "e-gov.go.jp", "mofa.go.jp", "mhlw.go.jp"]


# ============================================================
# 便利関数
# ============================================================

ALL_SOURCES = [
	# 国際機関
	UNHCRSource,
	IOMSource,
	WHOSource,
	WorldBankSource,
	OECDSource,
	UNSource,
	# 人権
	AmnestySource,
	HRWSource,
	ICRCSource,
	# シンクタンク
	BrookingsSource,
	RANDSource,
	CFRSource,
	ChathamHouseSource,
	CarnegieSource,
	# 政府
	USGovSource,
	EUSource,
	UKGovSource,
	JapanGovSource,
]


def get_all_sources(api_key: str | None = None) -> list[BaseSource]:
	"""全ソースのインスタンスを取得"""
	return [cls(perplexity_api_key=api_key) for cls in ALL_SOURCES]


def get_sources_by_category(category: SourceCategory, api_key: str | None = None) -> list[BaseSource]:
	"""カテゴリでソースを取得"""
	return [cls(perplexity_api_key=api_key) for cls in ALL_SOURCES if cls.CATEGORY == category]
