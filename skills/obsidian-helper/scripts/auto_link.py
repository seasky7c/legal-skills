#!/usr/bin/env python3
"""
自动为 Obsidian 笔记添加双向链接

功能：
1. 扫描知识库，获取所有笔记标题
2. 为指定 Markdown 文件添加 Wikilinks
3. 支持白名单（只链接特定笔记）
4. 支持黑名单（跳过特定笔记）

使用方式：
python3 auto_link.py <文件路径>
python3 auto_link.py <文件路径> --vault ~/Obsidian-Vault
python3 auto_link.py --all  # 处理所有笔记
"""

import re
import json
import argparse
from pathlib import Path
from typing import List, Set, Dict


def get_existing_notes(vault_path: Path) -> Dict[str, Path]:
    """
    获取知识库中所有笔记标题及其路径
    
    返回：{笔记标题：文件路径}
    """
    notes = {}
    
    # 排除的目录
    exclude_dirs = {
        '.git', '.obsidian', '.claude', 'node_modules',
        '10-Articles', '99-Archives', '99_System'
    }
    
    for md_file in vault_path.rglob("*.md"):
        # 跳过排除目录
        if any(exclude in str(md_file.parent) for exclude in exclude_dirs):
            continue
        
        # 使用文件名（不含扩展名）作为标题
        title = md_file.stem
        
        # 跳过太短的标题（可能是模板或配置）
        if len(title) < 2:
            continue
        
        notes[title] = md_file
    
    return notes


def load_config(vault_path: Path) -> Dict:
    """
    加载配置文件（如果存在）
    
    配置文件：_config/auto-link.json
    """
    config_file = vault_path / "_config" / "auto-link.json"
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 默认配置
    return {
        "whitelist": [],  # 白名单（只链接这些）
        "blacklist": [],  # 黑名单（跳过这些）
        "min_length": 2,  # 最小标题长度
        "exclude_dirs": ["10-Articles", "99-Archives", "99_System"]
    }


def add_wikilinks(content: str, existing_notes: Set[str], config: Dict) -> str:
    """
    为内容添加 Wikilinks
    
    规则：
    1. 跳过已有的 wikilinks（[[xxx]]）
    2. 跳过代码块内的内容
    3. 跳过 Frontmatter
    4. 优先匹配长标题（避免部分匹配）
    5. 遵守白名单/黑名单
    """
    whitelist = set(config.get("whitelist", []))
    blacklist = set(config.get("blacklist", []))
    min_length = config.get("min_length", 2)
    
    # 按长度排序，优先匹配长标题
    sorted_notes = sorted(existing_notes, key=len, reverse=True)
    
    # 过滤黑名单和长度
    notes_to_link = [
        note for note in sorted_notes
        if note not in blacklist and len(note) >= min_length
    ]
    
    # 如果有白名单，只链接白名单中的笔记
    if whitelist:
        notes_to_link = [note for note in notes_to_link if note in whitelist]
    
    # 分割内容，保留代码块和 Frontmatter
    # 使用占位符保护不需要处理的部分
    placeholders = {}
    placeholder_id = 0
    
    # 保护 Frontmatter
    frontmatter_match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if frontmatter_match:
        placeholder = f"__PLACEHOLDER_{placeholder_id}__"
        placeholders[placeholder] = frontmatter_match.group(0)
        content = content.replace(frontmatter_match.group(0), placeholder, 1)
        placeholder_id += 1
    
    # 保护代码块
    for match in re.finditer(r'```.*?```', content, re.DOTALL):
        placeholder = f"__PLACEHOLDER_{placeholder_id}__"
        placeholders[placeholder] = match.group(0)
        content = content.replace(match.group(0), placeholder, 1)
        placeholder_id += 1
    
    # 保护内联代码
    for match in re.finditer(r'`[^`]+`', content):
        placeholder = f"__PLACEHOLDER_{placeholder_id}__"
        placeholders[placeholder] = match.group(0)
        content = content.replace(match.group(0), placeholder, 1)
        placeholder_id += 1
    
    # 保护已有的 wikilinks
    for match in re.finditer(r'\[\[[^\]]+\]\]', content):
        placeholder = f"__PLACEHOLDER_{placeholder_id}__"
        placeholders[placeholder] = match.group(0)
        content = content.replace(match.group(0), placeholder, 1)
        placeholder_id += 1
    
    # 添加 Wikilinks
    for note in notes_to_link:
        # 使用单词边界匹配，避免部分匹配
        # 中文不需要单词边界，使用更宽松的模式
        pattern = r'(?<!\[)(?<!\[' + re.escape(note) + r')(?!\])(?!\])'
        
        # 跳过占位符中的内容
        def replace_func(match):
            matched_text = match.group(0)
            # 检查是否在占位符附近（简单启发式）
            start = match.start()
            context = content[max(0, start-50):start]
            if '__PLACEHOLDER_' in context:
                return matched_text
            return f'[[{note}]]'
        
        content = re.sub(pattern, replace_func, content, flags=re.IGNORECASE)
    
    # 恢复占位符
    for placeholder, original in placeholders.items():
        content = content.replace(placeholder, original)
    
    return content


