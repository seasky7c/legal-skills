# COCO-PPT 智能 PPT 生成技能 - 架构设计

## 1. 项目概述

### 1.1 目标
创建一个智能 PPT 生成技能，能够：
1. ✅ 智能识别 PPT 模板中每一页的版式
2. ✅ 将演讲大纲/内容与版式自动匹配找到最优版式
3. ✅ 自动组装生成完整 PPT
4. ✅ 完全本地化运行，不依赖外部 API
5. ✅ 非容器化部署

### 1.2 核心理念
- **智能自动化**: 最小化用户手动操作，自动完成版式匹配
- **内容驱动**: 基于内容结构和语义选择最佳版式
- **视觉感知**: 理解版式的视觉布局（列数、图片位置等）
- **简单工作流**: 一键生成，减少中间步骤

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      COCO-PPT Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │  输入层  │───▶│  分析引擎    │───▶│   生成引擎      │   │
│  │          │    │              │    │                 │   │
│  │ • 模板   │    │ • 版式识别   │    │ • 内容匹配      │   │
│  │ • 大纲   │    │ • 内容解析   │    │ • 幻灯片组装    │   │
│  │ • 内容   │    │ • 智能推荐   │    │ • 格式应用      │   │
│  └──────────┘    └──────────────┘    └─────────────────┘   │
│        │                │                   │               │
│        ▼                ▼                   ▼               │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │ 文件加载 │    │ 特征提取     │    │ PPTX 生成       │   │
│  │ 验证     │    │ 评分排序     │    │ 质量检查        │   │
│  └──────────┘    └──────────────┘    └─────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │    输出层       │
                    │                 │
                    │ • 生成的 PPTX   │
                    │ • 生成报告      │
                    │ • 缩略图预览    │
                    └─────────────────┘
```

---

## 3. 核心模块设计

### 3.1 模块结构

```
coco-ppt/
├── SKILL.md                 # 技能说明文档
├── README.md                # 使用指南
├── requirements.txt         # Python 依赖
├── package.json            # Node.js 依赖（可选）
├── src/
│   ├── __init__.py
│   ├── main.py             # 主入口
│   ├── loader/             # 输入加载模块
│   │   ├── __init__.py
│   │   ├── template_loader.py   # 模板加载
│   │   └── content_loader.py    # 内容加载
│   ├── analyzer/           # 分析引擎
│   │   ├── __init__.py
│   │   ├── layout_analyzer.py   # 版式分析
│   │   ├── content_analyzer.py  # 内容分析
│   │   └── matcher.py           # 匹配引擎
│   ├── generator/          # 生成引擎
│   │   ├── __init__.py
│   │   ├── assembler.py        # 幻灯片组装
│   │   ├── content_applier.py  # 内容应用
│   │   └── validator.py        # 质量验证
│   └── utils/              # 工具模块
│       ├── __init__.py
│       ├── thumbnail.py        # 缩略图生成
│       └── logger.py           # 日志记录
├── scripts/                # 命令行脚本
│   ├── coco-ppt.py         # 主命令行工具
│   └── ...
├── templates/              # 示例模板（可选）
├── examples/               # 示例输入
│   ├── sample-outline.md
│   └── sample-content.json
└── logs/                   # 日志目录
```

### 3.2 核心模块详细说明

#### 模块 1: loader (输入加载)

**template_loader.py**
```python
class TemplateLoader:
    """加载和验证 PPTX 模板"""
    
    def load(self, template_path: str) -> Presentation:
        """加载 PPTX 模板文件"""
        
    def validate(self, prs: Presentation) -> TemplateValidationResult:
        """验证模板是否有效"""
        
    def get_slide_layouts(self, prs: Presentation) -> List[SlideLayout]:
        """提取所有幻灯片版式"""
