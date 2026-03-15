"""
Semantic Scholar 数据源适配器

Semantic Scholar API: https://www.semanticscholar.org/product/api
免费 API Key，5000 次/天限额
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime


class SemanticScholarSource:
    """Semantic Scholar 论文检索适配器"""
    
    def __init__(self, api_key: Optional[str] = None, max_results: int = 10):
        """
        初始化 Semantic Scholar 检索器
        
        Args:
            api_key: Semantic Scholar API Key（可选，无 Key 限额 100 次/天）
            max_results: 最大结果数量
        """
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    def search(self, query: str, **kwargs) -> List[Dict]:
        """
        检索 Semantic Scholar 论文
        
        Args:
            query: 检索词
            **kwargs: 其他参数（limit, year, fields 等）
        
        Returns:
            论文列表（统一格式）
        """
        results = []
        
        # 构建请求参数
        params = {
            'query': query,
            'limit': kwargs.get('limit', self.max_results),
            'fields': 'title,authors,year,venue,abstract,citationCount,externalIds,url,doi,publicationTypes,journal,referenceCount'
        }
        
        # 添加年份范围
        if 'after' in kwargs and kwargs['after']:
            year = int(kwargs['after'].split('-')[0])
            params['year'] = f'{year}-'
        
        if 'before' in kwargs and kwargs['before']:
            year = int(kwargs['before'].split('-')[0])
            if 'year' in params:
                params['year'] = f"{params['year'].rstrip('-')}-{year}"
            else:
                params['year'] = f"-{year}"
        
        # 添加 API Key（如果有）
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('data', []):
                # 提取作者列表
                authors = []
                if 'authors' in item and item['authors']:
                    authors = [a['name'] for a in item['authors'] if a.get('name')]
                
                paper_data = {
                    'id': f"semantic_scholar:{item.get('paperId', '')}",
                    'title': item.get('title', ''),
                    'authors': authors,
                    'year': item.get('year'),
                    'venue': item.get('venue', {}).get('name') if item.get('venue') else item.get('journal', {}).get('name', ''),
                    'source': 'semantic_scholar',
                    'url': item.get('url', ''),
                    'pdf_url': None,  # Semantic Scholar 不直接提供 PDF
                    'doi': item.get('doi'),
                    'abstract': item.get('abstract'),
                    'citations': item.get('citationCount'),
                    'subjects': item.get('publicationTypes', []),
                    'references_count': item.get('referenceCount'),
                    'retrieved_at': datetime.now().isoformat()
                }
                results.append(paper_data)
        
        except requests.exceptions.RequestException as e:
            print(f"Semantic Scholar 检索错误：{e}")
        except Exception as e:
            print(f"Semantic Scholar 解析错误：{e}")
        
        return results
    
    def get_name(self) -> str:
        """返回数据源名称"""
        return "Semantic Scholar"
    
    def get_description(self) -> str:
        """返回数据源描述"""
        return "AI 驱动的学术搜索引擎，提供引用分析"
