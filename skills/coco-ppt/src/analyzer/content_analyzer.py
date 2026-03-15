"""
内容分析器 - 分析演讲大纲和内容结构
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from ..loader.content_loader import PresentationContent, SlideContent

logger = logging.getLogger(__name__)


@dataclass
class ContentRequirements:
    """内容需求"""
    slide_type: str = "auto"
    title: str = ""
    title_length: int = 0
    content_type: str = "text"  # text, bullets, quote, comparison
    column_count: int = 1
    text_shapes: int = 1
    has_bullets: bool = False
    bullet_count: int = 0
    content_length: str = "short"  # short, medium, long
    total_chars: int = 0
    section_type: str = "content"  # title, section, content, quote
    prefers_symmetry: bool = False
    visual_preference: Dict[str, float] = field(default_factory=dict)


@dataclass
class SlideRequirement:
    """单张幻灯片需求"""
    slide_index: int
    requirements: ContentRequirements
    content: SlideContent


class ContentAnalyzer:
    """分析演讲大纲和内容结构"""
    
    def __init__(self):
        """初始化内容分析器"""
        self.requirements: List[SlideRequirement] = []
    
    def analyze(self, content: PresentationContent) -> List[SlideRequirement]:
        """
        分析内容并提取需求
        
        Args:
            content: PresentationContent 对象
            
        Returns:
            需求列表
        """
        self.requirements = []
        
        for idx, slide_content in enumerate(content.slides):
            req = self._analyze_slide(slide_content, idx)
            self.requirements.append(req)
        
        logger.info(f"内容分析完成：{len(self.requirements)}个需求")
        return self.requirements
    
    def _analyze_slide(self, slide_content: SlideContent, index: int) -> SlideRequirement:
        """
        分析单张幻灯片内容
        
        Args:
            slide_content: 幻灯片内容
            index: 索引
            
        Returns:
            SlideRequirement 对象
        """
        requirements = ContentRequirements(
            slide_type=slide_content.slide_type,
            title=slide_content.title,
            title_length=len(slide_content.title),
        )
        
        # 分析内容类型
        if slide_content.slide_type == 'title':
            requirements.section_type = 'title'
            requirements.content_type = 'text'
            requirements.text_shapes = 1 if not slide_content.subtitle else 2
        
        elif slide_content.slide_type == 'section_header':
            requirements.section_type = 'section'
            requirements.content_type = 'text'
            requirements.text_shapes = 1
        
        elif slide_content.slide_type == 'bullets':
            requirements.section_type = 'content'
            requirements.content_type = 'bullets'
            requirements.has_bullets = True
            requirements.bullet_count = len(slide_content.items)
            requirements.text_shapes = 2 if slide_content.title else 1  # title + body
            requirements.column_count = 1
        
        elif slide_content.slide_type == 'two_column':
            requirements.section_type = 'content'
            requirements.content_type = 'comparison'
            requirements.column_count = 2
            requirements.text_shapes = 3 if slide_content.title else 2  # title + left + right
            requirements.prefers_symmetry = True
        
        elif slide_content.slide_type == 'quote':
            requirements.section_type = 'quote'
            requirements.content_type = 'quote'
            requirements.text_shapes = 2  # quote + author
            requirements.prefers_symmetry = True
        
        elif slide_content.slide_type == 'content':
            requirements.section_type = 'content'
            requirements.content_type = 'text'
            
            # 根据内容长度判断
            total_chars = len(slide_content.content)
            requirements.total_chars = total_chars
            
            if total_chars < 100:
                requirements.content_length = 'short'
            elif total_chars < 500:
                requirements.content_length = 'medium'
            else:
                requirements.content_length = 'long'
                requirements.text_shapes = 2  # title + body
        
        # 计算总字符数
        if not requirements.total_chars:
            total = requirements.title_length
            if slide_content.items:
                total += sum(len(item) for item in slide_content.items)
            if slide_content.content:
                total += len(slide_content.content)
            if slide_content.quote:
                total += len(slide_content.quote)
            requirements.total_chars = total
        
        # 根据总字符数调整内容长度
        if not requirements.content_length:
            if requirements.total_chars < 50:
                requirements.content_length = 'short'
            elif requirements.total_chars < 300:
                requirements.content_length = 'medium'
            else:
                requirements.content_length = 'long'
        
        return SlideRequirement(
            slide_index=index,
            requirements=requirements,
            content=slide_content
        )
    
    def get_requirements_by_type(self, content_type: str) -> List[SlideRequirement]:
        """
        根据内容类型获取需求
        
        Args:
            content_type: 内容类型
            
        Returns:
            需求列表
        """
        return [r for r in self.requirements if r.requirements.content_type == content_type]
    
    def export_requirements(self) -> List[Dict]:
        """
        导出需求为字典列表
        
        Returns:
            需求字典列表
        """
        return [
            {
                'slide_index': r.slide_index,
                'title': r.requirements.title,
                'slide_type': r.requirements.slide_type,
                'content_type': r.requirements.content_type,
                'column_count': r.requirements.column_count,
                'text_shapes': r.requirements.text_shapes,
                'has_bullets': r.requirements.has_bullets,
                'bullet_count': r.requirements.bullet_count,
                'content_length': r.requirements.content_length,
                'total_chars': r.requirements.total_chars,
            }
            for r in self.requirements
        ]
