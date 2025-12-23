"""Excel spreadsheet workflow."""

from pastemd.app.workflows.excel.excel_base import ExcelBaseWorkflow
from pastemd.service.spreadsheet import ExcelPlacer


class ExcelWorkflow(ExcelBaseWorkflow):
    """Excel 表格工作流"""

    def __init__(self):
        super().__init__()
        self._placer = ExcelPlacer()

    @property
    def app_name(self) -> str:
        return "Excel"

    @property
    def placer(self):
        return self._placer

