#!/usr/bin/env python3
"""
Legal Paper Search - 社会科学/法律类论文统一检索

用法:
    python3 legal_paper_search.py "检索词" [选项]
    python3 legal_paper_search.py --topic legal_tech [选项]

示例:
    python3 legal_paper_search.py "legal AI" --source arxiv core
    python3 legal_paper_search.py --topic judicial_ai --limit 20 --output results.md
"""

import click
import json
from datetime import datetime
from typing import List, Dict, Optional
import sys
import os

# 添加数据源
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sources import ArxivSource, CoreSource, SemanticScholarSource, DOAJSource


@click.command()
@click.argument('query', required=False, default='')
@click.option('--topic', type=click.Choice(['legal_tech', 'judicial_ai', 'contract_review', 'legal_nlp', 'sentencing_prediction']),
              help='预设检索主题')
@click.option('--source', multiple=True, default=['arxiv'], 
              type=click.Choice(['arxiv', 'core', 'semantic_scholar', 'doaj']),
              help='数据源（可多选）')
@click.option('--limit', default=10, help='每个数据源的最大结果数')
@click.option('--output', help='输出文件路径（.json/.md/.bib）')
@click.option('--format', 'output_format', type=click.Choice(['json', 'markdown', 'bibtex']),
              help='输出格式（默认根据文件扩展名）')
@click.option('--after', help='起始年份（YYYY-MM-DD）')
@click.option('--before', help='结束年份（YYYY-MM-DD）')
@click.option('--verbose', is_flag=True, help='显示详细信息')
def main(query, topic, source, limit, output, output_format, after, before, verbose):
    """
    Legal Paper Search - 社会科学/法律类论文统一检索工具
    """
    
    # 处理预设主题
    if topic:
        topic_queries = get_topic_queries()
        if topic in topic_queries:
            query = topic_queries[topic][0]  # 使用第一个检索词
            click.echo(f"📌 使用预设主题：{topic}")
            click.echo(f"🔍 检索词：{query}")
    
    if not query:
        click.echo("❌ 错误：请提供检索词或使用 --topic 选项")
        click.echo("使用 --help 查看用法")
        sys.exit(1)
    
    # 显示检索信息
    click.echo("=" * 60)
    click.echo("📚 Legal Paper Search - 法律类论文检索")
    click.echo("=" * 60)
    click.echo(f"🔍 检索词：{query}")
    click.echo(f"📊 数据源：{', '.join(source)}")
    click.echo(f"📈 每源限制：{limit} 篇")
    if after:
        click.echo(f"📅 起始时间：{after}")
    if before:
        click.echo(f"📅 结束时间：{before}")
    click.echo("=" * 60)
    
    # 执行检索
    all_results = []
    
    for source_name in source:
        click.echo(f"\n🔎 检索 {source_name}...")
        
        try:
            if source_name == 'arxiv':
                src = ArxivSource(max_results=limit)
            elif source_name == 'core':
                src = CoreSource(max_results=limit)
            elif source_name == 'semantic_scholar':
                src = SemanticScholarSource(max_results=limit)
            elif source_name == 'doaj':
                src = DOAJSource(max_results=limit)
            else:
                click.echo(f"⚠️ 不支持的数据源：{source_name}")
                continue
            
            results = src.search(query, limit=limit, after=after, before=before)
            click.echo(f"   ✅ 找到 {len(results)} 篇")
            all_results.extend(results)
        
        except Exception as e:
            click.echo(f"   ❌ 错误：{e}")
    
    # 去重（按标题）
    unique_results = []
    seen_titles = set()
    for paper in all_results:
        title_key = paper['title'].lower().strip()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_results.append(paper)
    
    click.echo("\n" + "=" * 60)
    click.echo(f"📊 总计：{len(unique_results)} 篇（去重后）")
    click.echo("=" * 60)
    
    # 输出结果
    if output:
        # 自动检测格式
        if not output_format:
            if output.endswith('.json'):
                output_format = 'json'
            elif output.endswith('.md'):
                output_format = 'markdown'
            elif output.endswith('.bib'):
                output_format = 'bibtex'
            else:
                output_format = 'json'
        
        export_results(unique_results, query, source, output, output_format, verbose)
    else:
        # 显示前 5 篇
        click.echo("\n📄 最新 5 篇论文：\n")
        for i, paper in enumerate(unique_results[:5], 1):
            click.echo(f"【{i}】{paper['title']}")
            click.echo(f"    作者：{', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}")
            click.echo(f"    来源：{paper['source']} | 年份：{paper['year']}")
            click.echo(f"    URL: {paper['url']}")
            click.echo()


