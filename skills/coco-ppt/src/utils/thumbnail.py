"""
缩略图生成工具
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def generate_thumbnails(pptx_path: str, 
                        output_dir: str = ".", 
                        cols: int = 5) -> Optional[str]:
    """
    生成幻灯片缩略图网格
    
    Args:
        pptx_path: PPTX 文件路径
        output_dir: 输出目录
        cols: 每列数量
        
    Returns:
        输出文件路径，失败返回 None
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
    except ImportError:
        logger.error("需要安装 Pillow: pip install Pillow")
        return None
    
    try:
        # 尝试使用 comtypes (Windows) 或 Quartz (macOS) 转换
        # 这里提供一个简化版本，实际可能需要 LibreOffice 或其他工具
        
        logger.info(f"生成缩略图：{pptx_path}")
        
        # 注意：完整的 PPTX 转图片需要额外依赖
        # 这里提供一个占位实现
        
        output_path = Path(output_dir) / "thumbnails.jpg"
        
        # TODO: 实现完整的 PPTX 转图片逻辑
        # 可以使用以下方法之一:
        # 1. LibreOffice: soffice --headless --convert-to pdf
        # 2. comtypes (Windows)
        # 3. Quartz (macOS)
        
        logger.warning("缩略图生成功能需要额外依赖，跳过生成")
        logger.info("建议安装 LibreOffice: sudo apt-get install libreoffice")
        
        return None
        
    except Exception as e:
        logger.error(f"生成缩略图失败：{e}")
        return None


def create_thumbnail_grid(images: list, 
                          output_path: str,
                          cols: int = 5,
                          thumb_size: tuple = (200, 150)) -> str:
    """
    创建缩略图网格
    
    Args:
        images: PIL Image 对象列表
        output_path: 输出路径
        cols: 每列数量
        thumb_size: 缩略图尺寸
        
    Returns:
        输出文件路径
    """
    if not images:
        raise ValueError("没有图片")
    
    # 计算网格尺寸
    rows = (len(images) + cols - 1) // cols
    grid_width = cols * thumb_size[0]
    grid_height = rows * thumb_size[1]
    
    # 创建网格图像
    grid = Image.new('RGB', (grid_width, grid_height), color='white')
    
    # 粘贴缩略图
    for idx, img in enumerate(images):
        # 调整大小
        thumb = img.copy()
        thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        
        # 计算位置
        col = idx % cols
        row = idx // cols
        x = col * thumb_size[0] + (thumb_size[0] - thumb.width) // 2
        y = row * thumb_size[1] + (thumb_size[1] - thumb.height) // 2
        
        # 粘贴
        grid.paste(thumb, (x, y))
    
    # 保存
    grid.save(output_path, quality=85)
    logger.info(f"缩略图网格已保存：{output_path}")
    
    return output_path
