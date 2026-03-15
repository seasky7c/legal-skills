# Obsidian 语法参考（兼容 Claude Skills）

本文档参考了 Obsidian 官方技能和 Claude Skills 的 obsidian-markdown，确保 AI 生成的内容完全兼容 Obsidian。

---

## 一、Wikilinks（双向链接）

### 基础语法

```markdown
[[Note Name]]                          链接到笔记
[[Note Name|Display Text]]             自定义显示文本
[[Note Name#Heading]]                  链接到标题
[[Note Name#^block-id]]                链接到块
[[#Heading in same note]]              同笔记内标题链接
[[Note Name|Custom Text#Heading]]      组合使用
```

### 自动双向链接规则

**AI 应自动识别并添加链接的内容**：

1. **人名/角色名** → `[[人物名]]`
2. **地点/机构名** → `[[地点名]]`、`[[机构名]]`
3. **概念/术语** → `[[专业术语]]`
4. **项目名** → `[[项目名]]`
5. **已存在笔记的标题** → 自动匹配并添加 `[[ ]]`

### 实体识别示例

```markdown
# 输入
叶枫是普罗米修斯计划的 P-07 实验体，能力是适应。
陈国栋是理事会主席，林薇是 P-08。

# AI 处理后（假设已有这些笔记）
[[叶枫]]是[[普罗米修斯计划]]的[[P-07 实验体]]，能力是[[适应]]。
[[陈国栋]]是[[理事会]]主席，[[林薇]]是[[P-08]]。
```

### 实现逻辑

```python
# 伪代码
def auto_add_wikilinks(content, existing_notes):
    """
    content: 待处理的 Markdown 内容
    existing_notes: 知识库中已有笔记标题列表
    
    返回：添加了 wikilinks 的内容
    """
    for note_title in existing_notes:
        # 使用正则匹配，避免替换已有的 wikilinks
        pattern = r'(?<!\[)(?<!\[' + re.escape(note_title) + r')(?!\])(?!\])'
        content = re.sub(pattern, f'[[{note_title}]]', content)
    return content
```

---

## 二、Embeds（嵌入）

```markdown
![[image.png]]                           嵌入图片
![[image.png|300x400]]                   指定尺寸
![[Note Name]]                           嵌入笔记
![[Note Name#Heading]]                   嵌入笔记的特定部分
![[PDF 文件.pdf]]                        嵌入 PDF
![[PDF 文件.pdf#page=5]]                 嵌入 PDF 的特定页
```

---

## 三、Callouts（标注框）

### 基础语法

```markdown
> [!TYPE] 标题（可选）
> 标注内容
> 
> 支持多行
> - 列表
> - 项目
```

### 支持的类型

| 类型 | 用途 | 颜色 |
|------|------|------|
| `NOTE` | 普通注释 | 蓝色 |
| `TIP` | 提示建议 | 绿色 |
| `IMPORTANT` | 重要信息 | 紫色 |
| `WARNING` | 警告 | 橙色 |
| `CAUTION` |  caution | 红色 |
| `INFO` | 信息 | 蓝色 |
| `SUCCESS` | 成功 | 绿色 |
| `FAILURE` | 失败 | 红色 |
| `EXAMPLE` | 示例 | 蓝色 |
| `QUOTE` | 引用 | 灰色 |

### 使用示例

```markdown
> [!TIP] 写作建议
> 每天固定时间写作，培养习惯。
> 使用番茄工作法，25 分钟专注写作。

> [!WARNING] 注意事项
> 此功能尚未稳定，请勿用于生产环境。

> [!EXAMPLE] 示例代码
> ```python
> def hello():
>     print("Hello, World!")
> ```
```

### AI 自动添加 Callouts 的场景

1. **重点内容** → 自动用 `> [!IMPORTANT]` 标注
2. **建议/技巧** → 自动用 `> [!TIP]` 标注
3. **警告/风险** → 自动用 `> [!WARNING]` 标注
4. **示例代码** → 自动用 `> [!EXAMPLE]` 标注

---

## 四、Frontmatter（Properties）

### YAML 格式

```yaml
---
type: note
title: "笔记标题"
tags:
  - 标签 1
  - 标签 2
aliases:
  - 别名 1
  - 别名 2
created: 2026-03-05
modified: 2026-03-05
status: active
---
```

### 支持的字段类型

```yaml
---
# 基础字段
type: note | product | project | zettel | article
title: 字符串
tags: 数组
aliases: 数组
created: YYYY-MM-DD
modified: YYYY-MM-DD
status: active | done | archived | draft

# 文章特有字段
author: 字符串
source: URL
publish_date: YYYY-MM-DD

# 项目特有字段
deadline: YYYY-MM-DD
priority: high | medium | low
progress: 0-100

# 产品卡片特有字段
category: 字符串
price: 数字
rating: 1-5
---
```

### AI 写入规则

**白名单字段**（只允许写这些，不能发明新字段）：
- `type`, `title`, `tags`, `aliases`, `created`, `modified`, `status`
- `author`, `source`, `publish_date`（文章类）
- `deadline`, `priority`, `progress`（项目类）
- `category`, `price`, `rating`（产品类）

---

## 五、Tags（标签）

```markdown
#tag                                 行内标签
#标签/子标签                         嵌套标签
#标签 标签内容                        标签后直接跟内容
---
tags:
  - 标签 1
  - 标签 2/子标签
---                                  YAML 中的标签
```

### 标签规范

1. 使用 `#` 开头，不能有空格
2. 支持嵌套：`#项目/法律科技`
3. YAML 中的标签数组更规范，推荐用于 Frontmatter
4. 行内标签适合快速标记

