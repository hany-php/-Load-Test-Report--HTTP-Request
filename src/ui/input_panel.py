# -*- coding: utf-8 -*-
"""
Input Panel Widget - Arabic RTL Version
لوحة الإدخال مع دعم اللغة العربية والتخطيط من اليمين لليسار
"""

from arabic_ui import ArabicTexts as AR
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton,
    QGroupBox, QMessageBox
)
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class InputPanel(QWidget):
    """
    لوحة إدخال إعدادات الاختبار.
    توفر حقول إدخال للرابط، عدد الطلبات، التزامن، وخيار Keep-Alive.
    """

    # Signals
    start_requested = Signal()
    stop_requested = Signal()

    # Default limits
    DEFAULT_MAX_REQUESTS = 20000
    DEFAULT_MAX_CONCURRENCY = 200

    def __init__(self, parent=None):
        super().__init__(parent)

        self._max_requests = self.DEFAULT_MAX_REQUESTS
        self._max_concurrency = self.DEFAULT_MAX_CONCURRENCY
        self._is_running = False

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """إعداد واجهة المستخدم."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Warning label
        warning_label = QLabel(AR.WARNING_MESSAGE)
        warning_label.setObjectName("warning-label")
        warning_label.setWordWrap(True)
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)

        # Input group
        input_group = QGroupBox(AR.INPUT_SECTION)
        input_group.setLayoutDirection(Qt.RightToLeft)
        input_layout = QFormLayout(input_group)
        input_layout.setSpacing(12)
        input_layout.setLabelAlignment(Qt.AlignRight)

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(AR.URL_PLACEHOLDER)
        self.url_input.setMinimumWidth(300)
        self.url_input.setLayoutDirection(Qt.LeftToRight)  # URLs are LTR
        input_layout.addRow(AR.URL_LABEL, self.url_input)

        # Requests input
        self.requests_input = QSpinBox()
        self.requests_input.setRange(1, self._max_requests)
        self.requests_input.setValue(1000)
        self.requests_input.setSingleStep(100)
        self.requests_input.setSuffix(" طلب")
        self.requests_input.setLayoutDirection(Qt.LeftToRight)
        input_layout.addRow(AR.TOTAL_REQUESTS_LABEL, self.requests_input)

        # Concurrency input
        self.concurrency_input = QSpinBox()
        self.concurrency_input.setRange(1, self._max_concurrency)
        self.concurrency_input.setValue(10)
        self.concurrency_input.setSingleStep(5)
        self.concurrency_input.setSuffix(" متزامن")
        self.concurrency_input.setLayoutDirection(Qt.LeftToRight)
        input_layout.addRow(AR.CONCURRENT_REQUESTS_LABEL,
                            self.concurrency_input)

        # Keep-alive checkbox
        self.keep_alive_checkbox = QCheckBox(AR.KEEP_ALIVE_LABEL)
        self.keep_alive_checkbox.setChecked(True)
        self.keep_alive_checkbox.setToolTip(AR.KEEP_ALIVE_TOOLTIP)
        input_layout.addRow("", self.keep_alive_checkbox)

        layout.addWidget(input_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setDirection(QHBoxLayout.RightToLeft)

        self.start_button = QPushButton(AR.BTN_START)
        self.start_button.setObjectName("start-button")
        self.start_button.setMinimumHeight(45)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton(AR.BTN_STOP)
        self.stop_button.setObjectName("stop-button")
        self.stop_button.setMinimumHeight(45)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        # Limits info
        limits_label = QLabel(
            AR.LIMITS_FORMAT.format(
                requests=self._max_requests,
                concurrency=self._max_concurrency
            )
        )
        limits_label.setStyleSheet("color: #6c7086; font-size: 12px;")
        limits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(limits_label)
        self._limits_label = limits_label

    def _connect_signals(self):
        """ربط الإشارات الداخلية."""
        self.start_button.clicked.connect(self._on_start_clicked)
        self.stop_button.clicked.connect(self._on_stop_clicked)
        self.url_input.textChanged.connect(self._validate_inputs)
        self.requests_input.valueChanged.connect(self._validate_inputs)
        self.concurrency_input.valueChanged.connect(self._validate_inputs)

    def _validate_inputs(self):
        """التحقق من جميع المدخلات وتحديث حالة الزر."""
        url = self.url_input.text().strip()
        requests = self.requests_input.value()
        concurrency = self.concurrency_input.value()

        is_valid = True

        # Check URL
        if not url:
            is_valid = False
        elif not url.startswith(('http://', 'https://')):
            is_valid = False

        # Check concurrency <= requests
        if concurrency > requests:
            is_valid = False
            self.concurrency_input.setStyleSheet("border-color: #f38ba8;")
        else:
            self.concurrency_input.setStyleSheet("")

        self.start_button.setEnabled(is_valid and not self._is_running)

    def _on_start_clicked(self):
        """معالجة النقر على زر البدء."""
        url = self.url_input.text().strip()
        requests = self.requests_input.value()
        concurrency = self.concurrency_input.value()

        if not url.startswith(('http://', 'https://')):
            QMessageBox.warning(
                self,
                AR.ERROR_INVALID_URL_TITLE,
                AR.ERROR_INVALID_URL
            )
            return

        if concurrency > requests:
            QMessageBox.warning(
                self,
                AR.ERROR_CONCURRENCY_TITLE,
                AR.ERROR_CONCURRENCY
            )
            return

        self.start_requested.emit()

    def _on_stop_clicked(self):
        """معالجة النقر على زر الإيقاف."""
        self.stop_requested.emit()

    def get_config(self) -> dict:
        """
        الحصول على تكوين الاختبار الحالي.

        Returns:
            dict: التكوين مع url, requests, concurrency, keep_alive
        """
        return {
            'url': self.url_input.text().strip(),
            'requests': self.requests_input.value(),
            'concurrency': self.concurrency_input.value(),
            'keep_alive': self.keep_alive_checkbox.isChecked(),
        }

    def set_running(self, running: bool):
        """
        تعيين حالة التشغيل للوحة.

        Args:
            running: True إذا كان الاختبار قيد التشغيل
        """
        self._is_running = running

        # Update button states
        self.start_button.setEnabled(not running)
        self.stop_button.setEnabled(running)

        # Disable inputs while running
        self.url_input.setEnabled(not running)
        self.requests_input.setEnabled(not running)
        self.concurrency_input.setEnabled(not running)
        self.keep_alive_checkbox.setEnabled(not running)

        # Update start button text
        if running:
            self.start_button.setText(AR.BTN_RUNNING)
        else:
            self.start_button.setText(AR.BTN_START)

    def set_max_limits(self, max_requests: int, max_concurrency: int):
        """
        تعيين الحدود القصوى للطلبات والتزامن.

        Args:
            max_requests: أقصى عدد للطلبات
            max_concurrency: أقصى مستوى تزامن
        """
        self._max_requests = max_requests
        self._max_concurrency = max_concurrency

        self.requests_input.setMaximum(max_requests)
        self.concurrency_input.setMaximum(max_concurrency)

        self._limits_label.setText(
            AR.LIMITS_FORMAT.format(
                requests=max_requests,
                concurrency=max_concurrency
            )
        )
