"""macOS Word document placer."""

import subprocess
import os
from ..base import BaseDocumentPlacer
from ....core.types import PlacementResult
from ....utils.logging import log
from ....i18n import t
from ....config.paths import get_user_data_dir


class WordPlacer(BaseDocumentPlacer):
    """macOS Word 内容落地器"""
    
    def __init__(self):
        """初始化并创建固定的临时文件路径"""
        super().__init__()
        # 使用固定的临时文件路径，避免每次都需要授权
        temp_dir = os.path.join(get_user_data_dir(), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        self._fixed_temp_path = os.path.join(temp_dir, "pastemd_word_insert.docx")
        log(f"Word 临时文件路径: {self._fixed_temp_path}")
    
    def place(self, docx_bytes: bytes, config: dict) -> PlacementResult:
        """通过 AppleScript 插入,失败不降级"""
        try:
            # 使用固定路径写入临时文件（覆盖之前的）
            with open(self._fixed_temp_path, 'wb') as f:
                f.write(docx_bytes)
            
            # 默认移动光标到末尾
            move_cursor_to_end = config.get("move_cursor_to_end", True)
            success = self._applescript_insert(self._fixed_temp_path, move_cursor_to_end)
            
            if success:
                return PlacementResult(success=True, method="applescript")
            else:
                raise Exception(t("placer.macos_word.applescript_failed"))
        
        except Exception as e:
            log(f"Word AppleScript 插入失败: {e}")
            return PlacementResult(
                success=False,
                method="applescript",
                error=t("placer.macos_word.insert_failed", error=str(e))
            )
    
    def _applescript_insert(self, docx_path: str, move_cursor_to_end: bool = True) -> bool:
        """
        使用 AppleScript 在当前光标/选中位置插入文档
        """
        # todo move_cursor_to_end未实现
        # 将路径转换为 POSIX 格式
        posix_path = os.path.abspath(docx_path)
        
        # 将 Python bool 转换为 AppleScript bool 字符串
        as_move_cursor = "true"

        script = f'''
        tell application "Microsoft Word"
            activate
            if (count of documents) is 0 then
                make new document
            end if
            
            -- 修复点：不要 tell selection，而是在 Application 上下文操作
            
            -- 1. 获取当前选区的位置对象 (text object)
            set targetRange to text object of selection
            
            -- 2. 在该位置插入文件 (insert file 是 app 的命令，不是 selection 的)
            -- 注意：Word AppleScript 这里的 file name 需要完整路径
            insert file at targetRange file name "{posix_path}"
            
            -- 3. 处理光标移动
            if {as_move_cursor} then
                -- 插入后，selection 通常会选中刚插入的内容
                -- 我们再次获取当前的 selection 并将其折叠到末尾
                set currentRange to text object of selection
                collapse range currentRange direction collapse end
                
                -- 显式选中折叠后的点，确保光标视觉上跳过去
                select currentRange
            end if
        end tell
        '''
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            log(f"AppleScript 插入成功: {docx_path} ")
            return True
        except subprocess.CalledProcessError as e:
            # 捕获更详细的错误输出
            error_msg = e.stderr.strip()
            log(f"AppleScript 执行失败: {error_msg}")
            
            # 特殊处理：如果 Word 弹窗导致超时或失败（如宏警告），给提示
            if "file not found" in error_msg.lower():
                raise Exception(f"Word 找不到文件: {posix_path}")
            
            raise Exception(f"AppleScript 错误: {error_msg}")
        except subprocess.TimeoutExpired:
            log("AppleScript 执行超时")
            raise Exception(t("placer.macos_word.timeout"))