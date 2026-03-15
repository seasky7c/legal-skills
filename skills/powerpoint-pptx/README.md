# PowerPoint PPTX 技能

✅ **已安装** - 完全本地化，无需外部 API

## 安装状态

- **技能位置**: `/home/seasky7/.openclaw/workspace/skills/powerpoint-pptx/`
- **python-pptx 版本**: 1.0.2 ✅ 已安装
- **网络依赖**: ❌ 无
- **外部 API**: ❌ 无

## 快速开始

### 创建简单的 PPT

```python
from pptx import Presentation
from pptx.util import Inches, Pt

# 创建演示文稿
prs = Presentation()

# 添加标题页 (布局 0)
title_slide = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "欢迎使用 PowerPoint PPTX"
subtitle.text = "内网环境专用"

# 添加内容页 (布局 1)
content_slide = prs.slide_layouts[1]
slide = prs.slides.add_slide(content_slide)
title = slide.shapes.title
title.text = "主要内容"
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "第一点"
p = tf.add_paragraph()
p.text = "第二点"
p.level = 1

# 保存
prs.save('演示文稿.pptx')
```

### 使用模板

```python
# 加载现有模板
prs = Presentation('template.pptx')

# 添加幻灯片
slide = prs.slides.add_slide(prs.slide_layouts[1])

# 保存
prs.save('output.pptx')
```

## 内置布局

| 索引 | 布局名称 | 用途 |
|------|---------|------|
| 0 | Title Slide | 封面页 |
| 1 | Title and Content | 标准内容页 |
| 2 | Section Header | 章节分隔 |
| 3 | Two Content | 并排内容 |
| 4 | Comparison | 对比页 |
| 5 | Title Only | 仅标题 |
| 6 | Blank | 空白页 |

## 相关文档

- `SKILL.md` - 技能完整说明
- `slides.md` - 幻灯片模式
- `charts.md` - 图表和表格
- `design.md` - 设计指南

## 注意事项

1. **布局索引**: 不同模板的布局索引可能不同，使用前先检查 `prs.slide_layouts`
2. **字体**: 使用常见字体（Arial、Calibri）确保兼容性
3. **图片尺寸**: 始终使用 `Inches()` 或 `Pt()` 指定尺寸
4. **图表数据**: 类别数量必须与数据系列长度完全匹配
