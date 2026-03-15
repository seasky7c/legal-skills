# 🧰 法律人 OpenClaw 技能仓库

> 专为法律职业群体设计的 OpenClaw 技能集合

**仓库地址**: https://github.com/seasky7c/legal-skills  
**许可协议**: MIT  
**维护者**: seasky7c  
**最后更新**: 2026-03-15

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

## 📦 已收录技能（12 个）

### 🔧 基础技能

#### 1. Agent Browser - 浏览器自动化

**技能路径**: `skills/agent-browser/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🌐 网页导航、表单填写、按钮点击
- 📸 截图、数据提取、网页测试
- 🔐 登录认证、会话管理
- 🎥 视频录制、代理支持

**使用场景**:
- 打开网站、填写表单、点击按钮
- 截取网页截图、提取网页数据
- 测试 Web 应用、自动化浏览器任务

**来源**: https://github.com/steipete/agent-browser

---

#### 2. Agent Reach - 全网平台访问

**技能路径**: `skills/agent-reach/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 📱 配置 Twitter/X、Reddit、YouTube、GitHub 等平台访问
- 📺 支持 Bilibili、小红书、抖音、LinkedIn、Boss 直聘
- 📰 RSS 订阅管理
- 🌐 任意网页访问

**支持平台**:
- 国际：Twitter/X, Reddit, YouTube, GitHub, LinkedIn
- 国内：Bilibili, 小红书，抖音，Boss 直聘
- 通用：RSS, 任意网页

**使用场景**:
- 配置平台访问工具
- 检查可用平台
- 启用平台频道

---

#### 3. Self-Improvement - 自我改进系统

**技能路径**: `skills/self-improvement/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 📝 自动记录错误和学习
- 📊 持续改进系统
- 🔍 错误检测和学习提取
- 📈 知识沉淀到项目记忆

**使用场景**:
- 命令或操作意外失败时
- 用户纠正 AI 错误时
- 发现更好的方法时
- 外部 API 或工具失败时

**文件结构**:
```
skills/self-improvement/
├── .learnings/
│   ├── ERRORS.md           # 错误记录
│   ├── LEARNINGS.md        # 学习记录
│   └── FEATURE_REQUESTS.md # 功能请求
├── hooks/                   # Hook 系统
└── scripts/                 # 工具脚本
```

---

#### 4. Skill Vetter - 技能安全审查

**技能路径**: `skills/skill-vetter/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🔒 安全检查（红色标记、权限范围、可疑模式）
- ✅ 安装前技能审查
- 📊 信任评分系统
- 🛡️ 权限分析

**使用场景**:
- 从 ClawHub、GitHub 等来源安装技能前
- 检查技能权限范围
- 识别可疑模式

**信任评分**: 97/100

---

#### 5. Find Skills - 技能发现工具

**技能路径**: `skills/find-skills/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🔍 帮助用户发现和安装技能
- 📦 技能生态系统查询
- 💡 功能需求匹配

**使用场景**:
- "如何做到 X"
- "找一个能做 X 的技能"
- "有没有技能可以..."
- 扩展能力需求

---

### 🔍 信息搜索

#### 6. Baidu Search - 百度搜索

**技能路径**: `skills/baidu-search/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🔍 百度 AI 搜索引擎 (BDSE)
- 📰 实时信息、文档、研究主题
- 🇨🇳 中文内容优先

**环境变量**: `BAIDU_API_KEY`

**使用场景**:
- 搜索实时信息
- 查找文档资料
- 研究课题调研

---

#### 7. China News Crawler - 中国新闻提取

**技能路径**: `skills/china-news-crawler/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 📰 微信公众号文章提取
- 📱 今日头条、网易、搜狐、腾讯新闻
- 📄 输出 JSON 和 Markdown 格式
- 🔗 自动提取标题、作者、正文、图片

**支持平台**:
- 微信公众号
- 今日头条
- 网易新闻
- 搜狐新闻
- 腾讯新闻

**使用场景**:
- 提取中国新闻内容
- 抓取公众号文章
- 获取新闻 JSON/Markdown

**特点**: 独立可迁移，无外部依赖

---

#### 8. Deep Research - 深度研究

**技能路径**: `skills/deep-research/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🔬 深度主题研究
- 📚 学术论文检索
- 🔗 引用图谱分析
- 📊 综合研究报告