```

**content_loader.py**
```python
class ContentLoader:
    """加载演讲大纲和内容"""
    
    def load_outline(self, path: str) -> Outline:
        """加载 Markdown 格式的大纲"""
        
    def load_content(self, path: str) -> Content:
        """加载 JSON 格式的内容"""
        
    def parse_text(self, text: str) -> Content:
        """解析纯文本内容"""
```

#### 模块 2: analyzer (分析引擎) ⭐核心

**layout_analyzer.py** - 版式识别
```python
class LayoutAnalyzer:
    """智能识别 PPT 模板版式"""
    
    def analyze(self, prs: Presentation) -> List[LayoutProfile]:
        """分析所有幻灯片版式"""
        
    def extract_features(self, slide: Slide) -> LayoutFeatures:
        """提取版式特征"""
        # 特征包括:
        # - 占位符类型 (TITLE, BODY, OBJECT 等)
        # - 文本形状数量
        # - 列数检测 (通过分析形状位置)
        # - 图片占位符检测
        # - 视觉权重分布
        # - 版式用途分类
        
    def classify_layout(self, features: LayoutFeatures) -> LayoutType:
        """分类版式类型"""
        # 支持的类型:
        # - TITLE_SLIDE: 封面页
        # - SECTION_HEADER: 章节页
        # - BULLET_LIST: 项目列表
        # - TWO_COLUMN: 双列对比
        # - THREE_COLUMN: 三列对比
        # - IMAGE_LEFT: 左图右文
        # - IMAGE_RIGHT: 右图左文
        # - IMAGE_TOP: 上图下文
        # - QUOTE: 引用页
        # - BLANK: 空白页
        # - CONTENT_WITH_CAPTION: 带标题的内容页
```

**layout_features.py** - 特征数据结构
```python
@dataclass
class LayoutFeatures:
    """版式特征"""
    slide_index: int
    placeholder_types: List[str]      # 占位符类型列表
    text_shape_count: int             # 文本形状数量
    image_placeholder_count: int      # 图片占位符数量
    column_count: int                 # 列数 (1-4)
    has_title: bool                   # 是否有标题
    has_body: bool                    # 是否有正文
    title_position: str               # 标题位置 (top, center, left, right)
    layout_symmetry: str              # 对称性 (symmetric, asymmetric)
    visual_weight: Dict[str, float]   # 视觉权重分布
    estimated_capacity: TextCapacity  # 文本容量估计
    
@dataclass
class TextCapacity:
    """文本容量估计"""
    title_max_chars: int              # 标题最大字符数
    body_max_lines: int               # 正文最大行数
    bullet_max_items: int             # 项目符号最大项数
```

**content_analyzer.py** - 内容分析
```python
class ContentAnalyzer:
    """分析演讲大纲和内容结构"""
    
    def analyze_outline(self, outline: Outline) -> OutlineStructure:
        """分析大纲结构"""
        # 识别:
        # - 层级结构 (章、节、小节)
        # - 内容类型 (标题、列表、段落、引用)
        # - 内容长度 (短、中、长)
        # - 特殊元素 (图片建议、图表建议)
        
    def extract_requirements(self, section: Section) -> ContentRequirements:
        """提取内容需求"""
        
    def classify_content(self, content: str) -> ContentType:
        """分类内容类型"""
        # - TITLE: 标题
        # - BULLETS: 项目列表
        # - PARAGRAPH: 段落
        # - QUOTE: 引用
        # - COMPARISON: 对比
        # - IMAGE_WITH_TEXT: 图文
