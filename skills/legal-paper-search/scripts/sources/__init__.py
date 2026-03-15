# 数据源适配器

from .arxiv_source import ArxivSource
from .core_source import CoreSource
from .semantic_scholar_source import SemanticScholarSource
from .lawarxiv_source import LawArXivSource
from .ssrn_source import SSRNSource
from .doaj_source import DOAJSource

__all__ = [
    'ArxivSource',
    'CoreSource',
    'SemanticScholarSource',
    'LawArXivSource',
    'SSRNSource',
    'DOAJSource',
]
