"""Workflow router - main entry point."""

from ...utils.detector import detect_active_app
from ...utils.logging import log
from ...service.notification.manager import NotificationManager
from ...i18n import t

from .word import WordWorkflow, WPSWorkflow
from .excel import ExcelWorkflow, WPSExcelWorkflow
from .fallback import FallbackWorkflow


class WorkflowRouter:
    """工作流路由器（单例）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        
        # 预创建所有工作流（复用实例，避免重复初始化）
        self.workflows = {
            "word": WordWorkflow(),
            "wps": WPSWorkflow(),
            "excel": ExcelWorkflow(),
            "wps_excel": WPSExcelWorkflow(),
            "": FallbackWorkflow(),  # 空字符串表示无应用
        }
        
        self.notification_manager = NotificationManager()
        self._initialized = True
        log("WorkflowRouter initialized")
    
    def route(self) -> None:
        """主入口：检测应用 → 路由到工作流"""
        try:
            # 检测目标应用
            target_app = detect_active_app()
            log(f"Detected target app: {target_app}")
            
            # 路由到对应工作流
            workflow = self.workflows.get(target_app, self.workflows[""])
            workflow.execute()
        
        except Exception as e:
            log(f"Router failed: {e}")
            import traceback
            traceback.print_exc()
            self.notification_manager.notify("PasteMD", t("workflow.generic.failure"), ok=False)


# 全局单例
router = WorkflowRouter()


def execute_paste_workflow():
    """热键入口函数"""
    router.route()
