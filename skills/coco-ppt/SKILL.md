---
name: coco-ppt
slug: coco-ppt
version: 1.0.0
homepage: https://github.com/seasky7/coco-ppt
description: 智能 PPT 生成技能。自动识别 PPT 模板版式，将演讲大纲/内容与版式自动匹配，一键生成完整 PPT。完全本地化运行，不依赖外部 API。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3","libreoffice"],"pip":["python-pptx","Pillow","defusedxml","click","rich"]},"os":["linux","darwin","win32"]}}
---

## 激活条件

当用户提到以下需求时激活此技能：

- "帮我做 PPT"
- "生成演示文稿"
- "根据大纲制作 PPT"
- "用这个模板生成 PPT"
- "自动制作幻灯片"
- "coco-ppt"
- "智能 PPT 生成"

## 快速开始

### 1. 安装依赖

```bash
cd ~/.agents/skills/coco-ppt
pip install -r requirements.txt
```

**可选**（缩略图生成）：
```bash
sudo apt-get install libreoffice  # Linux
brew install libreoffice  # macOS
```

### 2. 基本用法

```bash
# 使用 Markdown 大纲
python scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx

# 使用 JSON 内容
python scripts/coco-ppt.py \
  --template template.pptx \
  --content content.json \
  --output result.pptx
```

### 3. 高级选项

```bash
# 生成详细报告和缩略图
python scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --report \
  --thumbnails

# 仅分析不生成（预览版式匹配）
python scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --analyze-only \
  --report

# 调试模式
python scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --debug
```

## 输入格式

### Markdown 大纲格式

```markdown
# 演示文稿标题

## 第一章：引言
### 1.1 背景介绍
背景内容...

### 1.2 要点
- 要点 1
- 要点 2
- 要点 3

## 第二章：解决方案
### 2.1 方案概述
详细描述...

> "重要引用"
> —— 引用来源
```

**语法说明**：
- `#` 一级标题：演示文稿总标题
- `##` 二级标题：章节标题
- `###` 三级标题：幻灯片标题
- 普通文本：幻灯片正文内容
- `-` 列表项：项目符号列表
- `>` 引用：引用页内容

### JSON 内容格式

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
      "title": "列表页",
      "items": ["项目 1", "项目 2", "项目 3"]
    },
    {
      "type": "two_column",
      "title": "对比页",
      "left": {"title": "左侧", "content": "内容..."},
      "right": {"title": "右侧", "content": "内容..."}
    },
    {
      "type": "quote",
      "quote": "引用内容",
      "author": "作者"
    }
  ]
}
```

**支持的幻灯片类型**：
- `title`: 封面页
- `bullets`: 项目列表
- `text`: 纯文本
- `two_column`: 双列对比
- `three_column`: 三列对比
- `quote`: 引用页
- `section`: 章节页

## 命令参数

```
必需参数:
  --template PATH       PPTX 模板文件路径
  --outline PATH        Markdown 大纲文件 (与--content 二选一)
  --content PATH        JSON 内容文件 (与--outline 二选一)
  --output PATH         输出 PPTX 文件路径

可选参数:
  --report              生成详细匹配报告
  --thumbnails          生成缩略图预览 (需要 LibreOffice)
  --analyze-only        仅分析不生成
  --interactive         交互式选择版式
  --debug               调试模式
  --log-level LEVEL     日志级别 (DEBUG/INFO/WARNING/ERROR)
```

## 支持的版式类型

系统自动识别以下版式类型：

| 版式类型 | 说明 | 识别特征 |
|---------|------|---------|
| **TITLE_SLIDE** | 封面页 | 居中标题，单文本形状 |
| **SECTION_HEADER** | 章节页 | 左侧/顶部标题 |
| **BULLET_LIST** | 项目列表 | 标题 + 正文占位符 |
| **TWO_COLUMN** | 双列对比 | 2 列布局 |
| **THREE_COLUMN** | 三列对比 | 3 列布局 |
| **IMAGE_LEFT** | 左图右文 | 左侧图片占位符 |
| **IMAGE_RIGHT** | 右图左文 | 右侧图片占位符 |
| **IMAGE_TOP** | 上图下文 | 顶部图片占位符 |
| **QUOTE** | 引用页 | 对称双文本形状 |
| **BLANK** | 空白页 | 无文本形状 |
| **CONTENT_WITH_CAPTION** | 带标题的内容页 | 标题 + 内容 |

## 核心功能

### 1. 智能版式识别 🎯

自动分析 PPT 模板中每一页的版式类型：

- **占位符分析**：识别标题、正文、图片占位符
- **列数检测**：基于形状位置聚类分析列数
- **对称性分析**：检测版式对称性
- **视觉权重计算**：分析内容分布
- **文本容量估计**：预估可容纳的文本量

### 2. 内容 - 版式匹配 🧠

四维评分系统确保最佳匹配：

| 维度 | 权重 | 评分内容 |
|------|------|---------|
| **结构匹配** | 40% | 列数、形状数量、占位符类型 |
| **容量匹配** | 30% | 文本长度适配度 |
| **语义匹配** | 20% | 内容类型、版式用途 |
| **视觉匹配** | 10% | 对称性、视觉权重 |

### 3. 自动组装 ⚡

一键生成完整 PPT：

- 复制选中的版式
- 应用内容到占位符
- 质量验证和溢出检测
- 生成匹配报告

### 4. 缩略图生成 📸

使用 LibreOffice 生成幻灯片预览：

```bash
python scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --thumbnails
```

输出：`thumbnails-result.jpg`（网格预览图）

## 工作流程

```
1. 加载模板 → 验证有效性
2. 加载内容 → 解析结构
3. 分析版式 → 提取特征
4. 分析内容 → 提取需求
5. 智能匹配 → 计算分数
6. 组装幻灯片 → 复制版式
7. 应用内容 → 填充文本
8. 质量验证 → 检查问题
9. 保存结果 → 输出 PPTX
10. 生成缩略图 → 预览网格
```

## 示例

### 示例 1: 快速生成

```bash
python scripts/coco-ppt.py \
  --template templates/professional.pptx \
  --outline examples/sample-outline.md \
  --output output/presentation.pptx
