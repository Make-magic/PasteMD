"""Word document workflow."""

from pastemd.app.workflows.word.word_base import WordBaseWorkflow
from pastemd.service.document import WordPlacer


class WordWorkflow(WordBaseWorkflow):
    """Word 文档工作流"""

    def __init__(self):
        super().__init__()
        self._placer = WordPlacer()

    @property
    def app_name(self) -> str:
        return "Word"

    @property
    def placer(self):
        return self._placer