---

## 六、Canvas（画布）

### JSON Canvas 格式 1.0

```json
{
  "name": "画布名称",
  "nodes": [
    {
      "id": "node1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 200,
      "text": "# 标题\n\n内容"
    },
    {
      "id": "node2",
      "type": "file",
      "x": 400,
      "y": 0,
      "width": 300,
      "height": 200,
      "file": "笔记标题.md"
    },
    {
      "id": "node3",
      "type": "link",
      "x": 800,
      "y": 0,
      "width": 200,
      "height": 100,
      "url": "https://example.com"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "node1",
      "toNode": "node2",
      "label": "关联"
    }
  ]
}
```

### 节点类型

| 类型 | 用途 | 字段 |
|------|------|------|
| `text` | 文本节点 | `text` (Markdown 格式) |
| `file` | 文件节点 | `file` (文件路径), `subpath` (可选) |
| `link` | 链接节点 | `url` |
| `group` | 分组节点 | `nodes` (子节点 ID 列表), `label` |

### AI 生成 Canvas 的场景

1. **知识图谱**：概念之间的关系图
2. **项目规划**：任务分解与依赖关系
3. **文献综述**：论文之间的关系网络
4. **本体结构**：法律本体的类层级

---

## 七、自动处理规则（AI 必读）

### 1. Wikilinks 处理

```python
# 处理优先级
1. 已有笔记标题 → 必须添加 [[ ]]
2. 常见概念/术语 → 建议添加 [[ ]]
3. 人名/地名/机构名 → 建议添加 [[ ]]
4. 不确定的内容 → 保持原样，不添加
```

### 2. Callouts 处理

```python
# 自动识别并包裹 Callouts
if "注意" in text or "警告" in text:
    wrap_with_callout(text, "WARNING")
elif "建议" in text or "技巧" in text:
    wrap_with_callout(text, "TIP")
elif "重要" in text or "关键" in text:
    wrap_with_callout(text, "IMPORTANT")
elif "例如" in text or "示例" in text:
    wrap_with_callout(text, "EXAMPLE")
```

### 3. Frontmatter 处理

```python
# 每次创建新笔记时
1. 检查是否已有 Frontmatter
2. 如果没有，添加标准 Frontmatter
3. 如果有，只更新 modified 字段
4. 不删除已有字段，不添加白名单外的字段
```

---

## 八、与 china-news-crawler 整合

### 归档工作流程

```
1. 使用 china-news-crawler 提取网页内容
   ↓
2. 解析内容，提取：
   - 标题、作者、发布时间
   - 正文内容
   - 图片
   ↓
3. 自动处理：
   - 添加 Frontmatter（type: article, source, publish_date 等）
   - 识别关键概念，添加 Wikilinks
   - 用 Callouts 标注重点内容
   ↓
4. 保存到对应目录：
   - 微信公众号 → 10-Articles/WeChat/
   - 其他网页 → 10-Articles/Web/
   ↓
5. 更新索引文件
```

### 示例：处理后的文章

```markdown
---
type: article
title: "Obsidian Skills 如何重塑知识工作流"
tags:
  - 微信公众号
  - AI
  - 知识管理
  - Obsidian
  - AgentSkills
source: 微信公众号
original_url: https://mp.weixin.qq.com/s/xxx
author: DracoVibeCoding
publish_date: 2026-01-19
created: 2026-03-05
modified: 2026-03-05
---

# Obsidian Skills 如何重塑知识工作流

> [!IMPORTANT] 核心观点
> 任何无法向 Coding Agent 提供本地数据访问的笔记软件都应该被淘汰！

## 为什么需要 Obsidian Skills？

通用 AI 模型训练的是标准 Markdown，不「认识」[[Obsidian]] 特有语法：

1. **[[Wikilinks]]**: `[[Note Name]]`
2. **Embeds**: `![[image.png]]`
3. **[[Callouts]]**: `> [!note]`
4. **Frontmatter**: YAML 格式的元数据

> [!TIP] 使用建议
> 安装 obsidian-skills 到 `.claude/` 目录，Claude Code 会自动加载。

## 参考
- [[Obsidian]] 官网
- [[JSON Canvas]] 规范

---
_归档时间：2026-03-05_
```

---

## 九、实用脚本

### auto_link.py（自动添加双向链接）

```python
#!/usr/bin/env python3
"""
自动为 Markdown 内容添加 Wikilinks
"""

import re
from pathlib import Path

def get_existing_notes(vault_path):
    """获取知识库中所有笔记标题"""
    notes = []
    for md_file in Path(vault_path).rglob("*.md"):
        notes.append(md_file.stem)
    return notes

def add_wikilinks(content, existing_notes):
    """为内容添加 Wikilinks"""
    # 按长度排序，优先匹配长标题（避免部分匹配）
    existing_notes.sort(key=len, reverse=True)
    
    for note in existing_notes:
        # 跳过已有的 wikilinks
        pattern = r'(?<!\[)(?<!\[' + re.escape(note) + r')(?!\])(?!\])'
        # 只匹配完整的词
        pattern = r'\b' + pattern + r'\b'
        content = re.sub(pattern, f'[[{note}]]', content, flags=re.IGNORECASE)
    
    return content

if __name__ == "__main__":
    vault_path = Path.home() / "Obsidian-Vault"
    existing_notes = get_existing_notes(vault_path)
    print(f"检测到 {len(existing_notes)} 篇笔记")
```

---

*本文档参考了：*
- *Claude Skills - obsidian-markdown*
- *Obsidian 官方文档*
- *JSON Canvas Spec 1.0*
