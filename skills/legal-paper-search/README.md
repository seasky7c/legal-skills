# Legal Paper Search - 社会科学/法律类论文统一检索技能

> 一站式检索 arXiv、CORE、Semantic Scholar 等开放学术资源  
> 无需付费订阅，完全免费使用

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/seasky7/.openclaw/workspace/skills/legal-paper-search
pip install -r requirements.txt --break-system-packages
```

### 2. 基本使用

```bash
# 检索法律 AI 论文
python3 scripts/legal_paper_search.py "legal AI"

# 指定数据源
python3 scripts/legal_paper_search.py "contract review" --source arxiv core semantic_scholar

# 导出为 Markdown
python3 scripts/legal_paper_search.py "judicial AI" --output results.md

# 使用预设主题
python3 scripts/legal_paper_search.py --topic legal_tech --limit 20 --output legal_tech.md
```

---

## 📊 支持的数据源

| 数据源 | 类型 | API Key | 速率限制 | 法律相关度 |
|--------|------|---------|---------|-----------|
| **arXiv** | 预印本 | ❌ 无需 | 3 次/秒 | ⭐⭐⭐⭐ (法律科技) |
| **CORE** | 开放获取论文 | ⚠️ 可选 | 1000 次/小时 | ⭐⭐⭐⭐ (法学期刊) |
| **Semantic Scholar** | 学术论文 | ⚠️ 可选 | 5000 次/天 | ⭐⭐⭐⭐ (引用分析) |
| **DOAJ** | 开放期刊 | ❌ 无需 | 无限制 | ⭐⭐⭐ (法学期刊) |
| **LawArXiv** | 法律预印本 | ❌ 无 API | 手动访问 | ⭐⭐⭐⭐⭐ (法律专用) |
| **SSRN** | 社科预印本 | ❌ 无 API | 手动访问 | ⭐⭐⭐⭐⭐ (法律丰富) |

---

## 🎯 预设检索主题

```bash
# 法律科技
python3 scripts/legal_paper_search.py --topic legal_tech

# 司法 AI
python3 scripts/legal_paper_search.py --topic judicial_ai

# 合同审查 AI
python3 scripts/legal_paper_search.py --topic contract_review

# 法律 NLP
python3 scripts/legal_paper_search.py --topic legal_nlp

# 量刑预测
python3 scripts/legal_paper_search.py --topic sentencing_prediction
```

---

## 📁 输出格式

### JSON（机器处理）

```bash
python3 scripts/legal_paper_search.py "legal AI" --output results.json
```

### Markdown（阅读/分享）

```bash
python3 scripts/legal_paper_search.py "legal AI" --output results.md
```

### BibTeX（文献管理）

```bash
python3 scripts/legal_paper_search.py "legal AI" --output references.bib --format bibtex
```

---

## 🔧 API Key 配置（可选）

创建 `config.json`：

```json
{
  "semantic_scholar": {
    "api_key": "YOUR_API_KEY"
  },
  "core": {
    "api_key": "YOUR_API_KEY"
  }
}
```

**获取 API Key**：
- Semantic Scholar: https://www.semanticscholar.org/product/api
- CORE: https://core.ac.uk/services/documentation/

---

## 💡 使用场景

### 1. 法律科技综述写作

```bash
python3 scripts/legal_paper_search.py "legal AI" \
  --after 2023-01-01 \
  --limit 50 \
  --output legal_ai_review.md
```

### 2. 定期文献监控

```bash
# 每周检索最新论文
python3 scripts/legal_paper_search.py "legal judgment prediction" \
  --after $(date -d "last week" +%Y-%m-%d) \
  --output weekly_$(date +%Y%m%d).md
```

### 3. 文献管理集成

```bash
# 导出 BibTeX 到 Zotero/EndNote
python3 scripts/legal_paper_search.py "contract analysis" \
  --output references.bib \
  --format bibtex
```

---

## 📊 技能统计

运行检索后显示：

```
============================================================
📚 Legal Paper Search - 法律类论文检索
============================================================
🔍 检索词：legal AI
📊 数据源：arxiv, core, semantic_scholar
📈 每源限制：10 篇
============================================================

🔎 检索 arxiv...
   ✅ 找到 10 篇

🔎 检索 core...
   ✅ 找到 8 篇

🔎 检索 semantic_scholar...
   ✅ 找到 10 篇

============================================================
📊 总计：28 篇（去重后）
============================================================
```

---

## ⚠️ 注意事项

1. **速率限制**: 无 API Key 时注意请求频率
2. **数据去重**: 自动按标题去重
3. **预印本质量**: arXiv/LawArXiv 论文未经同行评审
4. **内网部署**: 部分数据源需外网访问

---

## 🔗 相关资源

- **技能文档**: `SKILL.md`
- **法律技能库**: https://github.com/seasky7c/legal-skills
- **Semantic Scholar API**: https://www.semanticscholar.org/product/api
- **CORE API**: https://core.ac.uk/services/documentation/
- **arXiv API**: https://arxiv.org/help/api

---

_版本：1.0.0 | 创建日期：2026-03-16 | 许可证：MIT_
