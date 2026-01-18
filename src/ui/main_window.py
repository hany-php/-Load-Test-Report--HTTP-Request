# -*- coding: utf-8 -*-
"""
Main Window Module - Arabic RTL Version
النافذة الرئيسية للتطبيق مع دعم اللغة العربية
"""

from arabic_ui import ArabicTexts as AR
from ab_resolver import verify_ab_installation
from ab_runner import ABRunnerWorker, ABTestConfig, ABTestResult
from ui.results_panel import ResultsPanel
from ui.input_panel import InputPanel
from ui.styles import DARK_THEME_RTL
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QMessageBox, QStatusBar,
    QDialog, QFormLayout, QSpinBox, QDialogButtonBox,
    QSplitter
)
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SettingsDialog(QDialog):
    """مربع حوار الإعدادات المتقدمة."""

    def __init__(self, max_requests: int, max_concurrency: int, parent=None):
        super().__init__(parent)

        self.setWindowTitle(AR.DIALOG_ADVANCED_TITLE)
        self.setMinimumWidth(350)
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.max_requests_input = QSpinBox()
        self.max_requests_input.setRange(100, 1000000)
        self.max_requests_input.setValue(max_requests)
        self.max_requests_input.setSingleStep(1000)
        self.max_requests_input.setLayoutDirection(Qt.LeftToRight)
        form_layout.addRow(AR.DIALOG_MAX_REQUESTS, self.max_requests_input)

        self.max_concurrency_input = QSpinBox()
        self.max_concurrency_input.setRange(1, 10000)
        self.max_concurrency_input.setValue(max_concurrency)
        self.max_concurrency_input.setSingleStep(50)
        self.max_concurrency_input.setLayoutDirection(Qt.LeftToRight)
        form_layout.addRow(AR.DIALOG_MAX_CONCURRENCY,
                           self.max_concurrency_input)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_values(self) -> tuple[int, int]:
        """الحصول على القيم المكوّنة."""
        return (
            self.max_requests_input.value(),
            self.max_concurrency_input.value()
        )


