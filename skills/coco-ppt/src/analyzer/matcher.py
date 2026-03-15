"""
匹配引擎 - 内容与版式智能匹配
"""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from .layout_analyzer import LayoutProfile
from .content_analyzer import SlideRequirement, ContentRequirements

logger = logging.getLogger(__name__)


@dataclass
class LayoutMatch:
    """版式匹配结果"""
    slide_index: int
    requirement: SlideRequirement
    matched_layout: LayoutProfile
    score: float
    score_details: Dict[str, float]
    rank: int


class LayoutMatcher:
    """内容与版式智能匹配"""
    
    def __init__(self):
        """初始化匹配引擎"""
        self.matches: List[LayoutMatch] = []
        self.weights = {
            'structure': 0.40,  # 结构匹配 40%
            'capacity': 0.30,   # 容量匹配 30%
            'semantic': 0.20,   # 语义匹配 20%
            'visual': 0.10      # 视觉匹配 10%
        }
    
    def match_all(self, 
                  requirements: List[SlideRequirement],
                  layouts: List[LayoutProfile]) -> List[LayoutMatch]:
        """
        为所有内容匹配最佳版式
        
        Args:
            requirements: 内容需求列表
            layouts: 版式档案列表
            
        Returns:
            匹配结果列表
        """
        self.matches = []
        
        for req in requirements:
            match = self.match(req, layouts)
            if match:
                self.matches.append(match)
        
        # 分配排名
        self._assign_ranks()
        
        logger.info(f"匹配完成：{len(self.matches)}个匹配")
        return self.matches
    
    def match(self, 
              requirement: SlideRequirement,
              layouts: List[LayoutProfile]) -> Optional[LayoutMatch]:
        """
        为单个内容需求匹配最佳版式
        
        Args:
            requirement: 内容需求
            layouts: 版式档案列表
            
        Returns:
            最佳匹配结果
        """
        if not layouts:
            return None
        
        # 计算所有版式的分数
        scored_layouts = []
        for layout in layouts:
            score, details = self.score(requirement.requirements, layout)
            scored_layouts.append((layout, score, details))
        
        # 排序并选择最佳
        scored_layouts.sort(key=lambda x: x[1], reverse=True)
        best_layout, best_score, best_details = scored_layouts[0]
        
        logger.debug(f"Slide {requirement.slide_index}: 最佳匹配 {best_layout.layout_type} "
                    f"(分数：{best_score:.2f})")
        
        return LayoutMatch(
            slide_index=requirement.slide_index,
            requirement=requirement,
            matched_layout=best_layout,
            score=best_score,
            score_details=best_details,
            rank=0  # 稍后分配
        )
    
    def score(self, 
              content: ContentRequirements,
              layout: LayoutProfile) -> Tuple[float, Dict[str, float]]:
        """
        计算内容与版式的匹配分数
        
        Args:
            content: 内容需求
            layout: 版式档案
            
        Returns:
            (总分, 各维度分数详情)
        """
        scores = {}
        
        # 1. 结构匹配 (40 分)
        structure_score = self._score_structure(content, layout)
        scores['structure'] = structure_score
        
        # 2. 容量匹配 (30 分)
        capacity_score = self._score_capacity(content, layout)
        scores['capacity'] = capacity_score
        
        # 3. 语义匹配 (20 分)
        semantic_score = self._score_semantic(content, layout)
        scores['semantic'] = semantic_score
        
        # 4. 视觉匹配 (10 分)
        visual_score = self._score_visual(content, layout)
        scores['visual'] = visual_score
        
        # 加权总分
        total_score = sum(
            scores[dim] * self.weights[dim]
            for dim in self.weights
        )
        
        return total_score, scores
    
    def _score_structure(self, content: ContentRequirements, layout: LayoutProfile) -> float:
        """
        结构匹配评分 (0-100)
        
        考虑:
        - 列数匹配 (15 分)
        - 形状数量匹配 (15 分)
        - 占位符类型匹配 (10 分)
        """
        score = 0.0
        features = layout.features
        
        # 列数匹配 (15 分)
        if content.column_count == features.column_count:
            score += 15.0
        elif abs(content.column_count - features.column_count) == 1:
            score += 8.0
        
        # 形状数量匹配 (15 分)
        if content.text_shapes == features.text_shape_count:
            score += 15.0
        elif abs(content.text_shapes - features.text_shape_count) <= 1:
            score += 8.0
        
        # 占位符类型匹配 (10 分)
        if content.title and features.has_title:
            score += 5.0
        
        if content.content_type in ['bullets', 'text'] and features.has_body:
            score += 5.0
        
        return score
    
    def _score_capacity(self, content: ContentRequirements, layout: LayoutProfile) -> float:
        """
        容量匹配评分 (0-100)
        
        考虑:
        - 标题长度适配 (15 分)
        - 正文长度适配 (15 分)
        """
        score = 0.0
        capacity = layout.features.estimated_capacity
        
        if not capacity:
            # 如果没有容量估计，给平均分
            return 15.0
        
        # 标题长度适配 (15 分)
        if content.title_length > 0 and capacity.title_max_chars > 0:
            title_ratio = content.title_length / capacity.title_max_chars
            if title_ratio <= 1.0:
                score += 15.0
            elif title_ratio <= 1.2:
                score += 10.0
            elif title_ratio <= 1.5:
                score += 5.0
        else:
            score += 15.0  # 没有标题，不扣分
        
        # 正文长度适配 (15 分)
        if content.total_chars > 0 and capacity.body_max_lines > 0:
            # 估算行数 (假设每行约 30 字符)
            estimated_lines = content.total_chars / 30
            body_ratio = estimated_lines / capacity.body_max_lines
            
            if body_ratio <= 1.0:
                score += 15.0
            elif body_ratio <= 1.2:
                score += 10.0
            elif body_ratio <= 1.5:
                score += 5.0
        else:
            score += 15.0
        
        return score
    
    def _score_semantic(self, content: ContentRequirements, layout: LayoutProfile) -> float:
        """
        语义匹配评分 (0-100)
        
        考虑:
        - 内容类型匹配 (10 分)
        - 版式用途匹配 (10 分)
        """
        score = 0.0
        
        # 内容类型匹配 (10 分)
        type_mapping = {
            'title': ['TITLE_SLIDE'],
            'bullets': ['BULLET_LIST', 'CONTENT_WITH_CAPTION'],
            'quote': ['QUOTE'],
            'comparison': ['TWO_COLUMN', 'THREE_COLUMN'],
            'text': ['CONTENT', 'CONTENT_WITH_CAPTION', 'BULLET_LIST']
        }
        
        compatible_types = type_mapping.get(content.content_type, [])
        if layout.layout_type in compatible_types:
            score += 10.0
        elif layout.layout_type == 'CONTENT':
            score += 5.0  # 通用版式
        
        # 版式用途匹配 (10 分)
        section_mapping = {
            'title': ['TITLE_SLIDE'],
            'section': ['SECTION_HEADER', 'TITLE_SLIDE'],
            'quote': ['QUOTE'],
            'content': ['BULLET_LIST', 'TWO_COLUMN', 'CONTENT_WITH_CAPTION', 'CONTENT']
        }
        
        compatible_sections = section_mapping.get(content.section_type, [])
        if layout.layout_type in compatible_sections:
            score += 10.0
        
        return score
    
    def _score_visual(self, content: ContentRequirements, layout: LayoutProfile) -> float:
        """
        视觉匹配评分 (0-100)
        
        考虑:
        - 对称性偏好 (5 分)
        - 视觉权重分布 (5 分)
        """
        score = 0.0
        features = layout.features
        
        # 对称性偏好 (5 分)
        if content.prefers_symmetry:
            if features.layout_symmetry == 'symmetric':
                score += 5.0
        else:
            score += 5.0  # 不要求对称，不扣分
        
        # 视觉权重分布 (5 分)
        # 简化处理：如果有特定偏好则评分
        if content.visual_preference:
            # TODO: 实现详细的视觉权重匹配
            score += 2.5
        else:
            score += 5.0
        
        return score
    
    def _assign_ranks(self):
        """分配排名"""
        # 按分数排序
        self.matches.sort(key=lambda m: m.score, reverse=True)
        
        # 分配排名
        for i, match in enumerate(self.matches):
            match.rank = i + 1
    
    def get_matches_by_layout_type(self, layout_type: str) -> List[LayoutMatch]:
        """
        根据版式类型获取匹配
        
        Args:
            layout_type: 版式类型
            
        Returns:
            匹配结果列表
        """
        return [m for m in self.matches if m.matched_layout.layout_type == layout_type]
    
    def get_low_confidence_matches(self, threshold: float = 0.7) -> List[LayoutMatch]:
        """
        获取低置信度匹配
        
        Args:
            threshold: 置信度阈值
            
        Returns:
            低置信度匹配列表
        """
        return [m for m in self.matches if m.score < threshold * 100]
    
    def export_matches(self) -> List[Dict]:
        """
        导出匹配结果为字典列表
        
        Returns:
            匹配字典列表
        """
        return [
            {
                'slide_index': m.slide_index,
                'rank': m.rank,
                'score': m.score,
                'score_details': m.score_details,
                'matched_layout': {
                    'slide_index': m.matched_layout.slide_index,
                    'layout_type': m.matched_layout.layout_type,
                    'description': m.matched_layout.description
                },
                'requirement': {
                    'title': m.requirement.requirements.title,
                    'content_type': m.requirement.requirements.content_type,
                }
            }
            for m in self.matches
        ]
    
    def generate_report(self) -> str:
        """
        生成匹配报告
        
        Returns:
            报告文本
        """
        lines = [
            "=" * 60,
            "COCO-PPT 版式匹配报告",
            "=" * 60,
            "",
            f"总幻灯片数：{len(self.matches)}",
            f"平均匹配分数：{sum(m.score for m in self.matches) / len(self.matches):.2f}" if self.matches else "N/A",
            "",
            "-" * 60,
            "匹配详情",
            "-" * 60,
        ]
        
        for match in self.matches:
            lines.append(f"\n幻灯片 {match.slide_index + 1} (排名 #{match.rank})")
            lines.append(f"  标题：{match.requirement.requirements.title or '(无标题)'}")
            lines.append(f"  内容类型：{match.requirement.requirements.content_type}")
            lines.append(f"  匹配版式：{match.matched_layout.layout_type}")
            lines.append(f"  使用模板页：{match.matched_layout.slide_index}")
            lines.append(f"  匹配分数：{match.score:.2f}/100")
            lines.append(f"  详情：{match.matched_layout.description}")
        
        # 低分警告
        low_conf = self.get_low_confidence_matches()
        if low_conf:
            lines.append("\n" + "-" * 60)
            lines.append("⚠️  低置信度匹配 (可能需要手动调整)")
            lines.append("-" * 60)
            for match in low_conf:
                lines.append(f"  - 幻灯片 {match.slide_index + 1}: {match.score:.2f}分")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