```

**matcher.py** - 智能匹配引擎 ⭐核心
```python
class LayoutMatcher:
    """内容与版式智能匹配"""
    
    def match(self, 
              content: ContentRequirements, 
              layouts: List[LayoutProfile]) -> LayoutMatch:
        """为内容匹配最佳版式"""
        
    def score(self, content: ContentRequirements, layout: LayoutProfile) -> float:
        """计算匹配分数"""
        # 评分维度:
        # 1. 结构匹配 (40%)
        #    - 列数匹配
        #    - 形状数量匹配
        #    - 占位符类型匹配
        # 2. 容量匹配 (30%)
        #    - 文本长度适配
        #    - 项目符号数量适配
        # 3. 语义匹配 (20%)
        #    - 内容类型匹配
        #    - 版式用途匹配
        # 4. 视觉匹配 (10%)
        #    - 视觉权重分布
        #    - 对称性偏好
        
    def rank(self, content: ContentRequirements, 
             layouts: List[LayoutProfile]) -> List[LayoutMatch]:
        """返回排序后的匹配结果"""
```

#### 模块 3: generator (生成引擎)

**assembler.py** - 幻灯片组装
```python
class SlideAssembler:
    """组装幻灯片"""
    
    def assemble(self, 
                 template: Presentation,
                 matches: List[LayoutMatch]) -> Presentation:
        """根据匹配结果组装幻灯片"""
        
    def duplicate_slide(self, source: Slide, layout: LayoutProfile) -> Slide:
        """复制幻灯片"""
        
    def reorder_slides(self, prs: Presentation, order: List[int]) -> Presentation:
        """重新排序幻灯片"""
```

**content_applier.py** - 内容应用
```python
class ContentApplier:
    """应用内容到幻灯片"""
    
    def apply(self, slide: Slide, content: ContentSection) -> Slide:
        """应用内容到单张幻灯片"""
        
    def fill_placeholder(self, 
                         shape: Shape, 
                         content: str, 
                         formatting: Formatting) -> None:
        """填充占位符内容"""
        
    def preserve_formatting(self, shape: Shape, new_content: str) -> None:
        """保留原有格式"""
```

**validator.py** - 质量验证
```python
class SlideValidator:
    """验证生成质量"""
    
    def validate(self, prs: Presentation) -> ValidationResult:
        """验证整个演示文稿"""
        
    def check_overflow(self, slide: Slide) -> List[OverflowIssue]:
        """检查文本溢出"""
        
    def check_empty_shapes(self, slide: Slide) -> List[Shape]:
        """检查空形状"""
        
    def generate_report(self, validation: ValidationResult) -> str:
        """生成验证报告"""
```

#### 模块 4: utils (工具)

**thumbnail.py** - 缩略图生成
```python
def generate_thumbnails(pptx_path: str, 
                        output_dir: str, 
                        cols: int = 5) -> str:
    """生成幻灯片缩略图网格"""
```

**logger.py** - 日志记录
```python
class CocoLogger:
    """统一日志记录"""
    
    def info(self, msg: str): ...
    def debug(self, msg: str): ...
    def warning(self, msg: str): ...
    def error(self, msg: str): ...
```

---

## 4. 数据流设计

### 4.1 完整流程

```
用户输入
   │
   ├─ template.pptx ──────┐
   ├─ outline.md ─────────┤
   └─ content.json ───────┤
                          │
                          ▼
              ┌───────────────────────┐
              │   1. 加载输入          │
              │   - 验证模板          │
              │   - 解析内容          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   2. 分析版式          │
              │   - 提取特征          │
              │   - 分类版式          │
              │   - 建立版式库        │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   3. 分析内容          │
              │   - 解析结构          │
              │   - 提取需求          │
              │   - 分类内容          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   4. 智能匹配          │
              │   - 计算匹配分数      │
              │   - 排序选择          │
              │   - 处理冲突          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   5. 组装幻灯片        │
              │   - 复制版式          │
              │   - 重新排序          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   6. 应用内容          │
              │   - 填充文本          │
              │   - 保留格式          │
              │   - 处理溢出          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   7. 质量验证          │
              │   - 检查溢出          │
              │   - 检查空形状        │
              │   - 生成报告          │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   8. 输出结果          │
              │   - 保存 PPTX         │
              │   - 生成缩略图        │
              │   - 输出报告          │
              └───────────────────────┘