class MainWindow(QMainWindow):
    """
    النافذة الرئيسية للتطبيق.
    """

    def __init__(self):
        super().__init__()

        self._worker: ABRunnerWorker = None
        self._max_requests = 20000
        self._max_concurrency = 200

        self._setup_ui()
        self._setup_menu()
        self._connect_signals()
        self._check_ab_installation()

    def _setup_ui(self):
        """إعداد واجهة المستخدم."""
        self.setWindowTitle(AR.APP_TITLE)

        # فتح النافذة بملء الشاشة وتعطيل تغيير الحجم
        # السماح فقط بالإغلاق والتصغير لشريط المهام
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        self.showMaximized()

        # Set RTL layout direction
        self.setLayoutDirection(Qt.RightToLeft)

        # Apply dark theme with RTL support
        self.setStyleSheet(DARK_THEME_RTL)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(f"🚀 {AR.APP_TITLE}")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(AR.APP_SUBTITLE)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(
            "color: #a6adc8; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(subtitle_label)

        # Splitter for input and results
        splitter = QSplitter(Qt.Horizontal)
        splitter.setLayoutDirection(Qt.RightToLeft)

        # Input panel (on the right for RTL)
        self.input_panel = InputPanel()
        splitter.addWidget(self.input_panel)

        # Results panel (on the left for RTL)
        self.results_panel = ResultsPanel()
        splitter.addWidget(self.results_panel)

        # Set splitter proportions
        splitter.setSizes([350, 700])

        layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setLayoutDirection(Qt.RightToLeft)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(AR.STATUS_READY)

    def _setup_menu(self):
        """إعداد شريط القوائم."""
        menu_bar = self.menuBar()
        menu_bar.setLayoutDirection(Qt.RightToLeft)

        # File menu
        file_menu = menu_bar.addMenu(AR.MENU_FILE)

        export_json_action = QAction(AR.MENU_EXPORT_JSON, self)
        export_json_action.triggered.connect(
            self.results_panel._on_export_json_clicked
        )
        file_menu.addAction(export_json_action)

        export_txt_action = QAction(AR.MENU_EXPORT_TXT, self)
        export_txt_action.triggered.connect(
            self.results_panel._on_export_txt_clicked
        )
        file_menu.addAction(export_txt_action)

        file_menu.addSeparator()

        exit_action = QAction(AR.MENU_EXIT, self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Settings menu
        settings_menu = menu_bar.addMenu(AR.MENU_SETTINGS)

        advanced_action = QAction(AR.MENU_ADVANCED, self)
        advanced_action.triggered.connect(self._show_settings_dialog)
        settings_menu.addAction(advanced_action)

        # Help menu
        help_menu = menu_bar.addMenu(AR.MENU_HELP)

        about_action = QAction(AR.MENU_ABOUT, self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

        check_ab_action = QAction(AR.MENU_CHECK_AB, self)
        check_ab_action.triggered.connect(self._check_ab_installation)
        help_menu.addAction(check_ab_action)

    def _connect_signals(self):
        """ربط الإشارات بالفتحات."""
        self.input_panel.start_requested.connect(self._on_start_test)
        self.input_panel.stop_requested.connect(self._on_stop_test)

    def _check_ab_installation(self):
        """التحقق من تثبيت ApacheBench بشكل صحيح."""
        success, message = verify_ab_installation()

        if not success:
            QMessageBox.warning(
                self,
                AR.ERROR_AB_NOT_FOUND_TITLE,
                AR.ERROR_AB_NOT_FOUND_MSG.format(message=message)
            )
            self.status_bar.showMessage(AR.STATUS_AB_NOT_FOUND)
        else:
            self.status_bar.showMessage(
                AR.STATUS_AB_FOUND.format(path=message.split(': ')[-1]))

    @Slot()
    def _on_start_test(self):
        """بدء اختبار الحمل."""
        # Get configuration
        config_dict = self.input_panel.get_config()
        config = ABTestConfig(
            url=config_dict['url'],
            requests=config_dict['requests'],
            concurrency=config_dict['concurrency'],
            keep_alive=config_dict['keep_alive']
        )

        # Validate configuration
        is_valid, error = config.validate()
        if not is_valid:
            QMessageBox.warning(self, AR.ERROR_CONFIG_TITLE, error)
            return

        # Clear previous results
        self.results_panel.clear()

        # Update UI state
        self.input_panel.set_running(True)
        self.status_bar.showMessage(AR.STATUS_TESTING.format(url=config.url))

        # Create and start worker
        self._worker = ABRunnerWorker(config)
        self._worker.output_signal.connect(self._on_output_received)
        self._worker.completed_signal.connect(self._on_test_completed)
        self._worker.error_signal.connect(self._on_error)
        self._worker.start()

    @Slot()
    def _on_stop_test(self):
        """إيقاف الاختبار الجاري."""
        if self._worker:
            self._worker.cancel()
            self.status_bar.showMessage(AR.STATUS_STOPPING)

    @Slot(str)
    def _on_output_received(self, text: str):
        """معالجة المخرجات من الاختبار."""
        self.results_panel.append_output(text)

    @Slot(ABTestResult)
    def _on_test_completed(self, result: ABTestResult):
        """معالجة اكتمال الاختبار."""
        self.input_panel.set_running(False)

        if result.success:
            # Set complete results
            config_dict = self.input_panel.get_config()
            config = ABTestConfig(
                url=config_dict['url'],
                requests=config_dict['requests'],
                concurrency=config_dict['concurrency'],
                keep_alive=config_dict['keep_alive']
            )
            self.results_panel.set_results(result.stdout, config)
            self.status_bar.showMessage(AR.STATUS_SUCCESS)
        else:
            if result.error_message:
                self.status_bar.showMessage(
                    AR.STATUS_FAILED.format(error=result.error_message))
            else:
                self.status_bar.showMessage(AR.STATUS_CANCELLED)

        self._worker = None

    @Slot(str)
    def _on_error(self, error: str):
        """معالجة الخطأ من الاختبار."""
        QMessageBox.critical(self, AR.ERROR_CONFIG_TITLE, error)
        self.status_bar.showMessage(AR.STATUS_FAILED.format(error=error))

    def _show_settings_dialog(self):
        """عرض مربع حوار الإعدادات المتقدمة."""
        dialog = SettingsDialog(
            self._max_requests,
            self._max_concurrency,
            self
        )

        if dialog.exec() == QDialog.Accepted:
            self._max_requests, self._max_concurrency = dialog.get_values()
            self.input_panel.set_max_limits(
                self._max_requests,
                self._max_concurrency
            )

    def _show_about_dialog(self):
        """عرض مربع حوار عن التطبيق."""
        QMessageBox.about(
            self,
            AR.ABOUT_TITLE,
            AR.ABOUT_CONTENT
        )

    def closeEvent(self, event):
        """معالجة حدث إغلاق النافذة."""
        if self._worker and self._worker.isRunning():
            reply = QMessageBox.question(
                self,
                AR.CONFIRM_EXIT_TITLE,
                AR.CONFIRM_EXIT_MSG,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self._worker.cancel()
                self._worker.wait(5000)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
