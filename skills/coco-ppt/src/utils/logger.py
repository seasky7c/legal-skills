"""
日志工具 - 统一日志记录
"""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

console = Console()


class CocoLogger:
    """统一日志记录"""
    
    def __init__(self, name: str = "coco-ppt", level: str = "INFO"):
        """
        初始化日志器
        
        Args:
            name: 日志器名称
            level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 添加 Rich 处理器（美化输出）
        try:
            rich_handler = RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=False
            )
            self.logger.addHandler(rich_handler)
        except ImportError:
            # 如果没有 rich，使用标准处理器
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, msg: str):
        """调试日志"""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """信息日志"""
        self.logger.info(msg)
    
    def warning(self, msg: str):
        """警告日志"""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """错误日志"""
        self.logger.error(msg)
    
    def critical(self, msg: str):
        """严重错误日志"""
        self.logger.critical(msg)
    
    def success(self, msg: str):
        """成功日志"""
        console.print(f"[green]✓[/green] {msg}")
    
    def step(self, msg: str):
        """步骤日志"""
        console.print(f"[bold blue]➤[/bold blue] {msg}")


def get_logger(name: str = "coco-ppt", level: str = "INFO") -> CocoLogger:
    """
    获取日志器实例
    
    Args:
        name: 日志器名称
        level: 日志级别
        
    Returns:
        CocoLogger 实例
    """
    return CocoLogger(name, level)