```

### 4.2 匹配算法详解

```python
def calculate_match_score(content, layout):
    """
    计算内容与版式的匹配分数 (0-100)
    """
    scores = {}
    weights = {
        'structure': 0.40,  # 结构匹配 40%
        'capacity': 0.30,   # 容量匹配 30%
        'semantic': 0.20,   # 语义匹配 20%
        'visual': 0.10      # 视觉匹配 10%
    }
    
    # 1. 结构匹配 (40 分)
    structure_score = 0
    # 列数匹配 (15 分)
    if content.column_count == layout.column_count:
        structure_score += 15
    elif abs(content.column_count - layout.column_count) == 1:
        structure_score += 8
    
    # 形状数量匹配 (15 分)
    if content.text_shapes == layout.text_shape_count:
        structure_score += 15
    elif abs(content.text_shapes - layout.text_shape_count) <= 1:
        structure_score += 8
    
    # 占位符类型匹配 (10 分)
    if content.has_title and layout.has_title:
        structure_score += 5
    if content.has_body and layout.has_body:
        structure_score += 5
    
    scores['structure'] = structure_score
    
    # 2. 容量匹配 (30 分)
    capacity_score = 0
    # 标题长度适配 (15 分)
    title_ratio = len(content.title) / layout.title_max_chars
    if title_ratio <= 1.0:
        capacity_score += 15
    elif title_ratio <= 1.2:
        capacity_score += 10
    elif title_ratio <= 1.5:
        capacity_score += 5
    
    # 正文长度适配 (15 分)
    body_ratio = content.body_lines / layout.body_max_lines
    if body_ratio <= 1.0:
        capacity_score += 15
    elif body_ratio <= 1.2:
        capacity_score += 10
    elif body_ratio <= 1.5:
        capacity_score += 5
    
    scores['capacity'] = capacity_score
    
    # 3. 语义匹配 (20 分)
    semantic_score = 0
    # 内容类型匹配 (10 分)
    if content.content_type == layout.layout_type:
        semantic_score += 10
    elif content.content_type in layout.compatible_types:
        semantic_score += 5
    
    # 版式用途匹配 (10 分)
    if content.section_type == layout.section_type:
        semantic_score += 10
    
    scores['semantic'] = semantic_score
    
    # 4. 视觉匹配 (10 分)
    visual_score = 0
    # 对称性偏好 (5 分)
    if content.prefers_symmetry == layout.layout_symmetry:
        visual_score += 5
    
    # 视觉权重分布 (5 分)
    visual_score += calculate_visual_similarity(
        content.visual_preference,
        layout.visual_weight
    ) * 5
    
    scores['visual'] = visual_score
    
    # 加权总分
    total_score = sum(
        scores[dim] * weights[dim] 
        for dim in weights
    )
    
    return total_score, scores
```

---

## 5. 命令行接口设计

### 5.1 基本用法

```bash
# 最简单用法 - 自动匹配
coco-ppt --template template.pptx --outline outline.md --output result.pptx

# 指定内容文件
coco-ppt --template template.pptx --content content.json --output result.pptx

# 生成详细报告
coco-ppt --template template.pptx --outline outline.md --output result.pptx --report

# 生成缩略图预览
coco-ppt --template template.pptx --outline outline.md --output result.pptx --thumbnails

# 调试模式 - 输出版式分析
coco-ppt --template template.pptx --analyze-only

# 交互式选择
coco-ppt --template template.pptx --outline outline.md --interactive
```

### 5.2 参数说明

```bash
必需参数:
  --template PATH       PPTX 模板文件路径
  --outline PATH        Markdown 大纲文件路径 (与--content 二选一)
  --content PATH        JSON 内容文件路径 (与--outline 二选一)
  --output PATH         输出 PPTX 文件路径

