# Legal Paper Search - 社会科学/法律类论文统一检索

**版本**: 1.0.0  
**创建日期**: 2026-03-16  
**作者**: seasky7  
**许可证**: MIT

---

## 🎯 技能描述

统一检索社会科学、法学、法律科技领域的学术论文，整合多个免费/开源数据源：

- ✅ **arXiv** - 预印本（含法律科技、AI 法律）
- ✅ **CORE** - 开放获取学术论文聚合
- ✅ **Semantic Scholar** - AI 驱动的学术搜索
- ✅ **LawArXiv** - 法律学科专用预印本
- ✅ **SSRN** - 社会科学预印本（法律论文丰富）
- ✅ **DOAJ** - 开放获取期刊目录

**适用场景**：法律研究、文献综述、学术研究、科技情报收集

---

## 🚀 快速使用

### 基本检索

```bash
# 检索法律 AI 相关论文
python3 scripts/legal_paper_search.py "legal artificial intelligence"

# 指定数据源
python3 scripts/legal_paper_search.py "machine learning law" --source arxiv core

# 指定结果数量
python3 scripts/legal_paper_search.py "judicial AI" --limit 20

# 导出为 JSON
python3 scripts/legal_paper_search.py "legal NLP" --output results.json

# 导出为 Markdown
python3 scripts/legal_paper_search.py "legal tech" --output results.md
```

### 高级检索

```bash
# 按时间范围检索
python3 scripts/legal_paper_search.py "contract review AI" --after 2023-01-01 --before 2026-12-31

# 按学科分类检索
python3 scripts/legal_paper_search.py "sentencing prediction" --subject cs.AI cs.LG

# 检索特定作者
python3 scripts/legal_paper_search.py "" --author "Richard Posner"

# 检索特定期刊/会议
python3 scripts/legal_paper_search.py "" --venue "ICAIL"

# 组合检索
python3 scripts/legal_paper_search.py "legal judgment prediction" \
  --source arxiv semantic_scholar \
  --after 2022-01-01 \
  --limit 30 \
  --output results.json
```

---

## 📦 依赖安装

### Python 依赖

```bash
cd /home/seasky7/.openclaw/workspace/skills/legal-paper-search
pip install -r requirements.txt
```

### API Key 配置（可选）

创建 `config.json` 文件：

```json
{
  "semantic_scholar": {
    "api_key": "",
    "use_cache": true
  },
  "core": {
    "api_key": "",
    "use_cache": true
  },
  "output": {
    "default_format": "markdown",
    "default_limit": 10
  }
}
```

**API Key 获取**：
- Semantic Scholar: https://www.semanticscholar.org/product/api
- CORE: https://core.ac.uk/services/documentation/

> ⚠️ **注意**: 所有数据源都支持无 API Key 访问，但速率受限。建议申请免费 API Key 提高限额。

---

## 🔧 技能架构

### 数据源适配器

```
legal_paper_search/
├── scripts/
│   ├── legal_paper_search.py      # 主程序
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── arxiv_source.py         # arXiv 适配器
│   │   ├── core_source.py           # CORE 适配器
│   │   ├── semantic_scholar.py      # Semantic Scholar 适配器
│   │   ├── lawarxiv_source.py       # LawArXiv 适配器
│   │   ├── ssrn_source.py           # SSRN 适配器
│   │   └── doaj_source.py           # DOAJ 适配器
│   └── exporters/
│       ├── __init__.py
│       ├── json_exporter.py
│       ├── markdown_exporter.py
│       └── bibtex_exporter.py
├── SKILL.md
├── requirements.txt
└── README.md
```

### 统一输出格式

所有数据源的结果统一为标准格式：

```json
{
  "id": "unique_identifier",
  "title": "论文标题",
  "authors": ["作者 1", "作者 2"],
  "year": 2024,
  "venue": "期刊/会议名称",
  "source": "arxiv",
  "url": "https://...",
  "pdf_url": "https://...",
  "doi": "10.xxxx/xxxxx",
  "abstract": "摘要内容...",
  "citations": 123,
  "subjects": ["cs.AI", "cs.LG"],
  "retrieved_at": "2026-03-16T00:00:00Z"
}
```

---

