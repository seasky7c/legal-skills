# 百度搜索引擎技能安装及使用说明

## 📦 技能信息

| 项目 | 说明 |
|------|------|
| **技能名称** | baidu-search |
| **功能描述** | 使用百度 AI 搜索引擎（BDSE）进行网页搜索 |
| **技能位置** | `/home/seasky7/.openclaw/workspace/skills/baidu-search/` |
| **API 提供商** | 百度 AI 搜索（Baidu AI Search Engine） |
| **状态** | ✅ 已安装并测试通过 |

---

## 🚀 安装步骤

### 步骤 1：安装技能

```bash
clawhub install baidu-search --registry https://clawhub.ai
```

安装成功后会显示：
```
✔ OK. Installed baidu-search -> /home/seasky7/.openclaw/workspace/skills/baidu-search
```

### 步骤 2：获取 API Key

1. 访问 [百度智能云控制台](https://console.bce.baidu.com/)
2. 注册/登录百度账号
3. 进入"应用列表" → "创建应用"
4. 选择"AI 搜索"服务
5. 获取 API Key（格式：`bce-v3/ALTAK-xxx/xxx`）

### 步骤 3：配置 API Key

编辑 OpenClaw 环境变量文件：

```bash
nano /home/seasky7/.openclaw/.env
```

添加以下内容：

```bash
#BAIDU SEARCH
BAIDU_API_KEY="bce-v3/ALTAK-yK5Y1AMmz94xihPZm0szP/1f418d345297776342f6e2553ddd3809ea926990"
```

### 步骤 4：重启 Gateway

```bash
openclaw gateway restart
```

### 步骤 5：验证安装

```bash
export BAIDU_API_KEY="你的 API_KEY"
cd /home/seasky7/.openclaw/workspace/skills/baidu-search
python3 scripts/search.py '{"query":"OpenClaw 是什么","count":3}'
```

---

## 📖 使用方法

### 基本用法

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"搜索关键词"}'
```

### 完整参数格式

```bash
python3 skills/baidu-search/scripts/search.py '{
  "query": "搜索关键词",
  "count": 10,
  "freshness": "pd"
}'
```

---

## ⚙️ 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | str | ✅ 是 | - | 搜索查询词 |
| `count` | int | ❌ 否 | 10 | 返回结果数量（范围：1-50） |
| `freshness` | str | ❌ 否 | null | 时间范围筛选 |

### `freshness` 参数格式

**格式一：日期范围**
```
"YYYY-MM-DDtoYYYY-MM-DD"
```
示例：`"2026-03-01to2026-03-13"`

**格式二：相对时间**
| 代码 | 含义 |
|------|------|
| `pd` | 过去 24 小时（past day） |
| `pw` | 过去 7 天（past week） |
| `pm` | 过去 31 天（past month） |
| `py` | 过去 365 天（past year） |

---

## 💡 使用示例

### 1. 基本搜索

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"人工智能"}'
```

### 2. 指定结果数量

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"旅游景点","count":20}'
```

### 3. 搜索最新新闻（过去 24 小时）

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"最新新闻","freshness":"pd"}'
```

### 4. 搜索过去一周的内容

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"科技动态","freshness":"pw"}'
```

### 5. 指定日期范围搜索

```bash
python3 skills/baidu-search/scripts/search.py '{"query":"两会报道","freshness":"2026-03-01to2026-03-13"}'
```

### 6. 组合使用

```bash
python3 skills/baidu-search/scripts/search.py '{
  "query":"法律科技",
  "count":15,
  "freshness":"pm"
}'
```

---

## 📋 返回结果格式

```json
[
  {
    "id": 1,
    "url": "https://example.com/article/123",
    "title": "文章标题",
    "date": "2026-03-12 18:00:00",
    "content": "内容摘要...",
    "icon": "https://example.com/favicon.ico",
    "website": "网站名称",
    "rerank_score": 1,
    "authority_score": 1
  }
]
```

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 结果序号 |
| `url` | str | 文章链接 |
| `title` | str | 文章标题 |
| `date` | str | 发布日期时间 |
| `content` | str | 内容摘要 |
| `icon` | str | 网站图标 |
| `website` | str | 来源网站名称 |
| `rerank_score` | float | 重排序得分 |
| `authority_score` | float | 权威性得分（0-1） |

---

## 🔧 常见问题

### 1. 报错：`BAIDU_API_KEY must be set in environment`

**原因**：环境变量未设置或未生效

**解决方法**：
```bash
# 临时设置（当前终端有效）
export BAIDU_API_KEY="你的 API_KEY"

# 永久设置（需重启 Gateway）
nano /home/seasky7/.openclaw/.env
# 添加 BAIDU_API_KEY="你的 API_KEY"
openclaw gateway restart
```

### 2. 报错：`Invalid API Key`

**原因**：API Key 格式错误或已失效

**解决方法**：
- 检查 API Key 格式是否为 `bce-v3/ALTAK-xxx/xxx`
- 登录百度智能云控制台重新生成

### 3. 搜索结果数量为 0

**原因**：搜索词太冷门或时间范围太窄

**解决方法**：
- 尝试更通用的搜索词
- 扩大时间范围或移除 `freshness` 参数

### 4. 技能未找到

**原因**：技能未正确安装

**解决方法**：
```bash
clawhub install baidu-search --registry https://clawhub.ai
```

---

## 📊 配额与限制

| 项目 | 限制 |
|------|------|
| 单次搜索最大结果数 | 50 条 |
| API 调用频率 | 请参考百度智能云控制台配额 |
| 支持的地域 | 中国大陆 |

---

## 🔗 相关资源

- **百度智能云控制台**：https://console.bce.baidu.com/
- **百度 AI 搜索文档**：https://cloud.baidu.com/doc/BDSE/index.html
- **ClawHub 技能市场**：https://clawhub.ai/
- **OpenClaw 文档**：https://docs.openclaw.ai/

---

## 📝 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-13 | 初始版本，支持基本搜索、时间筛选、结果数量控制 |

---

## 👤 维护者

- **安装配置**：seasky7
- **配置时间**：2026-03-13
- **API Key 位置**：`/home/seasky7/.openclaw/.env`

---

_最后更新：2026-03-13_
