---
name: scrapling-web-extractor
description: 通用网页内容提取技能。基于 scrapling 库，支持任意网站的内容抓取，包括微信公众号、今日头条、知乎、博客、新闻站点等。当用户需要提取网页文章、抓取链接内容、或将网页保存为 Markdown 时激活。
---

# Scrapling Web Extractor Skill

通用网页内容提取工具，基于 scrapling 库，支持任意网站的内容抓取。

**核心优势**：
- 🎭 **无痕迹** - 高度防检测，绕过反爬虫
- ⚡ **高性能** - 速度快，支持并发
- 🔧 **通用性** - 支持任意网站，不局限于特定平台
- 📄 **多格式输出** - 支持 Markdown、JSON、纯文本

## 安装依赖

```bash
pip install scrapling playwright
playwright install chromium
```

## 使用方式

### 基本用法

```bash
# 提取网页内容，输出 Markdown
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL"

# 指定输出目录
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --output ./output

# 输出 JSON 格式
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --format json

# 输出纯文本
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --format text

# 使用浏览器模式（适合 JavaScript 渲染的页面）
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --browser
```

### Python API

```python
from extract import WebExtractor

extractor = WebExtractor()

# 静态页面
result = extractor.extract("https://example.com/article")

# 动态页面（需要浏览器）
result = extractor.extract("https://toutiao.com/article/xxx", use_browser=True)

print(result['title'])
print(result['content'])
```

## 输出格式

### Markdown 格式

```markdown
# 文章标题

**作者**: 作者名  
**发布时间**: 2024-01-01  
**来源**: 网站名称  
**链接**: https://example.com/article

---

正文内容...
```

### JSON 格式

```json
{
  "title": "文章标题",
  "author": "作者名",
  "publish_time": "2024-01-01",
  "source": "网站名称",
  "url": "https://example.com/article",
  "content": "正文内容...",
  "paragraphs": ["段落 1", "段落 2"],
  "images": ["图片 URL1", "图片 URL2"],
  "extracted_at": "2024-01-01T12:00:00"
}
```

## 支持的平台

本技能支持**任意网站**，包括但不限于：

| 类型 | 平台示例 |
|------|---------|
| 微信公众号 | mp.weixin.qq.com |
| 今日头条 | toutiao.com |
| 知乎 | zhihu.com |
| 简书 | jianshu.com |
| 博客园 | cnblogs.com |
| 掘金 | juejin.cn |
| 新闻网站 | 163.com, sohu.com, qq.com |
| 个人博客 | 任意 WordPress、Hexo 等 |

## 工作流程

1. **接收 URL** - 用户提供网页链接
2. **智能检测** - 判断是否需要浏览器模式
3. **内容提取** - 使用 scrapling 或 Playwright 获取内容
4. **智能解析** - 提取标题、作者、正文、图片等
5. **格式输出** - 生成 Markdown/JSON/文本

## 使用示例

### 提取微信公众号文章

```bash
python3 scripts/extract.py "https://mp.weixin.qq.com/s/xxxxx"
```

输出:
```
[INFO] Fetching: https://mp.weixin.qq.com/s/xxxxx
[INFO] Status: 200
[INFO] Title: 文章标题
[INFO] Author: 公众号名称
[INFO] Paragraphs: 156
[SUCCESS] Saved: ./output/wechat_xxxxx.md
```

### 提取今日头条文章（浏览器模式）

```bash
python3 scripts/extract.py "https://www.toutiao.com/article/xxxxx" --browser
```

### 批量提取

```bash
# 从文件读取 URL 列表
python3 scripts/extract.py --batch urls.txt --output ./articles
```

## 高级配置

### 自定义选择器

对于特殊网站，可以自定义 CSS/XPath 选择器：

```python
result = extractor.extract(
    "https://example.com/article",
    selectors={
        'title': '//h1[@class="title"]',
        'content': '//div[@id="content"]',
        'author': '//span[@class="author"]'
    }
)
```

### 代理配置

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

## 错误处理

| 错误类型 | 说明 | 解决方案 |
|----------|------|----------|
| `请求超时` | 网络慢或网站响应慢 | 增加 timeout 参数或使用 --browser |
| `内容提取失败` | 页面结构特殊 | 使用自定义选择器 |
| `JavaScript 渲染` | 动态内容 | 添加 --browser 参数 |
| `反爬虫拦截` | 网站有防护措施 | 使用 scrapling 的 stealth 模式 |

## 注意事项

- 仅用于合法合规的内容提取
- 不要进行大规模爬取
- 尊重目标网站的 robots.txt 和服务条款
- 高频访问建议添加延迟

## 目录结构

```
scrapling-web-extractor/
├── SKILL.md                      # [必需] Skill 定义文件
├── README.md                     # 使用说明
└── scripts/
    ├── extract.py                # CLI 入口脚本
    ├── extractor.py              # 核心提取器
    └── templates/
        └── markdown.tmpl         # Markdown 模板
```

## 与 china-news-crawler 的区别

| 特性 | scrapling-web-extractor | china-news-crawler |
|------|------------------------|-------------------|
| 支持范围 | 任意网站 | 仅中国新闻站点 |
| 动态页面 | ✅ 支持（浏览器模式） | ❌ 不支持 |
| 防检测 | ✅ 高度防检测 | ⚠️ 基础防护 |
| 输出格式 | Markdown/JSON/文本 | JSON+Markdown |
| 自定义 | ✅ 支持自定义选择器 | ❌ 固定选择器 |

**推荐**：优先使用 `scrapling-web-extractor`，仅在特定中国新闻站点提取失败时使用 `china-news-crawler`。

## 更新日志

- **v1.0.0** (2026-03-08) - 初始版本
  - 基于 scrapling 库
  - 支持静态和动态页面
  - Markdown/JSON/文本输出
  - 智能内容解析
