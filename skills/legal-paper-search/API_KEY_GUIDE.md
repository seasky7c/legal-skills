# API Key 快速申请指南

> 5 分钟内完成，完全免费

---

## 🎯 为什么需要 API Key

| 数据源 | 无 Key 限额 | 有 Key 限额 | 提升倍数 |
|--------|-----------|-----------|---------|
| Semantic Scholar | 100 次/天 | 5000 次/天 | **50 倍** |
| CORE | 100 次/小时 | 1000 次/小时 | **10 倍** |
| arXiv | 无限 | 无限 | 无需 Key |
| DOAJ | 无限 | 无限 | 无需 Key |

**建议**: 经常使用建议申请，偶尔使用可不申请

---

## 📝 Semantic Scholar API Key 申请

### 步骤 1: 访问官网
```
https://www.semanticscholar.org/product/api
```

### 步骤 2: 注册账号
- 点击右上角 **"Sign Up"** 或 **"Get API Key"**
- 使用邮箱注册（推荐工作邮箱或 Gmail）
- 设置密码

### 步骤 3: 验证邮箱
- 查收验证邮件
- 点击验证链接

### 步骤 4: 获取 API Key
- 登录后自动进入 API 管理页面
- 复制 API Key（格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）
- **保存到安全位置**

### 步骤 5: 配置
编辑 `config.json`：
```json
{
  "semantic_scholar": {
    "api_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

### ⏱️ 预计时间
- 注册：2 分钟
- 验证：1 分钟
- 配置：1 分钟
- **总计：4 分钟**

---

## 📝 CORE API Key 申请

### 步骤 1: 访问文档页
```
https://core.ac.uk/services/documentation/
```

### 步骤 2: 点击申请
- 点击 **"Get an API Key"** 按钮

### 步骤 3: 填写申请表
```
Name: 你的姓名（拼音）
Email: 你的邮箱
Organization: 单位（可选，如 University/Company）
Intended use: Research / Personal use
```

### 步骤 4: 提交并接收
- 点击 **"Submit"**
- API Key 立即发送到邮箱
- 格式：一串字母数字组合

### 步骤 5: 配置
编辑 `config.json`：
```json
{
  "core": {
    "api_key": "你的 CORE API Key"
  }
}
```

### ⏱️ 预计时间
- 填写：2 分钟
- 接收：1 分钟
- 配置：1 分钟
- **总计：4 分钟**

---

## 🔒 安全提示

### ✅ 推荐做法
- 将 `config.json` 添加到 `.gitignore`
- 不要将 API Key 上传到 GitHub
- 定期更换 API Key

### ❌ 避免做法
- 不要公开分享 API Key
- 不要提交到代码仓库
- 不要在公共论坛发布

---

## 📧 常见问题

### Q: 申请被拒怎么办？
A: CORE 可能会人工审核，确保填写真实用途。如被拒，可邮件联系 support@core.ac.uk

### Q: API Key 有效期多久？
A: 永久有效，除非违反使用条款

### Q: 可以多人共用一个 Key 吗？
A: 不建议，配额是共享的，且违反使用条款

### Q: 配额用完了怎么办？
A: 等第二天/下个小时重置，或申请提高配额（需说明理由）

### Q: 忘记 API Key 怎么办？
A: 登录账户重新查看，或邮件联系客服

---

## 📞 客服联系

### Semantic Scholar
- 邮箱：api-support@semanticscholar.org
- 文档：https://www.semanticscholar.org/product/api

### CORE
- 邮箱：support@core.ac.uk
- 文档：https://core.ac.uk/services/documentation/

---

## 🎉 申请完成后

1. 复制 `config.template.json` 为 `config.json`
2. 填入你的 API Key
3. 运行检索测试：
   ```bash
   python3 scripts/legal_paper_search.py "legal AI" --source semantic_scholar
   ```

---

_最后更新：2026-03-16_
