# 🧰 法律人 OpenClaw 技能仓库

> 专为法律职业群体设计的 OpenClaw 技能集合

**仓库地址**: https://github.com/seasky7c/legal-skills  
**许可协议**: MIT  
**维护者**: seasky7c

---

## 📖 项目简介

本仓库收集了专为法律职业群体（检察官、律师、法官、法务、法律研究者）设计的 OpenClaw 技能，涵盖信息收集、办公办文、法律检索、合同审核、诉讼辅助等多个场景。

所有技能均支持本地化部署，可在政务专网环境中使用。

---

## 🎯 技能分类体系

本仓库采用 9 大类技能分类体系：

| 分类 | 数量 | 说明 |
|------|------|------|
| 🔧 基础技能 | 12 个 | 技能管理、OCR、网页抓取、浏览器自动化等 |
| 🔍 信息搜索 | 8 个 | 网页搜索、论文搜索、法规追踪等 |
| 📄 办公办文 | 20 个 | Word/PPT/PDF/Markdown 操作、公文写作等 |
| 📱 媒体管理 | 8 个 | 公众号文章、短视频制作等 |
| ⚖️ 法律通用 | 15 个 | 法规检索、案例检索、卷宗 GPT 等 |
| 👨‍⚖️ 律师业务 | 15 个 | 合同审查/起草、诉讼业务等 |
| 🧑‍⚖️ 检察官业务 | 15 个 | 审查起诉、公诉、法律监督等 |
| 👩‍⚖️ 法官业务 | 15 个 | 庭前准备、裁判文书、量刑辅助等 |
| 🤝 调解业务 | 12 个 | 纠纷分析、调解策略、协议生成等 |

**总计**: 120 个技能（规划中）

---

## 📦 已收录技能

### ⚖️ 法律通用技能

#### 1. Contract Review Pro - 专业合同审核

**技能路径**: `skills/contract-review-pro/`  
**版本**: v2.0  
**作者**: Claude + 陈石律师  
**状态**: ✅ 已收录

**核心功能**:
- 📋 合同类型指引 - 快速查询各类合同的审核要点
- 🔍 合同详细审核 - 对具体合同进行逐条审核
- 📊 风险四级管理 - 致命/重要/一般/轻微
- 📝 专业输出 - 法律意见书 + 批注版合同

**特色优势**:
- ✅ 基于《合同审核方法论体系》（整合 5 本专业著作）
- ✅ 三观四步法、三维审查法等专业方法论
- ✅ 支持 18 种合同类型（物权/金融/建设工程/服务/公司/劳动合同）
- ✅ 三种审核模式（快速 5-10 分钟/标准 30-60 分钟/深度 1-2 小时）

**支持的合同类型**:
| 类别 | 合同类型 |
|------|----------|
| 物权类 | 买卖合同、租赁合同、商品房买卖合同、土地承包合同 |
| 金融合同 | 借款合同、担保合同（保证/抵押/质押） |
| 建设工程 | 建设工程合同 |
| 服务类 | 服务合同、承揽合同、委托合同、中介合同、技术开发合同、物业服务合同、仓储合同 |
| 公司合同 | 股权转让合同、合伙合同 |
| 劳动合同 | 劳动合同 |

**使用方法**:
```bash
# 方式一：查询合同类型指引
用户：买卖合同的审核要点是什么？

# 方式二：审核具体合同
用户：[上传合同.docx]
Skill 会询问代表方、市场地位、审核深度等信息，然后生成审核报告
```

**技术架构**:
- **数据层**: CSV 驱动（contract_types.csv, risk_templates.csv, review_checklists.csv 等）
- **核心模块**: Python 脚本（review_config, contract_analyzer, risk_assessment 等）
- **理论基础**: 《合同起草审查指南：三观四步法》等 5 本专业著作

**依赖库**:
```bash
pip install pandas>=2.0.0
pip install python-docx>=0.8.11
pip install jieba>=0.42.1
```

**文件结构**:
```
skills/contract-review-pro/
├── main.py                    # 主程序
├── main_v2.py                 # v2 版本
├── skill.json                 # 技能配置
├── SKILL.md                   # 技能说明
├── scripts/                   # 核心脚本
│   ├── review_config.py       # 审核配置管理
│   ├── contract_analyzer.py   # 合同分析器
│   ├── risk_assessment.py     # 风险评估器
│   ├── clause_review.py       # 条款审核器
│   ├── document_generator.py  # 文档生成器
│   └── ...
├── data/                      # 数据文件
│   ├── contract_types.csv     # 合同类型定义
│   ├── risk_templates.csv     # 风险模板库
│   └── review_checklists.csv  # 审查清单
└── data_collection/           # 用户反馈数据
```

**来源**: https://github.com/cslawyer1985/contract-review-pro

---

## 🚀 快速开始

### 安装技能

1. **克隆仓库**
```bash
git clone https://github.com/seasky7c/legal-skills.git
```

2. **复制技能到 OpenClaw**
```bash
cp -r legal-skills/skills/contract-review-pro ~/.openclaw/workspace/skills/
```

3. **安装依赖**
```bash
cd ~/.openclaw/workspace/skills/contract-review-pro
pip install -r requirements.txt  # 如有
```

4. **使用技能**
```bash
# 在 OpenClaw 中调用技能
# 具体使用方法请参考各技能的 SKILL.md
```

### 开发新技能

1. 参考 `skills/contract-review-pro/` 的目录结构
2. 创建 `SKILL.md` 定义技能元数据
3. 编写核心功能代码
4. 提交 Pull Request

---

## 📊 开发优先级

| 优先级 | 分类 | 数量 | 说明 |
|--------|------|------|------|
| 🔴 P0 | 法律通用 + 律师业务 | 20 个 | 急需技能，优先开发 |
| 🟠 P1 | 检察官 + 法官业务 | 26 个 | 重要技能，次优先 |
| 🟡 P2 | 调解业务 + 其他 | 18 个 | 可选技能，后续开发 |

---

## 🤝 贡献指南

欢迎法律从业者贡献技能或使用案例！

### 提交技能
1. Fork 本仓库
2. 在 `skills/` 目录下创建技能文件夹
3. 确保包含 `SKILL.md` 和必要的文档
4. 提交 Pull Request

### 技能要求
- ✅ 有明确的法律场景应用
- ✅ 包含完整的 SKILL.md 说明
- ✅ 代码有基本注释
- ✅ 支持本地化部署（政务专网友好）

---

## 📝 更新日志

### 2026-03-15
- ✅ 创建仓库
- ✅ 收录 contract-review-pro v2.0（专业合同审核技能）

---

## 📄 许可协议

本仓库技能除非另有说明，均采用 **MIT 许可协议**。

各技能的源代码许可请参考各自目录下的 LICENSE 文件。

---

## 💬 联系方式

- **GitHub Issues**: 提交问题和建议
- **仓库地址**: https://github.com/seasky7c/legal-skills

---

_法律人技能库 · 让法律工作更高效_
