"""
CORE 数据源适配器

CORE API: https://core.ac.uk/services/documentation/
免费 API Key，1000 次/小时限额
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime


class CoreSource:
    """CORE 开放获取论文检索适配器"""
    
    def __init__(self, api_key: Optional[str] = None, max_results: int = 10):
        """
        初始化 CORE 检索器
        
        Args:
            api_key: CORE API Key（可选，无 Key 限额 100 次/小时）
            max_results: 最大结果数量
        """
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://api.core.ac.uk/v3/search/outputs"
    
    def search(self, query: str, **kwargs) -> List[Dict]:
        """
        检索 CORE 论文
        
        Args:
            query: 检索词
            **kwargs: 其他参数（limit, after, before 等）
        
        Returns:
            论文列表（统一格式）
        """
        results = []
        
        # 构建请求参数
        params = {
            'q': query,
            'limit': kwargs.get('limit', self.max_results),
        }
        
        # 添加 API Key（如果有）
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('results', []):
                paper_data = {
                    'id': f"core:{item.get('id', '')}",
                    'title': item.get('title', ''),
                    'authors': item.get('authors', []),
                    'year': item.get('publishedYear'),
                    'venue': item.get('sourceTitle', ''),
                    'source': 'core',
                    'url': item.get('sourceUrl', ''),
                    'pdf_url': item.get('fullTextPdfUrl', ''),
                    'doi': item.get('doi'),
                    'abstract': item.get('abstract', ''),
                    'citations': None,
                    'subjects': item.get('topics', []),
                    'language': item.get('language'),
                    'retrieved_at': datetime.now().isoformat()
                }
                results.append(paper_data)
        
        except requests.exceptions.RequestException as e:
            print(f"CORE 检索错误：{e}")
        except Exception as e:
            print(f"CORE 解析错误：{e}")
        
        return results
    
    def get_name(self) -> str:
        """返回数据源名称"""
        return "CORE"
    
    def get_description(self) -> str:
        """返回数据源描述"""
        return "开放获取学术论文聚合平台（1.3 亿 + 篇）"
