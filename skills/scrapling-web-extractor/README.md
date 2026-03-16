# Scrapling Web Extractor - 通用网页提取技能

## 📦 安装状态

✅ **已安装** - 2026-03-08

**位置**: `~/.agents/skills/scrapling-web-extractor/`

## 🎯 技能定位

**默认网页提取技能**，替换原有的 `china-news-crawler`。

### 优势对比

| 特性 | scrapling-web-extractor | china-news-crawler |
|------|------------------------|-------------------|
| 支持范围 | 任意网站 | 仅中国新闻站点 |
| 动态页面 | ✅ 支持（浏览器模式） | ❌ 不支持 |
| 防检测 | ✅ 高度防检测 | ⚠️ 基础防护 |
| 输出格式 | Markdown/JSON/文本 | JSON+Markdown |
| 自定义 | ✅ 支持自定义选择器 | ❌ 固定选择器 |

## 📖 使用方式

### 基本用法

```bash
# 提取网页内容，输出 Markdown
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL"

# 指定输出目录
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --output ./output

# 浏览器模式（适合动态页面如今日头条）
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --browser

# JSON 输出
python3 ~/.agents/skills/scrapling-web-extractor/scripts/extract.py "URL" --format json
```

### 已验证支持的网站

| 网站 | 测试状态 | 备注 |
|------|---------|------|
| 微信公众号 | ✅ 成功 | 静态提取 |
| 今日头条 | ✅ 成功 | 需要 `--browser` 参数 |
| 知乎 | ⏳ 待测试 | - |
| 博客园 | ⏳ 待测试 | - |
| 任意博客 | ⏳ 待测试 | - |

## 🔧 依赖

```bash
# 已安装
pip install scrapling playwright
playwright install chromium
```

## 📝 测试记录

### 2026-03-08 测试

**测试 1：微信公众号**
- URL: https://mp.weixin.qq.com/s/2NKDazjBJjpLaHRmn2dYhw
- 结果：✅ 成功
- 提取段落：156 段
- 输出文件：`/home/seasky7/.openclaw/workspace/output/wechat_2026_claude_skills.md`

**测试 2：今日头条**
- URL: https://www.toutiao.com/article/7610020817287529001/
- 结果：✅ 成功（使用 Playwright 浏览器模式）
- 提取内容：1,166 字符
- 输出文件：`/home/seasky7/.openclaw/workspace/output/toutiao_article.md`

## 📚 相关技能

- **china-news-crawler** - 备用技能，仅在中国新闻站点提取失败时使用
- **obsidian-helper** - 已更新为使用 scrapling 进行知识归档

## 🔄 替换记录

**2026-03-08**:
1. ✅ 创建 `scrapling-web-extractor` 技能
2. ✅ 更新 `TOOLS.md` - 标记为默认网页提取技能
3. ✅ 更新 `MEMORY.md` - 添加主线任务记录
4. ✅ 更新 `obsidian-helper/SKILL.md` - v1.5.0 → v1.6.0
5. ✅ 测试微信公众号、今日头条提取

---

_最后更新：2026-03-08_
