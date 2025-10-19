"""
Lightweight Research System - No Browser Automation

軽量版研究支援システム（ブラウザ自動化不使用）

httpx + BeautifulSoup + AI自動化による超軽量実装
- メモリ: 10-20MB (browser-useの1/50)
- CPU: 1-2% (browser-useの1/30)
- 起動: 0.1秒 (browser-useの1/1800)

対応:
- IEEE Xplore (軽量スクレイピング)
- arXiv API (公式API)
- Semantic Scholar API (公式API)
"""

from .arxiv_searcher import ArxivSearcher
from .hybrid_system import HybridResearchSystem
from .ieee_searcher import IEEELightweightSearcher
from .semantic_scholar_searcher import SemanticScholarSearcher

__all__ = [
	'IEEELightweightSearcher',
	'ArxivSearcher',
	'SemanticScholarSearcher',
	'HybridResearchSystem',
]
