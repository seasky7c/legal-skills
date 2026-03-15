# 📊 COCO-PPT 智能 PPT 生成技能

**位置**: `~/.agents/skills/coco-ppt/`

**版本**: 1.0.0

**许可证**: MIT

## 一句话介绍

自动识别 PPT 模板版式，将演讲大纲/内容与版式自动匹配，一键生成完整 PPT。

## 核心特性

- 🎯 **智能版式识别**: 自动分析 PPT 模板中的每一页版式
- 🧠 **内容 - 版式匹配**: 四维评分系统确保最佳匹配
- ⚡ **自动组装**: 一键生成完整 PPT
- 🔒 **完全本地**: 不依赖外部 API，保护隐私
- 📦 **简单部署**: pip install 即可使用

## 快速开始

```bash
# 1. 安装依赖
cd ~/.agents/skills/coco-ppt
pip install -r requirements.txt

# 2. 生成 PPT
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx

# 3. 查看结果
open result.pptx  # macOS
xdg-open result.pptx  # Linux
start result.pptx  # Windows
```

## 文件结构

```
coco-ppt/
├── SKILL.md              # 技能完整文档
├── INSTALL.md            # 安装指南
├── QUICKSTART.md         # 快速入门
├── README.md             # 项目说明
├── PROJECT_SUMMARY.md    # 项目总结
├── requirements.txt      # Python 依赖
├── scripts/
│   └── coco-ppt.py      # 主命令行工具
├── src/                  # 源代码
│   ├── loader/          # 输入加载
│   ├── analyzer/        # 分析引擎
│   ├── generator/       # 生成引擎
│   └── utils/           # 工具模块
├── examples/            # 示例文件
│   ├── sample-outline.md
│   └── sample-content.json
└── docs/                # 文档
    └── architecture.md
```

## 使用场景

✅ **适合**：
- 根据大纲快速生成 PPT
- 批量制作风格统一的演示文稿
- 将现有文档转换为 PPT
- 自动化 PPT 生成流程

❌ **不适合**：
- 需要高度定制化设计
- 复杂动画和过渡效果
- 嵌入视频和音频
- 实时协作编辑

## 命令参数

```
必需参数:
  --template PATH       PPTX 模板文件
  --outline PATH        Markdown 大纲 (或 --content)
  --content PATH        JSON 内容 (或 --outline)
  --output PATH         输出 PPTX 文件

可选参数:
  --report              生成匹配报告
  --thumbnails          生成缩略图
  --analyze-only        仅分析不生成
  --debug               调试模式
```

## 示例

### 最简单用法
```bash
python3 scripts/coco-ppt.py \
  --template my-template.pptx \
  --outline my-outline.md \
  --output presentation.pptx
```

### 带报告和缩略图
```bash
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --report \
  --thumbnails
```

### 分析模式（预览匹配）
```bash
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --analyze-only \
  --report
```

## Markdown 大纲示例

```markdown
# 项目汇报

## 第一章：项目背景
### 1.1 市场需求
- 市场规模：100 亿
- 增长率：30%/年
- 竞争格局：分散

### 1.2 我们的优势
技术领先、团队强大、资金充足

## 第二章：产品介绍
### 2.1 核心功能
智能匹配、自动生成、质量验证

> "创新改变世界"
> —— 乔布斯
```

## 支持的版式

系统自动识别 10+ 种版式：
- TITLE_SLIDE (封面页)
- SECTION_HEADER (章节页)
- BULLET_LIST (项目列表)
- TWO_COLUMN (双列对比)
- THREE_COLUMN (三列对比)
- IMAGE_LEFT/RIGHT (左右图文)
- IMAGE_TOP (上图下文)
- QUOTE (引用页)
- BLANK (空白页)
- CONTENT_WITH_CAPTION (带标题内容)

## 匹配算法

四维评分系统：

| 维度 | 权重 | 说明 |
|------|------|------|
| 结构匹配 | 40% | 列数、形状数量、占位符类型 |
| 容量匹配 | 30% | 文本长度适配度 |
| 语义匹配 | 20% | 内容类型、版式用途 |
| 视觉匹配 | 10% | 对称性、视觉权重 |

## 依赖项

**Python**:
- python-pptx >= 0.6.21
- Pillow >= 9.0.0
- defusedxml >= 0.7.1
- click >= 8.0.0
- rich >= 12.0.0

**可选**:
- LibreOffice (缩略图生成)

## 性能

- 分析 + 生成 20 页 PPT：~5 秒
- 含缩略图生成：~30 秒
- 版式识别：~0.1 秒/页
- 内容匹配：~0.05 秒/页

## 常见问题

**Q: 需要安装 LibreOffice 吗？**
A: 可选。不安装仍可生成 PPT，只是无法生成缩略图预览。

**Q: 模板有什么要求？**
A: 有效的 `.pptx` 文件，包含至少 2-3 个版式。

**Q: 匹配分数低怎么办？**
A: 使用版式更丰富的模板，或简化内容结构。

**Q: 支持中文吗？**
A: 完全支持。使用包含中文字体的模板即可。

## 文档链接

- 📖 [完整技能文档](SKILL.md)
- 🔧 [安装指南](INSTALL.md)
- 🚀 [快速入门](QUICKSTART.md)
- 🏗️ [架构设计](docs/architecture.md)

## 开发信息

- **作者**: seasky7
- **开发时间**: 2026-03-12
- **代码行数**: ~2000 行
- **完成度**: 90%（核心功能完成）

## 许可证

MIT License - 自由使用、修改和分发

---

**开始使用**: `cd ~/.agents/skills/coco-ppt && bash test_skill.sh`