def get_topic_queries() -> Dict[str, List[str]]:
    """获取预设主题的检索词"""
    return {
        'legal_tech': ['legal technology', 'legal tech', 'law technology'],
        'judicial_ai': ['judicial artificial intelligence', 'AI in judiciary', 'smart court'],
        'contract_review': ['contract review AI', 'automated contract analysis', 'contract understanding'],
        'legal_nlp': ['legal natural language processing', 'legal text analysis', 'law NLP'],
        'sentencing_prediction': ['sentencing prediction', 'judgment prediction', 'court decision prediction']
    }


def export_results(results: List[Dict], query: str, sources: List[str], 
                   output_path: str, output_format: str, verbose: bool = False):
    """导出检索结果"""
    
    metadata = {
        'query': query,
        'sources': sources,
        'total_results': len(results),
        'retrieved_at': datetime.now().isoformat()
    }
    
    try:
        if output_format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'metadata': metadata, 'papers': results}, f, ensure_ascii=False, indent=2)
        
        elif output_format == 'markdown':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# 法律类论文检索结果\n\n")
                f.write(f"**检索词**: {query}  \n")
                f.write(f"**数据源**: {', '.join(sources)}  \n")
                f.write(f"**检索时间**: {metadata['retrieved_at']}  \n")
                f.write(f"**结果数量**: {len(results)} 篇\n\n")
                f.write("---\n\n")
                
                for i, paper in enumerate(results, 1):
                    f.write(f"## 【{i}】{paper['title']}\n\n")
                    f.write(f"**作者**: {', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}  \n")
                    f.write(f"**年份**: {paper['year']}  \n")
                    f.write(f"**来源**: {paper['source']}  \n")
                    if paper.get('venue'):
                        f.write(f"**期刊/会议**: {paper['venue']}  \n")
                    if paper.get('doi'):
                        f.write(f"**DOI**: {paper['doi']}  \n")
                    f.write(f"**摘要**: {paper['abstract'][:300]}...  \n")
                    f.write(f"**URL**: {paper['url']}  \n")
                    if paper.get('pdf_url'):
                        f.write(f"**PDF**: {paper['pdf_url']}  \n")
                    f.write("\n---\n\n")
        
        elif output_format == 'bibtex':
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, paper in enumerate(results, 1):
                    # 生成 BibTeX key
                    first_author = paper['authors'][0].split()[-1].lower() if paper['authors'] else 'unknown'
                    year = paper['year'] or 'nodate'
                    key = f"{first_author}{year}{i}"
                    
                    f.write(f"@article{{{key},\n")
                    f.write(f"  title={{{paper['title']}}},\n")
                    f.write(f"  author={' and '.join(paper['authors'])},\n")
                    f.write(f"  year={{{year}}},\n")
                    if paper.get('venue'):
                        f.write(f"  journal={{{paper['venue']}}},\n")
                    if paper.get('doi'):
                        f.write(f"  doi={{{paper['doi']}}},\n")
                    f.write(f"  url={{{paper['url']}}},\n")
                    f.write(f"}}\n\n")
        
        click.echo(f"\n✅ 结果已保存到：{output_path}")
    
    except Exception as e:
        click.echo(f"\n❌ 导出失败：{e}")


if __name__ == '__main__':
    main()
