#!/usr/bin/env python3
"""
Scrapling Web Extractor - 通用网页内容提取工具

支持任意网站的内容抓取，包括静态和动态页面。
输出格式：Markdown / JSON / 纯文本
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

try:
    from scrapling import Fetcher
except ImportError:
    print("❌ 错误：scrapling 未安装，请先运行：pip install scrapling")
    sys.exit(1)


class WebExtractor:
    """通用网页提取器"""
    
    def __init__(self, timeout: int = 30000):
        self.timeout = timeout
        self.fetcher = Fetcher()
    
    def extract(self, url: str, use_browser: bool = False, 
                selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        提取网页内容
        
        Args:
            url: 网页 URL
            use_browser: 是否使用浏览器模式（适合 JavaScript 渲染的页面）
            selectors: 自定义选择器
        
        Returns:
            提取结果字典
        """
        result = {
            'url': url,
            'title': '',
            'author': '',
            'publish_time': '',
            'source': '',
            'content': '',
            'paragraphs': [],
            'images': [],
            'extracted_at': datetime.now().isoformat(),
            'status': 'success'
        }
        
        try:
            # 获取页面
            print(f"[INFO] Fetching: {url}")
            page = self.fetcher.get(url, timeout=self.timeout)
            
            if page.status != 200:
                result['status'] = f'failed: HTTP {page.status}'
                print(f"[ERROR] HTTP {page.status}")
                return result
            
            print(f"[INFO] Status: {page.status}")
            
            # 提取标题
            title_selectors = [
                '//h1[@id="activity-name"]//text()',
                '//h1[@class="rich_media_title"]//text()',
                '//h1[@class="article-title"]//text()',
                '//h1[@class="title"]//text()',
                '//title//text()',
            ]
            
            for sel in (selectors or {}).get('title', title_selectors) if isinstance((selectors or {}).get('title', title_selectors), list) else [selectors.get('title', '')]:
                title = page.xpath(sel).getall()
                if title and title[0].strip():
                    result['title'] = title[0].strip()
                    break
            
            # 如果还是没找到，尝试获取所有文本的第一个非空行
            if not result['title']:
                all_text = page.get_all_text()
                lines = [l.strip() for l in all_text.split('\n') if l.strip()]
                if lines:
                    result['title'] = lines[0][:200]
            
            print(f"[INFO] Title: {result['title'][:100]}...")
            
            # 提取作者
            author_selectors = [
                '//span[@id="js_author_name_text"]//text()',
                '//span[@class="author-name"]//text()',
                '//a[@id="js_name"]//text()',
                '//span[@class="author"]//text()',
                '//meta[@name="author"]/@content',
            ]
            
            for sel in author_selectors:
                author = page.xpath(sel).getall()
                if author and author[0].strip():
                    result['author'] = author[0].strip()
                    break
            
            # 提取发布时间
            time_selectors = [
                '//em[@id="publish_time"]//text()',
                '//span[@class="publish-time"]//text()',
                '//time[@datetime]/@datetime',
                '//span[@class="time"]//text()',
            ]
            
            for sel in time_selectors:
                pub_time = page.xpath(sel).getall()
                if pub_time and pub_time[0].strip():
                    result['publish_time'] = pub_time[0].strip()
                    break
            
            # 提取正文段落
            content_selectors = [
                '//div[@id="js_content"]//p//text()',
                '//div[@class="article-content"]//p//text()',
                '//article//p//text()',
                '//div[@class="rich_media_content"]//p//text()',
                '//div[@id="content"]//p//text()',
            ]
            
            for sel in content_selectors:
                paragraphs = page.xpath(sel).getall()
                if paragraphs:
                    result['paragraphs'] = [p.strip() for p in paragraphs if p.strip() and len(p.strip()) > 5]
                    break
            
            # 如果没找到段落，尝试获取所有文本
            if not result['paragraphs']:
                all_text = page.get_all_text()
                if all_text:
                    # 按空行分割
                    paragraphs = [p.strip() for p in all_text.split('\n\n') if p.strip() and len(p.strip()) > 10]
                    result['paragraphs'] = paragraphs[:100]  # 限制最多 100 段
            
            print(f"[INFO] Paragraphs: {len(result['paragraphs'])}")
            
            # 提取图片
            img_selectors = [
                '//div[@id="js_content"]//img/@src',
                '//div[@class="article-content"]//img/@src',
                '//article//img/@src',
                '//img/@src',
            ]
            
            for sel in img_selectors:
                images = page.xpath(sel).getall()
                if images:
                    result['images'] = [img for img in images if img.startswith('http')]
                    break
            
            # 组合内容
            result['content'] = '\n\n'.join(result['paragraphs'])
            
            # 提取来源
            parsed = urlparse(url)
            result['source'] = parsed.netloc.replace('www.', '')
            
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            print(f"[ERROR] {e}")
        
        return result
    
    def to_markdown(self, result: Dict[str, Any]) -> str:
        """转换为 Markdown 格式"""
        md = f"# {result['title']}\n\n"
        
        if result['author']:
            md += f"**作者**: {result['author']}  \n"
        if result['publish_time']:
            md += f"**发布时间**: {result['publish_time']}  \n"
        if result['source']:
            md += f"**来源**: {result['source']}  \n"
        
        md += f"**链接**: {result['url']}  \n"
        md += f"**提取时间**: {result['extracted_at']}\n\n"
        md += "---\n\n"
        
        md += result['content']
        
        if result['images']:
            md += "\n\n---\n\n## 图片\n\n"
            for i, img in enumerate(result['images'], 1):
                md += f"![图片{i}]({img})\n"
        
        return md
    
    def to_json(self, result: Dict[str, Any]) -> str:
        """转换为 JSON 格式"""
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Scrapling 网页内容提取器')
    parser.add_argument('url', nargs='?', help='要提取的网页 URL')
    parser.add_argument('--output', '-o', default='./output', help='输出目录')
    parser.add_argument('--format', '-f', choices=['markdown', 'json', 'text'], 
                        default='markdown', help='输出格式')
    parser.add_argument('--browser', '-b', action='store_true', 
                        help='使用浏览器模式（适合动态页面）')
    parser.add_argument('--batch', help='批量提取，从文件读取 URL 列表')
    
    args = parser.parse_args()
    
    if not args.url and not args.batch:
        parser.print_help()
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    extractor = WebExtractor()
    
    # 收集 URLs
    urls = []
    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    elif args.url:
        urls = [args.url]
    
    # 提取
    for url in urls:
        print(f"\n{'='*60}")
        result = extractor.extract(url, use_browser=args.browser)
        
        # 生成文件名
        parsed = urlparse(url)
        url_id = parsed.path.split('/')[-1] or 'article'
        url_id = url_id.split('?')[0][:50]
        
        # 输出
        if args.format == 'markdown':
            output = extractor.to_markdown(result)
            filename = f"{url_id}.md"
        elif args.format == 'json':
            output = extractor.to_json(result)
            filename = f"{url_id}.json"
        else:
            output = result['content']
            filename = f"{url_id}.txt"
        
        # 保存
        output_path = os.path.join(args.output, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"[SUCCESS] Saved: {output_path}")
        print(f"[INFO] File size: {len(output)} chars")


if __name__ == '__main__':
    main()
