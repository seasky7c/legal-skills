"""
COCA-PPT - 智能 PPT 生成技能

自动识别 PPT 模板版式并匹配内容生成演示文稿
"""

__version__ = "0.1.0"
__author__ = "seasky7"

from .loader import TemplateLoader, ContentLoader
from .analyzer import LayoutAnalyzer, ContentAnalyzer, LayoutMatcher
from .generator import SlideAssembler, ContentApplier, SlideValidator

__all__ = [
    "TemplateLoader",
    "ContentLoader",
    "LayoutAnalyzer",
    "ContentAnalyzer",
    "LayoutMatcher",
    "SlideAssembler",
    "ContentApplier",
    "SlideValidator",
]
