"""Base classes for document placement."""

from abc import ABC, abstractmethod
from ...core.types import PlacementResult


class BaseDocumentPlacer(ABC):
    """文档内容落地器基类"""
    
    @abstractmethod
    def place(self, docx_bytes: bytes, config: dict) -> PlacementResult:
        """
        将 DOCX 内容落地到目标应用
        
        Args:
            docx_bytes: DOCX 文件字节流
            config: 配置字典
            
        Returns:
            PlacementResult: 落地结果
            
        Note:
            ❌ 不做优雅降级,失败即返回错误
            ✅ 由 Workflow 决定如何处理失败(通知用户/记录日志)
        """
        pass