def process_file(file_path: Path, vault_path: Path, config: Dict, dry_run: bool = False) -> Dict:
    """
    处理单个文件
    
    返回：{
        "file": 文件路径，
        "links_added": 添加的链接数量，
        "modified": 是否修改
    }
    """
    # 获取现有笔记
    existing_notes = set(get_existing_notes(vault_path).keys())
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # 添加 Wikilinks
    new_content = add_wikilinks(original_content, existing_notes, config)
    
    # 统计添加的链接数量
    original_links = len(re.findall(r'\[\[[^\]]+\]\]', original_content))
    new_links = len(re.findall(r'\[\[[^\]]+\]\]', new_content))
    links_added = new_links - original_links
    
    # 如果内容有变化，保存文件
    modified = original_content != new_content
    if modified and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return {
        "file": str(file_path),
        "links_added": links_added,
        "modified": modified
    }


def main():
    parser = argparse.ArgumentParser(description="自动为 Obsidian 笔记添加双向链接")
    parser.add_argument("file", nargs="?", help="要处理的文件路径")
    parser.add_argument("--vault", default="~/Obsidian-Vault", help="知识库路径")
    parser.add_argument("--all", action="store_true", help="处理所有笔记")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不修改文件")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    
    args = parser.parse_args()
    
    # 解析知识库路径
    vault_path = Path(args.vault).expanduser().resolve()
    
    if not vault_path.exists():
        print(f"❌ 知识库不存在：{vault_path}")
        return
    
    # 加载配置
    config = load_config(vault_path)
    
    # 显示统计信息
    if args.stats:
        existing_notes = get_existing_notes(vault_path)
        print(f"📊 知识库统计")
        print(f"  笔记总数：{len(existing_notes)}")
        print(f"  配置：{config}")
        return
    
    # 处理所有笔记
    if args.all:
        print(f"🔄 处理所有笔记...")
        files = list(vault_path.rglob("*.md"))
        # 排除配置目录
        files = [
            f for f in files
            if not any(exclude in str(f.parent) for exclude in config.get("exclude_dirs", []))
        ]
        
        total_links = 0
        modified_files = 0
        
        for file_path in files:
            result = process_file(file_path, vault_path, config, args.dry_run)
            total_links += result["links_added"]
            if result["modified"]:
                modified_files += 1
        
        print(f"✅ 完成！")
        print(f"  处理文件：{len(files)}")
        print(f"  修改文件：{modified_files}")
        print(f"  添加链接：{total_links}")
        return
    
    # 处理单个文件
    if args.file:
        file_path = Path(args.file).expanduser().resolve()
        if not file_path.exists():
            print(f"❌ 文件不存在：{file_path}")
            return
        
        result = process_file(file_path, vault_path, config, args.dry_run)
        
        if args.dry_run:
            print(f"👁️  预览模式")
        
        print(f"✅ 完成！")
        print(f"  文件：{result['file']}")
        print(f"  添加链接：{result['links_added']}")
        print(f"  已修改：{result['modified']}")
        return
    
    # 没有指定文件，显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
