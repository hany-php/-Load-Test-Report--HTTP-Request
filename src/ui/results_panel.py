# -*- coding: utf-8 -*-
"""
Results Panel Widget - Arabic RTL Version
لوحة النتائج مع دعم اللغة العربية والتخطيط من اليمين لليسار
"""

from arabic_ui import ArabicTexts as AR
from parser import ABMetrics, ABOutputParser, format_summary_arabic
from exporter import export_to_json, export_to_txt, export_to_pdf, get_default_filename
from ab_runner import ABTestConfig
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTextEdit, QPushButton, QApplication, QFileDialog,
    QMessageBox
)
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ResultsPanel(QWidget):
    """
    لوحة النتائج مع تبويبات للمخرجات الخام والملخص.
    تتضمن أزرار للنسخ والتصدير.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._raw_output = ""
        self._metrics: ABMetrics = None
        self._config: ABTestConfig = None
        self._parser = ABOutputParser()

        self._setup_ui()

    def _setup_ui(self):
        """إعداد واجهة المستخدم."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setLayoutDirection(Qt.RightToLeft)

        # Raw output tab
        self.raw_output_text = QTextEdit()
        self.raw_output_text.setReadOnly(True)
        self.raw_output_text.setFont(QFont("Consolas", 11))
        self.raw_output_text.setLayoutDirection(
            Qt.LeftToRight)  # Output is LTR
        self.raw_output_text.setPlaceholderText(AR.PLACEHOLDER_RAW)
        self.tab_widget.addTab(self.raw_output_text, AR.TAB_RAW_OUTPUT)

        # Summary tab
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setFont(QFont("Consolas", 11))
        self.summary_text.setPlaceholderText(AR.PLACEHOLDER_SUMMARY)
        self.tab_widget.addTab(self.summary_text, AR.TAB_SUMMARY)

        layout.addWidget(self.tab_widget)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setDirection(QHBoxLayout.RightToLeft)

        self.copy_button = QPushButton(AR.BTN_COPY)
        self.copy_button.clicked.connect(self._on_copy_clicked)
        self.copy_button.setEnabled(False)
        button_layout.addWidget(self.copy_button)

        self.export_json_button = QPushButton(AR.BTN_EXPORT_JSON)
        self.export_json_button.setObjectName("export-button")
        self.export_json_button.clicked.connect(self._on_export_json_clicked)
        self.export_json_button.setEnabled(False)
        button_layout.addWidget(self.export_json_button)

        self.export_txt_button = QPushButton(AR.BTN_EXPORT_TXT)
        self.export_txt_button.setObjectName("export-button")
        self.export_txt_button.clicked.connect(self._on_export_txt_clicked)
        self.export_txt_button.setEnabled(False)
        button_layout.addWidget(self.export_txt_button)

        self.export_pdf_button = QPushButton(AR.BTN_EXPORT_PDF)
        self.export_pdf_button.setObjectName("export-button")
        self.export_pdf_button.clicked.connect(self._on_export_pdf_clicked)
        self.export_pdf_button.setEnabled(False)
        button_layout.addWidget(self.export_pdf_button)

        self.clear_button = QPushButton(AR.BTN_CLEAR)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

    def append_output(self, text: str):
        """
        إضافة نص إلى المخرجات الخام.

        Args:
            text: النص المراد إضافته
        """
        from PySide6.QtGui import QTextCursor
        self._raw_output += text
        self.raw_output_text.moveCursor(QTextCursor.MoveOperation.End)
        self.raw_output_text.insertPlainText(text)
        self.raw_output_text.moveCursor(QTextCursor.MoveOperation.End)

    def set_results(self, output: str, config: ABTestConfig):
        """
        تعيين نتائج الاختبار الكاملة.

        Args:
            output: المخرجات الخام الكاملة
            config: تكوين الاختبار المستخدم
        """
        self._raw_output = output
        self._config = config

        # Parse the output
        self._metrics = self._parser.parse(output)

        # Update summary tab with Arabic formatting
        try:
            summary = format_summary_arabic(self._metrics)
        except Exception:
            # Fallback to English if Arabic formatter fails
            from parser import format_summary
            summary = format_summary(self._metrics)

        self.summary_text.setText(summary)

        # Enable export buttons
        self.copy_button.setEnabled(True)
        self.export_json_button.setEnabled(True)
        self.export_txt_button.setEnabled(True)
        self.export_pdf_button.setEnabled(True)

        # Switch to summary tab
        self.tab_widget.setCurrentIndex(1)

    def clear(self):
        """مسح جميع النتائج."""
        self._raw_output = ""
        self._metrics = None
        self._config = None

        self.raw_output_text.clear()
        self.summary_text.clear()

        self.copy_button.setEnabled(False)
        self.export_json_button.setEnabled(False)
        self.export_txt_button.setEnabled(False)
        self.export_pdf_button.setEnabled(False)

    def _on_copy_clicked(self):
        """معالجة النقر على زر النسخ."""
        current_tab = self.tab_widget.currentIndex()

        if current_tab == 0:
            # Copy raw output
            text = self._raw_output
        else:
            # Copy summary
            text = self.summary_text.toPlainText()

        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

            # Show feedback
            self.copy_button.setText(AR.BTN_COPIED)
            QTimer.singleShot(
                1500, lambda: self.copy_button.setText(AR.BTN_COPY))

    def _on_export_json_clicked(self):
        """معالجة النقر على زر تصدير JSON."""
        if not self._metrics or not self._config:
            return

        default_name = get_default_filename(self._config, "json")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            AR.MENU_EXPORT_JSON,
            default_name,
            "JSON Files (*.json)"
        )

        if filepath:
            try:
                export_to_json(self._metrics, self._config, filepath)
                QMessageBox.information(
                    self,
                    AR.SUCCESS_EXPORT_TITLE,
                    AR.SUCCESS_EXPORT_MSG.format(filepath=filepath)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    AR.ERROR_EXPORT_TITLE,
                    AR.ERROR_EXPORT_MSG.format(error=str(e))
                )

    def _on_export_txt_clicked(self):
        """معالجة النقر على زر تصدير TXT."""
        if not self._metrics or not self._config:
            return

        default_name = get_default_filename(self._config, "txt")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            AR.MENU_EXPORT_TXT,
            default_name,
            "Text Files (*.txt)"
        )

        if filepath:
            try:
                export_to_txt(self._metrics, self._config, filepath)
                QMessageBox.information(
                    self,
                    AR.SUCCESS_EXPORT_TITLE,
                    AR.SUCCESS_EXPORT_MSG.format(filepath=filepath)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    AR.ERROR_EXPORT_TITLE,
                    AR.ERROR_EXPORT_MSG.format(error=str(e))
                )

    def _on_clear_clicked(self):
        """معالجة النقر على زر المسح."""
        self.clear()

    def _on_export_pdf_clicked(self):
        """معالجة النقر على زر تصدير PDF."""
        if not self._metrics or not self._config:
            return

        default_name = get_default_filename(self._config, "pdf")

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            AR.MENU_EXPORT_PDF,
            default_name,
            "PDF Files (*.pdf)"
        )

        if filepath:
            try:
                export_to_pdf(self._metrics, self._config, filepath)
                QMessageBox.information(
                    self,
                    AR.SUCCESS_EXPORT_TITLE,
                    AR.SUCCESS_EXPORT_MSG.format(filepath=filepath)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    AR.ERROR_EXPORT_TITLE,
                    AR.ERROR_EXPORT_MSG.format(error=str(e))
                )
