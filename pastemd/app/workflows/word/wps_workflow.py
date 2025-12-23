"""WPS document workflow."""

from pastemd.app.workflows.word.word_base import WordBaseWorkflow
from pastemd.service.document import WPSPlacer


class WPSWorkflow(WordBaseWorkflow):
    """WPS 文档工作流"""

    def __init__(self):
        super().__init__()
        self._placer = WPSPlacer()

    @property
    def app_name(self) -> str:
        return "WPS 文字"

    @property
    def placer(self):
        return self._placer