可选参数:
  --report              生成详细匹配报告
  --thumbnails          生成缩略图预览
  --analyze-only        仅分析不生成
  --interactive         交互式选择版式
  --debug               调试模式输出
  --log-level LEVEL     日志级别 (DEBUG/INFO/WARNING/ERROR)
  --output-dir DIR      输出目录 (默认当前目录)
```

---

## 6. 输入格式规范

### 6.1 Markdown 大纲格式

```markdown
# 演示文稿标题

## 第一章：引言
### 1.1 背景介绍
这里是背景介绍的详细内容...

### 1.2 问题陈述
- 问题点 1
- 问题点 2
- 问题点 3

## 第二章：解决方案
### 2.1 方案概述
方案的详细描述...

### 2.2 技术架构
- 组件 A
- 组件 B
- 组件 C

> "这是一句重要的引用"
> —— 引用来源

## 第三章：对比分析
### 3.1 方案对比
| 特性 | 方案 A | 方案 B |
|------|--------|--------|
| 性能 | 高     | 中     |
| 成本 | 低     | 高     |
```

### 6.2 JSON 内容格式

```json
{
  "title": "演示文稿标题",
  "slides": [
    {
      "type": "title",
      "title": "主标题",
      "subtitle": "副标题"
    },
    {
      "type": "bullets",
      "title": "项目列表页",
      "items": [
        "第一点内容",
        "第二点内容",
        "第三点内容"
      ]
    },
    {
      "type": "two_column",
      "title": "对比页",
      "left": {
        "title": "左侧标题",
        "content": "左侧内容..."
      },
      "right": {
        "title": "右侧标题",
        "content": "右侧内容..."
      }
    },
    {
      "type": "quote",
      "quote": "引用内容",
      "author": "作者名"
    }
  ]
}
```

---

## 7. 输出规范

### 7.1 生成的 PPTX
- 保持模板的视觉风格
- 内容正确填充到对应版式
- 格式保留（字体、颜色、对齐等）

### 7.2 生成报告 (可选)

```markdown
# COCO-PPT 生成报告

## 基本信息
- 模板：template.pptx (73 页)
- 内容：outline.md
- 生成时间：2026-03-12 00:00:00
- 输出：result.pptx (15 页)

## 版式匹配详情

### Slide 1: 封面页
- 使用模板页：0
- 版式类型：TITLE_SLIDE
- 匹配分数：95/100
- 内容：演示文稿标题

### Slide 2: 背景介绍
- 使用模板页：12
- 版式类型：BULLET_LIST
- 匹配分数：88/100
- 内容：3 个项目点

### Slide 3: 问题陈述
- 使用模板页：15
- 版式类型：TWO_COLUMN
- 匹配分数：92/100
- 内容：左右对比

...

## 质量检查
✅ 所有文本适配良好
✅ 无空形状
✅ 格式保留完整

## 统计
- 总幻灯片数：15
- 平均匹配分数：90.5
- 最高匹配分数：98 (Slide 5)
- 最低匹配分数：75 (Slide 12)
```

### 7.3 缩略图预览
- 网格布局 (5 列 x N 行)
- 每张幻灯片清晰可见
- 文件名：thumbnails.jpg

---

## 8. 技术实现要点

### 8.1 版式识别算法

**列数检测**:
```python
def detect_column_count(shapes):
    """通过分析形状的水平位置分布检测列数"""
    # 1. 收集所有文本形状的中心 X 坐标
    x_centers = [shape.center_x for shape in shapes]
    
    # 2. 聚类分析
    clusters = cluster_x_coordinates(x_centers)
    
    # 3. 根据聚类数量判断列数
    if len(clusters) == 1:
        return 1
    elif len(clusters) == 2:
        return 2
    elif len(clusters) >= 3:
        return 3
    
    return 1
