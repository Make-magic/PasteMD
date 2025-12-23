"""Document domain - cross-platform document placement."""

import sys

# 导出基类
from .base import BaseDocumentPlacer
from .generator import DocumentGenerator

# 导出类型
from ...core.types import PlacementResult, PlacementMethod

# 平台特定实现(统一类名)
if sys.platform == "darwin":
    from .macos.word import WordPlacer
    from .macos.wps import WPSPlacer
elif sys.platform == "win32":
    from .win32.word import WordPlacer
    from .win32.wps import WPSPlacer
else:
    # 不支持的平台
    class WordPlacer(BaseDocumentPlacer):
        def place(self, *args, **kwargs):
            raise NotImplementedError(f"不支持的平台: {sys.platform}")
    
    class WPSPlacer(BaseDocumentPlacer):
        def place(self, *args, **kwargs):
            raise NotImplementedError(f"不支持的平台: {sys.platform}")

__all__ = [
    "BaseDocumentPlacer",
    "PlacementResult",
    "PlacementMethod",
    "WordPlacer",
    "WPSPlacer",
    "DocumentGenerator",
]