**使用场景**:
- 研究、调查、探索主题
- 学术论文调研
- 深度分析报告

---

### 📄 办公办文

#### 9. COCO-PPT - 智能 PPT 生成

**技能路径**: `skills/coco-ppt/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 🎯 智能版式识别（10+ 种版式类型）
- 🧠 内容 - 版式匹配（四维评分系统）
- ⚡ 自动组装（一键生成完整 PPT）
- 🔒 完全本地化（不依赖外部 API）

**评分系统**:
- 结构匹配 40%
- 容量匹配 30%
- 语义匹配 20%
- 视觉匹配 10%

**使用方法**:
```bash
python3 coco-ppt.py \
  --template template.pptx \
  --outline outline.md \
  --output result.pptx
```

**依赖**:
- python-pptx >= 0.6.21
- Pillow >= 9.0.0
- LibreOffice（可选，缩略图生成）

**来源**: https://github.com/seasky7/coco-ppt

---

#### 10. PowerPoint PPTX - PPTX 操作

**技能路径**: `skills/powerpoint-pptx/`  
**版本**: 1.0.0  
**状态**: ✅ 已收录

**核心功能**:
- 📊 创建、编辑 PowerPoint 演示文稿
- 📐 幻灯片、版式、图表操作
- 📝 批量处理
- 🎨 设计模板应用

**使用场景**:
- 创建新演示文稿
- 修改编辑内容
- 处理版式和布局
- 添加注释和演讲者备注

**依赖**: python-pptx

---

#### 11. Obsidian Helper - Obsidian 笔记助手

**技能路径**: `skills/obsidian-helper/`  
**版本**: 1.5.0  
**状态**: ✅ 已收录

**核心功能**:
- 📝 智能笔记创建和管理
- 🔗 自动双向链接
- 📌 自动 Callouts 标注
- 📚 日记、周复盘、月复盘模板
- 🗂️ 自动归档（整合 scrapling-web-extractor）

**目录结构**:
```
~/Obsidian-Vault/
├── 00-Inbox/          # 临时收集区
├── 10-Articles/       # 文章
├── 20-Notes/          # 永久笔记
├── 30-Projects/       # 项目
├── 40-Templates/      # 模板
└── 99-Archives/       # 归档
```

**使用场景**:
- 提到 obsidian、日记、笔记、知识库
- capture、review、归档、链接

**特点**: 遵循三条硬规矩（00_Inbox/AI/、追加式、白名单字段）

---

### ⚖️ 法律通用

#### 12. Contract Review Pro - 专业合同审核

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

**技术架构**:
- **数据层**: CSV 驱动（contract_types.csv, risk_templates.csv, review_checklists.csv 等）
- **核心模块**: Python 脚本（review_config, contract_analyzer, risk_assessment 等）
- **理论基础**: 《合同起草审查指南：三观四步法》等 5 本专业著作

**来源**: https://github.com/cslawyer1985/contract-review-pro

---

## 🚀 快速开始

### 安装技能

1. **克隆仓库**
```bash
git clone https://github.com/seasky7c/legal-skills.git
cd legal-skills
```

2. **复制技能到 OpenClaw**
```bash
# 复制单个技能
cp -r skills/contract-review-pro ~/.openclaw/workspace/skills/

# 或复制所有技能
cp -r skills/* ~/.openclaw/workspace/skills/
```

3. **安装依赖**
```bash
# 以 contract-review-pro 为例
cd ~/.openclaw/workspace/skills/contract-review-pro
pip install pandas python-docx jieba --break-system-packages
```

4. **使用技能**
```bash
# 在 OpenClaw 中直接调用
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

### 2026-03-15 v1.0.0
- ✅ 创建仓库
- ✅ 收录 12 个核心技能：
  - 基础技能：agent-browser, agent-reach, self-improvement, skill-vetter, find-skills
  - 信息搜索：baidu-search, china-news-crawler, deep-research
  - 办公办文：coco-ppt, powerpoint-pptx, obsidian-helper
  - 法律通用：contract-review-pro
- ✅ 添加完整 README 文档
- ✅ 9 大类技能分类体系设计

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