## 📊 检索结果示例

### Markdown 输出

```markdown
# 法律 AI 论文检索结果

**检索词**: legal artificial intelligence  
**数据源**: arXiv, CORE, Semantic Scholar  
**检索时间**: 2026-03-16 00:45:00  
**结果数量**: 25 篇

---

## 【1】Legal Zero-Days: A Novel Risk Vector for Advanced AI Systems

**作者**: Greg Sadler, Nathan Sherburn  
**年份**: 2025  
**来源**: arXiv  
**arXiv 编号**: 2508.10050  
**分类**: cs.CY, cs.AI  
**引用数**: 5  
**摘要**: We introduce the concept of "Legal Zero-Days" as a novel risk vector for advanced AI systems...  
**PDF**: https://arxiv.org/pdf/2508.10050.pdf

---

## 【2】The Law-Following AI Framework: Legal Foundations and Technical Constraints

**作者**: Katalina Hernandez Delgado  
**年份**: 2025  
**来源**: arXiv  
**arXiv 编号**: 2509.08009  
**分类**: cs.CY, cs.AI  
**引用数**: 3  
**摘要**: This paper critically evaluates the "Law-Following AI" (LFAI) framework...  
**PDF**: https://arxiv.org/pdf/2509.08009.pdf
```

### JSON 输出

```json
{
  "query": "legal artificial intelligence",
  "sources": ["arxiv", "core", "semantic_scholar"],
  "total_results": 25,
  "retrieved_at": "2026-03-16T00:45:00Z",
  "papers": [
    {
      "id": "arxiv:2508.10050",
      "title": "Legal Zero-Days: A Novel Risk Vector for Advanced AI Systems",
      "authors": ["Greg Sadler", "Nathan Sherburn"],
      "year": 2025,
      "venue": "arXiv preprint",
      "source": "arxiv",
      "arxiv_id": "2508.10050",
      "categories": ["cs.CY", "cs.AI"],
      "abstract": "...",
      "pdf_url": "https://arxiv.org/pdf/2508.10050.pdf",
      "citations": 5
    }
  ]
}
```

### BibTeX 输出（用于文献管理）

```bibtex
@article{sadler2025legal,
  title={Legal Zero-Days: A Novel Risk Vector for Advanced AI Systems},
  author={Sadler, Greg and Sherburn, Nathan},
  journal={arXiv preprint arXiv:2508.10050},
  year={2025},
  url={https://arxiv.org/abs/2508.10050}
}

@article{delgado2025law,
  title={The Law-Following AI Framework: Legal Foundations and Technical Constraints},
  author={Delgado, Katalina Hernandez},
  journal={arXiv preprint arXiv:2509.08009},
  year={2025},
  url={https://arxiv.org/abs/2509.08009}
}
```

---

## 🎯 法律领域专用功能

### 预设检索主题

```bash
# 法律科技热点
python3 scripts/legal_paper_search.py --topic legal_tech

# 司法智能化
python3 scripts/legal_paper_search.py --topic judicial_ai

# 合同审查 AI
python3 scripts/legal_paper_search.py --topic contract_review

# 法律 NLP
python3 scripts/legal_paper_search.py --topic legal_nlp

# 量刑预测
python3 scripts/legal_paper_search.py --topic sentencing_prediction

# 类案推送
python3 scripts/legal_paper_search.py --topic similar_case_recommendation

# 法律知识图谱
python3 scripts/legal_paper_search.py --topic legal_knowledge_graph
```

### 预设主题配置（`topics.json`）

```json
{
  "legal_tech": [
    "legal technology",
    "legal tech",
    "law technology",
    "legal innovation"
  ],
  "judicial_ai": [
    "judicial artificial intelligence",
    "AI in judiciary",
    "smart court",
    "judicial decision making AI"
  ],
  "contract_review": [
    "contract review AI",
    "automated contract analysis",
    "contract understanding",
    "legal document review"
  ],
  "legal_nlp": [
    "legal natural language processing",
    "legal text analysis",
    "legal language model",
    "law NLP"
  ],
  "sentencing_prediction": [
    "sentencing prediction",
    "judgment prediction",
    "legal judgment analysis",
    "court decision prediction"
  ]
}
```

