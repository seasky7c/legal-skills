"""
arXiv 数据源适配器

arXiv API: https://arxiv.org/help/api
无需 API Key，免费开放访问
"""

import arxiv
from typing import List, Dict, Optional
from datetime import datetime


class ArxivSource:
    """arXiv 论文检索适配器"""
    
    def __init__(self, max_results: int = 10, sort_by: str = 'relevance'):
        """
        初始化 arXiv 检索器
        
        Args:
            max_results: 最大结果数量
            sort_by: 排序方式 ('relevance', 'lastUpdatedDate', 'submittedDate')
        """
        self.max_results = max_results
        self.sort_by = getattr(arxiv.SortCriterion, sort_by, arxiv.SortCriterion.Relevance)
        self.client = arxiv.Client()
    
    def search(self, query: str, **kwargs) -> List[Dict]:
        """
        检索 arXiv 论文
        
        Args:
            query: 检索词
            **kwargs: 其他参数（after, before, subject 等）
        
        Returns:
            论文列表（统一格式）
        """
        results = []
        
        # 构建检索条件
        search_kwargs = {
            'query': query,
            'max_results': kwargs.get('limit', self.max_results),
            'sort_by': self.sort_by,
            'sort_order': arxiv.SortOrder.Descending
        }
        
        try:
            search = arxiv.Search(**search_kwargs)
            
            for paper in self.client.results(search):
                paper_data = {
                    'id': f"arxiv:{paper.entry_id.split('/')[-1]}",
                    'title': paper.title,
                    'authors': [a.name for a in paper.authors],
                    'year': paper.published.year if paper.published else None,
                    'venue': 'arXiv preprint',
                    'source': 'arxiv',
                    'url': paper.entry_id,
                    'pdf_url': paper.pdf_url,
                    'doi': paper.doi,
                    'abstract': paper.summary,
                    'citations': None,  # arXiv 不提供引用数
                    'subjects': paper.categories,
                    'arxiv_id': paper.entry_id.split('/')[-1],
                    'comment': paper.comment,
                    'retrieved_at': datetime.now().isoformat()
                }
                results.append(paper_data)
        
        except Exception as e:
            print(f"arXiv 检索错误：{e}")
        
        return results
    
    def get_name(self) -> str:
        """返回数据源名称"""
        return "arXiv"
    
    def get_description(self) -> str:
        """返回数据源描述"""
        return "预印本论文库，含 AI、机器学习、计算语言学等领域"
