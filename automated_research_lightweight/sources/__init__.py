"""
Pluggable Source System - 情報源プラグインシステム

使い方:
    from automated_research_lightweight.sources import (
        SourceRegistry, PerplexitySource, SourceCategory,
        UNHCRSource, AmnestySource, get_all_sources
    )

    # 方法1: 個別登録
    registry = SourceRegistry()
    registry.register(PerplexitySource(api_key="..."))
    registry.register(UNHCRSource(api_key="..."))

    # 方法2: 全ソース一括登録
    registry = SourceRegistry()
    for source in get_all_sources(api_key="..."):
        registry.register(source)

    # 検索
    results = await registry.search("refugee crisis")

    # 特定ソースで検索
    results = await registry.search("human rights", source_ids=["amnesty", "hrw"])

    # カテゴリで検索
    results = await registry.search_by_category("migration", SourceCategory.INTERNATIONAL_ORG)

利用可能なソース:
    - PerplexitySource: 汎用Web検索
    - 国際機関: UNHCRSource, IOMSource, WHOSource, WorldBankSource, OECDSource, UNSource
    - 人権団体: AmnestySource, HRWSource, ICRCSource
    - シンクタンク: BrookingsSource, RANDSource, CFRSource, ChathamHouseSource, CarnegieSource
    - 政府: USGovSource, EUSource, UKGovSource, JapanGovSource

新規ソース追加:
    DomainFilteredSourceを継承し、DOMAINS等を設定するだけ
"""

from .base import BaseSource, SearchResult, SourceCategory, SourceInfo
from .registry import SourceRegistry
from .perplexity import PerplexitySource
from .organizations import (
	DomainFilteredSource,
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
	# ユーティリティ
	ALL_SOURCES,
	get_all_sources,
	get_sources_by_category,
)

__all__ = [
	# Base
	'BaseSource',
	'SearchResult',
	'SourceCategory',
	'SourceInfo',
	'SourceRegistry',
	'DomainFilteredSource',
	# Perplexity
	'PerplexitySource',
	# 国際機関
	'UNHCRSource',
	'IOMSource',
	'WHOSource',
	'WorldBankSource',
	'OECDSource',
	'UNSource',
	# 人権
	'AmnestySource',
	'HRWSource',
	'ICRCSource',
	# シンクタンク
	'BrookingsSource',
	'RANDSource',
	'CFRSource',
	'ChathamHouseSource',
	'CarnegieSource',
	# 政府
	'USGovSource',
	'EUSource',
	'UKGovSource',
	'JapanGovSource',
	# ユーティリティ
	'ALL_SOURCES',
	'get_all_sources',
	'get_sources_by_category',
]