---

## 🔍 数据源详细说明

### 1. arXiv

- **覆盖范围**: 预印本，含 cs.AI（AI）、cs.LG（机器学习）、cs.CL（计算语言学）
- **法律相关**: 法律科技、AI 法律、法律 NLP
- **API**: 免费，无需认证
- **速率限制**: 每 3 秒 1 次请求
- **优势**: 最新研究、开放获取

### 2. CORE

- **覆盖范围**: 开放获取学术论文聚合（1.3 亿 + 篇）
- **法律相关**: 社会科学、法学开放期刊
- **API**: 免费 API Key（可选）
- **速率限制**: 无 Key: 100 次/小时，有 Key: 1000 次/小时
- **优势**: 覆盖广、全文可下载

### 3. Semantic Scholar

- **覆盖范围**: 学术论文（含引用关系）
- **法律相关**: 法律期刊、会议论文
- **API**: 免费 API Key（可选）
- **速率限制**: 无 Key: 100 次/天，有 Key: 5000 次/天
- **优势**: 引用分析、影响力评估

### 4. LawArXiv

- **覆盖范围**: 法律学科专用预印本
- **法律相关**: 100% 法律论文
- **API**: 无官方 API，爬虫访问
- **优势**: 法律垂直领域、同行评审前

### 5. SSRN

- **覆盖范围**: 社会科学预印本
- **法律相关**: Legal Scholarship Network（LSN）
- **API**: 无官方 API，爬虫访问
- **优势**: 法律论文丰富、更新快

### 6. DOAJ

- **覆盖范围**: 开放获取期刊目录
- **法律相关**: 法学期刊
- **API**: 免费，无需认证
- **优势**: 期刊质量筛选、完全开放

---

## 💡 使用场景

### 场景 1: 法律科技综述写作

```bash
# 检索近 3 年法律 AI 论文
python3 scripts/legal_paper_search.py "legal AI" \
  --after 2023-01-01 \
  --limit 50 \
  --output legal_ai_review.json

# 导出为 Markdown 用于阅读
python3 scripts/legal_paper_search.py "legal AI" \
  --after 2023-01-01 \
  --limit 50 \
  --output legal_ai_review.md
```

### 场景 2: 研究趋势分析

```bash
# 检索不同主题的论文
python3 scripts/legal_paper_search.py --topic legal_tech --output legal_tech.json
python3 scripts/legal_paper_search.py --topic judicial_ai --output judicial_ai.json
python3 scripts/legal_paper_search.py --topic contract_review --output contract_review.json

# 分析年度趋势（使用分析脚本）
python3 scripts/analyze_trends.py legal_tech.json judicial_ai.json contract_review.json
```

### 场景 3: 文献管理集成

```bash
# 导出为 BibTeX，导入 Zotero/EndNote
python3 scripts/legal_paper_search.py "legal judgment prediction" \
  --output references.bib \
  --format bibtex
```

### 场景 4: 定期监控

```bash
# 每周检索最新论文（cron 任务）
0 9 * * 1 cd /home/seasky7/.openclaw/workspace/skills/legal-paper-search && \
  python3 scripts/legal_paper_search.py "legal AI" \
  --after $(date -d "last week" +%Y-%m-%d) \
  --output weekly_legal_ai_$(date +%Y%m%d).md
```

---

## ⚠️ 注意事项

1. **速率限制**: 无 API Key 时注意请求频率，避免被封禁
2. **数据去重**: 同一论文可能在多个数据源出现，建议启用去重功能
3. **质量筛选**: 预印本未经同行评审，引用时需谨慎
4. **版权合规**: 开放获取论文也需遵守相应许可协议
5. **内网部署**: 部分数据源需外网访问，政务专网需配置代理

---

## 🔗 相关资源

- **OpenClaw 法律技能库**: https://github.com/seasky7c/legal-skills
- **Semantic Scholar API**: https://www.semanticscholar.org/product/api
- **CORE API**: https://core.ac.uk/services/documentation/
- **arXiv API**: https://arxiv.org/help/api
- **LawArXiv**: https://lawarxiv.org/
- **SSRN**: https://www.ssrn.com/

---

_最后更新：2026-03-16_
