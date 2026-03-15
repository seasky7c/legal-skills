"""
内容加载器 - 加载演讲大纲和内容
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SlideContent:
    """单张幻灯片内容"""
    slide_type: str = "auto"  # auto, title, bullets, two_column, quote, etc.
    title: str = ""
    subtitle: str = ""
    content: str = ""
    items: List[str] = field(default_factory=list)
    left_content: Optional[Dict] = None
    right_content: Optional[Dict] = None
    quote: str = ""
    author: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class PresentationContent:
    """演示文稿内容"""
    title: str = ""
    slides: List[SlideContent] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class ContentLoader:
    """加载演讲大纲和内容"""
    
    def __init__(self):
        """初始化内容加载器"""
        self.content: Optional[PresentationContent] = None
    
    def load_outline(self, path: str) -> PresentationContent:
        """
        加载 Markdown 格式的大纲
        
        Args:
            path: Markdown 文件路径
            
        Returns:
            PresentationContent 对象
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"大纲文件不存在：{path}")
        
        logger.info(f"加载 Markdown 大纲：{path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        self.content = self._parse_markdown(markdown_content)
        return self.content
    
    def _parse_markdown(self, markdown: str) -> PresentationContent:
        """
        解析 Markdown 内容
        
        Args:
            markdown: Markdown 文本
            
        Returns:
            PresentationContent 对象
        """
        content = PresentationContent()
        lines = markdown.split('\n')
        
        current_slide = None
        current_items = []
        in_list = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # 文档标题 (#)
            if line.startswith('# ') and line_stripped:
                if current_slide:
                    if current_items:
                        current_slide.items = current_items
                        current_items = []
                    content.slides.append(current_slide)
                
                content.title = line_stripped[2:].strip()
                current_slide = SlideContent(slide_type='title', title=content.title)
                in_list = False
                continue
            
            # 章节标题 (##)
            elif line.startswith('## ') and line_stripped:
                if current_slide:
                    if current_items:
                        current_slide.items = current_items
                        current_items = []
                    content.slides.append(current_slide)
                
                chapter_title = line_stripped[3:].strip()
                current_slide = SlideContent(
                    slide_type='section_header',
                    title=chapter_title
                )
                in_list = False
                continue
            
            # 小节标题 (###)
            elif line.startswith('### ') and line_stripped:
                if current_slide:
                    if current_items:
                        current_slide.items = current_items
                        current_items = []
                    content.slides.append(current_slide)
                
                section_title = line_stripped[4:].strip()
                current_slide = SlideContent(
                    slide_type='bullets',
                    title=section_title
                )
                current_items = []
                in_list = False
                continue
            
            # 列表项
            elif line_stripped.startswith('- ') or line_stripped.startswith('* '):
                item = line_stripped[2:].strip()
                if current_slide is None:
                    current_slide = SlideContent(slide_type='bullets')
                current_items.append(item)
                in_list = True
                continue
            
            # 引用
            elif line_stripped.startswith('> '):
                if current_slide:
                    if current_items:
                        current_slide.items = current_items
                        current_items = []
                    content.slides.append(current_slide)
                
                quote_text = line_stripped[2:].strip()
                current_slide = SlideContent(
                    slide_type='quote',
                    quote=quote_text
                )
                in_list = False
                continue
            
            # 普通段落
            elif line_stripped and not in_list:
                if current_slide is None:
                    current_slide = SlideContent(slide_type='content')
                
                if current_slide.content:
                    current_slide.content += '\n' + line_stripped
                else:
                    current_slide.content = line_stripped
                in_list = False
        
        # 添加最后一张幻灯片
        if current_slide:
            if current_items:
                current_slide.items = current_items
            content.slides.append(current_slide)
        
        logger.info(f"解析完成：{len(content.slides)}张幻灯片")
        return content
    
    def load_content(self, path: str) -> PresentationContent:
        """
        加载 JSON 格式的内容
        
        Args:
            path: JSON 文件路径
            
        Returns:
            PresentationContent 对象
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"内容文件不存在：{path}")
        
        logger.info(f"加载 JSON 内容：{path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.content = self._parse_json(data)
        return self.content
    
    def _parse_json(self, data: dict) -> PresentationContent:
        """
        解析 JSON 数据
        
        Args:
            data: JSON 数据
            
        Returns:
            PresentationContent 对象
        """
        content = PresentationContent(
            title=data.get('title', ''),
            metadata=data.get('metadata', {})
        )
        
        for slide_data in data.get('slides', []):
            slide = SlideContent(
                slide_type=slide_data.get('type', 'auto'),
                title=slide_data.get('title', ''),
                subtitle=slide_data.get('subtitle', ''),
                content=slide_data.get('content', ''),
                items=slide_data.get('items', []),
                quote=slide_data.get('quote', ''),
                author=slide_data.get('author', ''),
                left_content=slide_data.get('left'),
                right_content=slide_data.get('right'),
                metadata=slide_data.get('metadata', {})
            )
            content.slides.append(slide)
        
        logger.info(f"解析完成：{len(content.slides)}张幻灯片")
        return content
    
    def load_text(self, text: str) -> PresentationContent:
        """
        直接解析文本内容
        
        Args:
            text: 文本内容
            
        Returns:
            PresentationContent 对象
        """
        logger.info("解析文本内容")
        self.content = self._parse_markdown(text)
        return self.content
