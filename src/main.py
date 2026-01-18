# -*- coding: utf-8 -*-
"""
أداة اختبار الحمل - Load Testing App
تطبيق واجهة رسومية لـ ApacheBench مع دعم اللغة العربية
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
import sys
import os

# Add src directory to path
src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)


def main():
    """نقطة الدخول الرئيسية للتطبيق."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("أداة اختبار الحمل")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("LoadTester")

    # Set RTL layout direction for the entire application
    app.setLayoutDirection(Qt.RightToLeft)

    # Set default font with Arabic support
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)

    # Set application icon if available
    icon_path = os.path.join(
        os.path.dirname(src_dir),
        'assets',
        'icon.png'
    )
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
