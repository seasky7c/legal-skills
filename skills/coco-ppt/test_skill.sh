#!/bin/bash
# COCO-PPT 技能测试脚本

set -e

SKILL_DIR="$HOME/.agents/skills/coco-ppt"
TEST_DIR="/tmp/coco-ppt-test-$$"

echo "🧪 COCO-PPT 技能测试"
echo "===================="
echo ""

# 创建测试目录
mkdir -p "$TEST_DIR"

# 检查依赖
echo "1. 检查依赖..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python3 已安装"

if ! python3 -c "import pptx" 2>/dev/null; then
    echo "⚠️  python-pptx 未安装，正在安装..."
    pip install python-pptx
fi
echo "✅ python-pptx 已安装"

if ! python3 -c "import click" 2>/dev/null; then
    echo "⚠️  click 未安装，正在安装..."
    pip install click
fi

if ! python3 -c "import rich" 2>/dev/null; then
    echo "⚠️  rich 未安装，正在安装..."
    pip install rich
fi

echo ""
echo "2. 安装技能依赖..."
cd "$SKILL_DIR"
pip install -r requirements.txt -q
echo "✅ 依赖安装完成"

echo ""
echo "3. 检查技能文件结构..."
required_files=(
    "SKILL.md"
    "scripts/coco-ppt.py"
    "src/__init__.py"
    "requirements.txt"
    "examples/sample-outline.md"
)

all_ok=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        all_ok=false
    fi
done

if [ "$all_ok" = false ]; then
    echo ""
    echo "❌ 技能文件不完整"
    exit 1
fi

echo ""
echo "4. 测试命令行帮助..."
python3 scripts/coco-ppt.py --help > /dev/null 2>&1
echo "✅ 命令行工具正常"

echo ""
echo "5. 测试分析模式（使用示例文件）..."
python3 scripts/coco-ppt.py \
    --template examples/sample.pptx \
    --outline examples/sample-outline.md \
    --analyze-only \
    --report \
    --log-level ERROR \
    2>&1 | head -20 || echo "⚠️  分析测试需要示例模板文件"

echo ""
echo "===================="
echo "✅ 技能测试完成！"
echo ""
echo "使用技能："
echo "  python3 $SKILL_DIR/scripts/coco-ppt.py --template <模板> --outline <大纲> --output <输出>"
echo ""

# 清理测试目录
rm -rf "$TEST_DIR"
