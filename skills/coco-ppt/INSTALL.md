# COCO-PPT 技能安装指南

## 快速安装

### 1. 安装 Python 依赖

```bash
cd ~/.agents/skills/coco-ppt
pip install -r requirements.txt
```

### 2. 安装 LibreOffice（可选，用于缩略图生成）

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y libreoffice
```

**macOS:**
```bash
brew install libreoffice
```

**Windows:**
从 https://www.libreoffice.org/download/ 下载并安装

### 3. 验证安装

```bash
# 运行测试脚本
bash test_skill.sh

# 或手动测试
python3 scripts/coco-ppt.py --help
```

## 依赖说明

### Python 依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| python-pptx | >=0.6.21 | PPTX 文件操作 |
| Pillow | >=9.0.0 | 图像处理 |
| defusedxml | >=0.7.1 | XML 解析 |
| click | >=8.0.0 | 命令行接口 |
| rich | >=12.0.0 | 美化输出 |

### 系统依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| Python 3.8+ | 运行环境 | ✅ |
| LibreOffice | 缩略图生成 | ❌ (可选) |

## 使用方法

### 基本用法

```bash
python3 scripts/coco-ppt.py \
  --template /path/to/template.pptx \
  --outline /path/to/outline.md \
  --output /path/to/output.pptx
```

### 完整示例

```bash
# 进入技能目录
cd ~/.agents/skills/coco-ppt

# 使用示例文件测试
python3 scripts/coco-ppt.py \
  --template examples/sample.pptx \
  --outline examples/sample-outline.md \
  --output ~/test-presentation.pptx \
  --report \
  --thumbnails
```

## 常见问题

### Q: pip install 失败？

**A:** 尝试使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: LibreOffice 安装失败？

**A:** 缩略图功能是可选的。不安装 LibreOffice 仍可正常使用 PPT 生成功能，只是无法生成缩略图预览。

### Q: 模板验证失败？

**A:** 确保：
- 模板文件是 `.pptx` 格式（不是 `.ppt`）
- 模板中至少有 2 个版式
- 模板文件未损坏（能用 PowerPoint 或 LibreOffice 打开）

### Q: 文本溢出警告？

**A:** 这是正常提示，不影响生成。如需避免：
- 减少单张幻灯片的内容量
- 使用版式更丰富的模板
- 调整内容结构

## 升级技能

```bash
cd ~/.agents/skills/coco-ppt
git pull origin main  # 如果是 git 安装
# 或重新下载最新版本
```

## 卸载技能

```bash
rm -rf ~/.agents/skills/coco-ppt
```

## 获取帮助

```bash
# 查看命令行帮助
python3 scripts/coco-ppt.py --help

# 查看技能文档
cat SKILL.md

# 查看架构文档
cat docs/architecture.md
```

---

**技能位置**: `~/.agents/skills/coco-ppt/`
**作者**: seasky7
**许可证**: MIT
