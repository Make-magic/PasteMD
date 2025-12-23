"""Windows WPS document placer."""

from ..base import BaseDocumentPlacer
from ....utils.win32.memfile import EphemeralFile
from ....core.errors import InsertError
from ....core.types import PlacementResult
from ....utils.logging import log
from ....i18n import t

# 复用现有 COM 插入器
from .wps_inserter import WPSInserter


class WPSPlacer(BaseDocumentPlacer):
    """Windows WPS 内容落地器"""
    
    def __init__(self):
        self.com_inserter = WPSInserter()
    
    def place(self, docx_bytes: bytes, config: dict) -> PlacementResult:
        """通过 COM 插入,失败不降级"""
        try:
            with EphemeralFile(suffix=".docx") as eph:
                eph.write_bytes(docx_bytes)
                success = self.com_inserter.insert(
                    eph.path,
                    move_cursor_to_end=config.get("move_cursor_to_end", True)
                )
            
            if success:
                return PlacementResult(success=True, method="com")
            else:
                raise InsertError("COM 插入返回 False")
        
        except Exception as e:
            log(f"WPS COM 插入失败: {e}")
            return PlacementResult(
                success=False,
                method="com",
                error=t("placer.win32_wps.insert_failed", error=str(e))
            )
