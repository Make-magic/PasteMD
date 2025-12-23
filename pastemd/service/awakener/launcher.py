"""Application awakener - awakens applications by creating and opening files."""

import os
import subprocess
from typing import Literal

from ...utils.logging import log
from ...utils.system_detect import is_windows, is_macos


AppType = Literal["word", "wps", "excel", "wps_excel"]


class AppLauncher:
    """应用唤醒器 - 通过创建文件并用默认应用打开来唤醒应用"""
    
    @staticmethod
    def _open_file_with_default_app(file_path: str) -> bool:
        """
        使用默认应用打开文件（跨平台）
        
        Args:
            file_path: 文件的完整路径
            
        Returns:
            True 如果成功打开
        """
        try:
            if is_windows():
                # Windows: 使用 os.startfile 或 start 命令
                try:
                    os.startfile(file_path)
                    log(f"Successfully opened file with os.startfile: {file_path}")
                    return True
                except Exception as e:
                    log(f"os.startfile failed, trying cmd start: {e}")
                    subprocess.Popen(
                        ['cmd', '/c', 'start', '', file_path],
                        shell=False,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    log(f"Successfully opened file with cmd start: {file_path}")
                    return True
            elif is_macos():
                # macOS: 使用 open 命令
                subprocess.Popen(['open', file_path])
                log(f"Successfully opened file with open command: {file_path}")
                return True
            else:
                # Linux: 使用 xdg-open 命令
                subprocess.Popen(['xdg-open', file_path])
                log(f"Successfully opened file with xdg-open: {file_path}")
                return True
        except Exception as e:
            log(f"Failed to open file with default application: {e}")
            return False
    
    @staticmethod
    def awaken_and_open_document(docx_path: str) -> bool:
        """
        唤醒文档应用（Word/WPS）并打开指定的 DOCX 文件（前台显示）
        
        Args:
            docx_path: DOCX 文件的完整路径（文件应已存在且包含内容）
            
        Returns:
            True 如果成功打开
        """
        if not os.path.exists(docx_path):
            log(f"Document file not found: {docx_path}")
            return False
        
        return AppLauncher._open_file_with_default_app(docx_path)
    
    @staticmethod
    def awaken_and_open_spreadsheet(xlsx_path: str) -> bool:
        """
        唤醒表格应用（Excel/WPS）并打开指定的 XLSX 文件（前台显示）
        
        Args:
            xlsx_path: XLSX 文件的完整路径（文件应已存在且包含内容）
            
        Returns:
            True 如果成功打开
        """
        if not os.path.exists(xlsx_path):
            log(f"Spreadsheet file not found: {xlsx_path}")
            return False
        
        return AppLauncher._open_file_with_default_app(xlsx_path)