```

**版式分类**:
```python
def classify_layout(features):
    """基于特征分类版式"""
    rules = [
        # 封面页
        (lambda f: f.has_title and f.text_shape_count == 1 
                   and f.title_position == 'center', 'TITLE_SLIDE'),
        
        # 章节页
        (lambda f: f.has_title and f.text_shape_count == 1 
                   and f.title_position == 'left', 'SECTION_HEADER'),
        
        # 项目列表
        (lambda f: f.has_title and f.has_body 
                   and f.column_count == 1, 'BULLET_LIST'),
        
        # 双列对比
        (lambda f: f.has_title and f.column_count == 2, 'TWO_COLUMN'),
        
        # 三列对比
        (lambda f: f.has_title and f.column_count == 3, 'THREE_COLUMN'),
        
        # 左图右文
        (lambda f: f.has_title and f.image_placeholder_count == 1 
                   and f.visual_weight['right'] > 0.6, 'IMAGE_RIGHT'),
        
        # 引用页
        (lambda f: f.text_shape_count == 2 
                   and f.layout_symmetry == 'symmetric', 'QUOTE'),
    ]
    
    for condition, layout_type in rules:
        if condition(features):
            return layout_type
    
    return 'CONTENT_WITH_CAPTION'  # 默认
```

### 8.2 依赖管理

**requirements.txt**:
```
python-pptx>=0.6.21
Pillow>=9.0.0
defusedxml>=0.7.1
click>=8.0.0  # 命令行接口
rich>=12.0.0  # 美化输出
```

### 8.3 性能优化

- 版式分析结果缓存
- 批量处理幻灯片
- 延迟加载大文件
- 并行处理独立任务

---

## 9. 测试计划

### 9.1 单元测试
- 版式特征提取
- 内容解析
- 匹配算法
- 内容应用

### 9.2 集成测试
- 完整流程测试
- 多模板测试
- 边界条件测试

### 9.3 用户测试
- 真实场景测试
- 性能基准测试
- 用户体验反馈

---

## 10. 实现路线图

### Phase 1: 基础框架 (Week 1)
- [ ] 项目结构搭建
- [ ] 输入加载模块
- [ ] 基础版式分析
- [ ] 简单内容解析

### Phase 2: 核心算法 (Week 2)
- [ ] 智能版式识别
- [ ] 内容 - 版式匹配引擎
- [ ] 评分系统实现
- [ ] 幻灯片组装

### Phase 3: 内容应用 (Week 3)
- [ ] 内容填充逻辑
- [ ] 格式保留
- [ ] 溢出处理
- [ ] 质量验证

### Phase 4: 完善优化 (Week 4)
- [ ] 命令行接口
- [ ] 报告生成
- [ ] 缩略图生成
- [ ] 性能优化
- [ ] 文档编写

---

## 11. 风险与挑战

### 技术风险
1. **版式识别准确性**: 复杂版式可能误判
   - 缓解：多特征融合，人工校验模式
   
2. **文本溢出处理**: 内容过长导致排版问题
   - 缓解：智能截断，字体自适应，警告提示

3. **格式保留**: 复杂格式可能丢失
   - 缓解：深度格式分析，渐进式降级

### 使用风险
1. **用户期望管理**: 自动化不完美
   - 缓解：清晰文档，交互式确认

2. **模板兼容性**: 非标准模板可能不支持
   - 缓解：模板验证，兼容性报告

---

## 12. 成功标准

### 功能标准
- ✅ 支持常见版式类型识别 (90%+ 准确率)
- ✅ 自动匹配内容与版式 (80%+ 满意度)
- ✅ 生成可编辑的 PPTX 文件
- ✅ 完全本地运行，无需 API

### 性能标准
- ✅ 100 页模板分析 < 10 秒
- ✅ 20 页 PPT 生成 < 30 秒
- ✅ 内存占用 < 500MB

### 用户体验标准
- ✅ 单命令完成生成
- ✅ 清晰的进度反馈
- ✅ 详细的生成报告
- ✅ 友好的错误提示

---

**设计完成时间**: 2026-03-12
**版本**: 1.0
**状态**: 待实现
