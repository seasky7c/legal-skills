"""
DOAJ 数据源适配器

DOAJ: https://doaj.org/
开放获取期刊目录
免费 API，无需认证
"""

import requests
from typing import List, Dict
from datetime import datetime


class DOAJSource:
    """DOAJ 开放获取期刊论文检索适配器"""
    
    def __init__(self, max_results: int = 10):
        """
        初始化 DOAJ 检索器
        
        Args:
            max_results: 最大结果数量
        """
        self.max_results = max_results
        self.base_url = "https://doaj.org/api/v3/search/articles"
    
    def search(self, query: str, **kwargs) -> List[Dict]:
        """
        检索 DOAJ 论文
        
        Args:
            query: 检索词
            **kwargs: 其他参数
        
        Returns:
            论文列表（统一格式）
        """
        results = []
        
        # 构建检索参数
        search_query = {
            "query": {
                "query_string": {
                    "query": query
                }
            },
            "size": kwargs.get('limit', self.max_results)
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=search_query,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('results', []):
                article = item.get('article', {})
                
                paper_data = {
                    'id': f"doaj:{article.get('id', '')}",
                    'title': article.get('title', ''),
                    'authors': [a.get('name', '') for a in article.get('author', [])],
                    'year': None,  # DOAJ 不直接提供年份
                    'venue': article.get('journal', {}).get('title', ''),
                    'source': 'doaj',
                    'url': article.get('link', [{}])[0].get('url', ''),
                    'pdf_url': None,
                    'doi': article.get('doi'),
                    'abstract': article.get('abstract', ''),
                    'citations': None,
                    'subjects': article.get('subject', []),
                    'license': article.get('license', [{}])[0].get('name', ''),
                    'retrieved_at': datetime.now().isoformat()
                }
                results.append(paper_data)
        
        except requests.exceptions.RequestException as e:
            print(f"DOAJ 检索错误：{e}")
        except Exception as e:
            print(f"DOAJ 解析错误：{e}")
        
        return results
    
    def get_name(self) -> str:
        return "DOAJ"
    
    def get_description(self) -> str:
        return "开放获取期刊目录"