```

### 示例 2: 带报告和缩略图

```bash
python scripts/coco-ppt.py \
  --template templates/modern.pptx \
  --content examples/sample-content.json \
  --output output/presentation.pptx \
  --report \
  --thumbnails
```

### 示例 3: 分析模式

```bash
python scripts/coco-ppt.py \
  --template templates/template.pptx \
  --outline outline.md \
  --analyze-only \
  --report
```

## 输出

### 生成的文件

- **result.pptx**: 生成的演示文稿
- **匹配报告** (可选): 详细的版式匹配信息（`--report`）
- **缩略图** (可选): 幻灯片预览网格（`--thumbnails`）

### 报告内容

- 每张幻灯片的版式选择
- 匹配分数和排名
- 使用的模板页索引
- 低置信度匹配警告
- 质量验证结果

## 故障排除

### 常见问题

**Q: 模板验证失败**
A: 确保模板是有效的 PPTX 文件，且包含至少 2 个版式。

**Q: 文本溢出警告**
A: 减少单张幻灯片的内容量，或选择容量更大的版式。

**Q: 匹配分数低**
A: 尝试使用版式更丰富的模板，或简化内容结构。

**Q: 缩略图生成失败**
A: 安装 LibreOffice:
```bash
# Linux
sudo apt-get install libreoffice

# macOS
brew install libreoffice

# Windows
# 从 https://www.libreoffice.org 下载安装
```

### 调试技巧

1. 使用 `--debug` 模式查看详细日志
2. 使用 `--analyze-only` 预览版式分析结果
3. 使用 `--report` 查看匹配详情
4. 检查 `logs/coco-ppt.log` 日志文件

## 项目结构

```
coco-ppt/
├── src/                    # 源代码
│   ├── loader/            # 输入加载
│   │   ├── template_loader.py
│   │   └── content_loader.py
│   ├── analyzer/          # 分析引擎
│   │   ├── layout_analyzer.py
│   │   ├── content_analyzer.py
│   │   └── matcher.py
│   ├── generator/         # 生成引擎
│   │   ├── assembler.py
│   │   ├── content_applier.py
│   │   └── validator.py
│   └── utils/             # 工具模块
│       ├── logger.py
│       └── thumbnail.py
├── scripts/               # 命令行脚本
│   └── coco-ppt.py
├── examples/              # 示例输入
│   ├── sample-outline.md
│   └── sample-content.json
├── docs/                  # 文档
│   └── architecture.md
└── requirements.txt       # 依赖
```

## 依赖项

### Python 依赖

```
python-pptx>=0.6.21     # PPTX 文件操作
Pillow>=9.0.0          # 图像处理
defusedxml>=0.7.1      # XML 解析
click>=8.0.0           # 命令行接口
rich>=12.0.0           # 美化输出
```

安装：`pip install -r requirements.txt`

### 可选依赖

```
LibreOffice            # 缩略图生成（PPTX 转图片）
```

## 技术架构

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   输入层    │───▶│   分析引擎   │───▶│   生成引擎   │
│             │    │              │    │              │
│ • 模板加载  │    │ • 版式识别   │    │ • 幻灯片组装 │
│ • 内容解析  │    │ • 内容分析   │    │ • 内容应用   │
│ • 验证      │    │ • 智能匹配   │    │ • 质量验证   │
└─────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │    输出层    │
                                      │              │
                                      │ • PPTX 文件  │
                                      │ • 匹配报告   │
                                      │ • 缩略图     │
                                      └──────────────┘
```

## 性能指标

- **版式识别**: ~0.1 秒/幻灯片
- **内容匹配**: ~0.05 秒/幻灯片
- **内容应用**: ~0.2 秒/幻灯片
- **缩略图生成**: ~2-5 秒/幻灯片（依赖 LibreOffice）

**典型性能**（20 页 PPT）：
- 分析 + 生成：~5 秒
- 含缩略图：~30 秒

## 已知限制

1. **缩略图生成**: 需要安装 LibreOffice
2. **项目符号**: python-pptx 的项目符号支持有限
3. **复杂版式**: 非常规版式可能识别不准确
4. **文本溢出**: 提供警告但不自动调整字体大小
5. **图片处理**: 暂不支持自动插入图片

## 后续优化方向

1. **机器学习**: 使用 ML 模型改进版式分类
2. **用户反馈**: 收集反馈优化匹配算法
3. **性能优化**: 并行处理和大文件优化
4. **交互界面**: Web 或 GUI 界面
5. **更多模板**: 示例模板和预设
6. **图片支持**: 自动从内容中提取和插入图片

## 许可证

MIT License

## 作者

seasky7

## 反馈

- 问题反馈：GitHub Issues
- 技能更新：`clawhub sync`
- 推荐技能：`clawhub star coco-ppt`
