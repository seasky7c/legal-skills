# COCO-PPT

智能 PPT 生成技能 - 自动识别模板版式并匹配内容

## 功能特性

- 🎯 **智能版式识别**: 自动分析 PPT 模板中的每一页版式
- 🧠 **内容 - 版式匹配**: 将演讲大纲/内容与版式自动匹配找到最优版式
- ⚡ **自动组装**: 一键生成完整 PPT
- 🔒 **完全本地**: 不依赖外部 API，保护隐私
- 📦 **简单部署**: 非容器化，pip install 即可使用

## 快速开始

### 安装

```bash
cd coco-ppt
pip install -r requirements.txt
```

### 基本用法

```bash
# 最简单用法
python scripts/coco-ppt.py --template template.pptx --outline outline.md --output result.pptx

# 生成详细报告和缩略图
python scripts/coco-ppt.py --template template.pptx --outline outline.md --output result.pptx --report --thumbnails
```

### 输入格式

#### Markdown 大纲

```markdown
# 演示文稿标题

## 第一章：引言
### 1.1 背景介绍
背景内容...

### 1.2 要点
- 要点 1
- 要点 2
- 要点 3
```

#### JSON 内容

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
    }
  ]
}
```

## 命令参数

```
必需参数:
  --template PATH       PPTX 模板文件路径
  --outline PATH        Markdown 大纲文件 (与--content 二选一)
  --content PATH        JSON 内容文件 (与--outline 二选一)
  --output PATH         输出 PPTX 文件路径

可选参数:
  --report              生成详细匹配报告
  --thumbnails          生成缩略图预览
  --analyze-only        仅分析不生成
  --interactive         交互式选择版式
  --debug               调试模式
  --log-level LEVEL     日志级别 (DEBUG/INFO/WARNING/ERROR)
```

## 项目结构

```
coco-ppt/
├── src/                    # 源代码
│   ├── loader/            # 输入加载
│   ├── analyzer/          # 分析引擎
│   ├── generator/         # 生成引擎
│   └── utils/             # 工具模块
├── scripts/               # 命令行脚本
├── templates/             # 示例模板
├── examples/              # 示例输入
├── docs/                  # 文档
└── logs/                  # 日志
```

## 支持的版式类型

- TITLE_SLIDE: 封面页
- SECTION_HEADER: 章节页
- BULLET_LIST: 项目列表
- TWO_COLUMN: 双列对比
- THREE_COLUMN: 三列对比
- IMAGE_LEFT: 左图右文
- IMAGE_RIGHT: 右图左文
- IMAGE_TOP: 上图下文
- QUOTE: 引用页
- BLANK: 空白页
- CONTENT_WITH_CAPTION: 带标题的内容页

## 开发进度

- [x] 架构设计
- [ ] Phase 1: 基础框架
- [ ] Phase 2: 核心算法
- [ ] Phase 3: 内容应用
- [ ] Phase 4: 完善优化

## 许可证

MIT License
