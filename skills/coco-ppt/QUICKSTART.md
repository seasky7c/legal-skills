# COCO-PPT 快速入门

## 5 分钟上手

### Step 1: 安装依赖 (1 分钟)

```bash
cd ~/.agents/skills/coco-ppt
pip install -r requirements.txt
```

### Step 2: 准备材料 (2 分钟)

**准备一个 PPTX 模板**：
- 任意 `.pptx` 文件
- 包含多个版式（至少 3 个）
- 可以从网上下载免费模板

**准备一个 Markdown 大纲**：
```markdown
# 我的演示文稿

## 第一章：引言
### 1.1 背景
介绍项目背景...

### 1.2 目标
- 目标 1
- 目标 2
- 目标 3

## 第二章：内容
### 2.1 详细信息
详细内容描述...
```

### Step 3: 生成 PPT (1 分钟)

```bash
python3 scripts/coco-ppt.py \
  --template /path/to/your/template.pptx \
  --outline /path/to/your/outline.md \
  --output /path/to/output.pptx \
  --report
```

### Step 4: 查看结果 (1 分钟)

- 打开生成的 `output.pptx`
- 查看匹配报告（终端输出）
- 根据需要手动调整

## 完整示例

使用技能自带的示例文件：

```bash
cd ~/.agents/skills/coco-ppt

# 生成 PPT
python3 scripts/coco-ppt.py \
  --template examples/sample.pptx \
  --outline examples/sample-outline.md \
  --output ~/my-presentation.pptx \
  --report \
  --thumbnails

# 查看生成的文件
ls -lh ~/my-presentation.pptx
ls -lh ~/thumbnails-my-presentation.jpg
```

## 常用命令

### 仅分析（不生成）

```bash
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --analyze-only \
  --report
```

### 调试模式

```bash
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --debug
```

### 生成缩略图

```bash
python3 scripts/coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx \
  --thumbnails
```

## Markdown 大纲语法

```markdown
# 演示文稿总标题

## 章节标题（可选）
### 幻灯片标题
幻灯片正文内容...

- 列表项 1
- 列表项 2
- 列表项 3

> 引用内容
> —— 作者
```

## JSON 内容格式

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

## 提示与技巧

### 选择好模板
- 版式越多，匹配越准确
- 包含标题、列表、引用等多种版式
- 避免过于简单的模板

### 优化大纲
- 每张幻灯片内容不要太多
- 使用列表项组织内容
- 标题简洁明了

### 查看报告
- 关注低分匹配（<70 分）
- 检查文本溢出警告
- 必要时手动调整

## 下一步

- 阅读完整文档：`cat SKILL.md`
- 查看架构设计：`cat docs/architecture.md`
- 运行测试：`bash test_skill.sh`

---

**需要帮助？** 查看 `INSTALL.md` 获取详细安装指南。
