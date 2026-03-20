# HTML Infographic - 专业信息图生成技能

🎨 根据用户输入内容，自动生成精美的可视化信息图 HTML 页面。

**版本**: 3.0 (专业版)  
**特性**: 多色系 · 多风格 · 多终端 · 参考图提取

---

## 🚀 快速开始

### 方式 1: 对话生成（推荐）

直接告诉我要素，我直接输出 HTML：

```
请生成 HTML 信息图：
内容：[标题 + 数据 + 章节]
色系：深蓝专业
风格：商务正式
终端：响应式
```

### 方式 2: 命令行生成

```bash
# 基本用法（默认紫蓝渐变 + 现代简约 + 响应式）
python3 scripts/generate.py content.md

# 指定色系
python3 scripts/generate.py content.md --color "深蓝专业"

# 指定风格
python3 scripts/generate.py content.md --style "商务正式"

# 指定终端
python3 scripts/generate.py content.md --device "mobile"

# 完整参数
python3 scripts/generate.py content.md \
  --color "深蓝专业" \
  --style "商务正式" \
  --device "responsive" \
  --name "项目名称"
```

---

## 🎨 五大色系（--color）

| 色系 | 配色 | 适用场景 |
|------|------|---------|
| **紫蓝渐变** (default) | `#667eea → #764ba2` | 科技、数据、商务报告 |
| **青绿清新** | `#11998e → #38ef7d` | 环保、健康、教育、成长 |
| **橙红活力** | `#f093fb → #f5576c` | 营销、活动、创意、年轻化 |
| **深蓝专业** | `#1e3c72 → #2a5298` | 政府、金融、法律、正式报告 ⭐ |
| **极简黑白** | `#2d3748 → #4a5568` | 极简主义、高端品牌、艺术 |

---

## 🎭 五大风格（--style）

| 风格 | 特点 | 适用场景 |
|------|------|---------|
| **现代简约** (default) | 圆角 16px、柔和阴影、留白充足 | 通用场景 ⭐ |
| **科技感** | 发光效果、科技蓝、未来感 | 科技产品、创新展示 |
| **商务正式** | 圆角 4px、保守阴影、边框清晰 | 政府、法律、金融报告 ⭐ |
| **创意活泼** | 圆角 24px、硬阴影、倾斜动画 | 营销、活动、年轻化 |
| **高端奢华** | 金色点缀、深度阴影、精致细节 | 高端品牌、产品发布 |

---

## 📱 终端适配（--device）

| 终端 | 布局 | 适用场景 |
|------|------|---------|
| **responsive** (default) | 自适应（桌面多列/手机单列） | 通用场景 ⭐ |
| **desktop** | 多列网格，信息密度高 | 电脑端展示、大屏演示 |
| **mobile** | 单列布局，大字体，触摸友好 | 手机端传播、社交媒体 |

---

## 📁 项目结构

每个项目生成独立文件夹：

```
projects/
└── 项目名称_20260320_191841/
    ├── index.html        # 主页面（可直接打开）
    ├── source.md         # 原始内容
    ├── config.json       # 配置参数（色系/风格/终端）
    └── reference.png     # 参考图（如有）
```

### config.json 示例

```json
{
  "color": "深蓝专业",
  "style": "商务正式",
  "device": "responsive",
  "color_info": {
    "primary": "#1e3c72",
    "gradient": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"
  },
  "style_info": {
    "radius": "4px",
    "shadow": "0 2px 4px rgba(0,0,0,0.1)"
  }
}
```

---

## 💡 推荐组合

### 法律/政府报告
```bash
--color "深蓝专业" --style "商务正式" --device "responsive"
```

### 科技产品展示
```bash
--color "紫蓝渐变" --style "科技感" --device "desktop"
```

### 营销活动页
```bash
--color "橙红活力" --style "创意活泼" --device "mobile"
```

### 环保/教育主题
```bash
--color "青绿清新" --style "现代简约" --device "responsive"
```

### 高端品牌发布
```bash
--color "极简黑白" --style "高端奢华" --device "desktop"
```

---

## 🖼️ 参考图提取（待实现）

从参考图片自动提取设计参数：

```bash
python3 scripts/generate.py content.md --template reference.png
```

**提取内容**:
- 主色调、辅助色、强调色
- 圆角大小、阴影强度
- 布局结构、间距比例
- 字体风格、边框样式

---

## 📋 内容格式

支持 Markdown 格式：

```markdown
# 标题

副标题（可选）

## 关键指标
- 指标 1: 123
- 指标 2: 456 万

## 内容章节
这里是详细描述...

### 子章节
更多内容...
```

---

## ⚙️ 依赖安装

```bash
pip install markdown click --break-system-packages
```

---

## 📊 示例项目

查看 `examples/` 目录获取内容示例。

运行测试：
```bash
# 默认样式
python3 scripts/generate.py examples/sample.md

# 深蓝商务风格
python3 scripts/generate.py examples/sample.md --color "深蓝专业" --style "商务正式"

# 移动端优化
python3 scripts/generate.py examples/sample.md --device "mobile"
```

---

## 🔧 命令行帮助

```bash
python3 scripts/generate.py --help
```

输出：
```
Usage: generate.py [OPTIONS] CONTENT_OR_FILE

Options:
  -c, --color [紫蓝渐变 | 青绿清新 | 橙红活力 | 深蓝专业 | 极简黑白]
  -s, --style [现代简约 | 科技感 | 商务正式 | 创意活泼 | 高端奢华]
  -d, --device [mobile|desktop|responsive]
  -o, --output TEXT               输出目录
  -n, --name TEXT                 项目名称
  -t, --template TEXT             参考图路径
  --help                          Show this message
```

---

**创建时间**: 2026-03-20  
**作者**: 嘟嘟 (for seasky7)  
**许可**: MIT
