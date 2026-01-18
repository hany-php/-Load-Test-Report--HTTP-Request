# -*- coding: utf-8 -*-
"""
تنسيقات التطبيق - Modern Dark Theme
Application Styles
"""

# الألوان الأساسية
COLORS = {
    'bg_primary': '#1a1a2e',
    'bg_secondary': '#16213e',
    'bg_tertiary': '#0f3460',
    'accent': '#e94560',
    'accent_hover': '#ff6b6b',
    'success': '#00d9a5',
    'warning': '#ffc107',
    'error': '#ff4757',
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'border': '#2d3748',
}

# التنسيق الرئيسي للتطبيق
MAIN_STYLE = f"""
QMainWindow {{
    background-color: {COLORS['bg_primary']};
}}

QWidget {{
    font-family: 'Segoe UI', 'Cairo', 'Tahoma', sans-serif;
    font-size: 14px;
    color: {COLORS['text_primary']};
}}

/* العناوين */
QLabel#titleLabel {{
    font-size: 28px;
    font-weight: bold;
    color: {COLORS['accent']};
    padding: 10px;
}}

QLabel#subtitleLabel {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
    padding-bottom: 20px;
}}

/* قسم الإعدادات */
QGroupBox {{
    background-color: {COLORS['bg_secondary']};
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 20px;
    padding: 20px;
    padding-top: 35px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 8px 20px;
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
    border-radius: 8px;
    font-weight: bold;
}}

/* حقول الإدخال */
QLineEdit {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px 16px;
    color: {COLORS['text_primary']};
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

QLineEdit:hover {{
    border-color: {COLORS['accent_hover']};
}}

/* حقول الأرقام */
QSpinBox {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 16px;
    color: {COLORS['text_primary']};
    font-size: 14px;
}}

QSpinBox:focus {{
    border-color: {COLORS['accent']};
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {COLORS['accent']};
    border: none;
    width: 24px;
    border-radius: 4px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background-color: {COLORS['accent_hover']};
}}

/* مربع الاختيار */
QCheckBox {{
    spacing: 10px;
    color: {COLORS['text_primary']};
}}

QCheckBox::indicator {{
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid {COLORS['border']};
    background-color: {COLORS['bg_tertiary']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['accent_hover']};
}}

/* الأزرار */
QPushButton {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-radius: 10px;
    padding: 12px 24px;
    color: {COLORS['text_primary']};
    font-weight: bold;
    font-size: 14px;
    min-width: 120px;
}}

QPushButton:hover {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

/* زر البدء */
QPushButton#startButton {{
    background-color: {COLORS['success']};
    border-color: {COLORS['success']};
    color: #000000;
}}

QPushButton#startButton:hover {{
    background-color: #00f5b8;
}}

/* زر الإيقاف */
QPushButton#stopButton {{
    background-color: {COLORS['error']};
    border-color: {COLORS['error']};
}}

QPushButton#stopButton:hover {{
    background-color: #ff6b7a;
}}

/* زر المسح */
QPushButton#clearButton {{
    background-color: {COLORS['warning']};
    border-color: {COLORS['warning']};
    color: #000000;
}}

QPushButton#clearButton:hover {{
    background-color: #ffd43b;
}}

/* التبويبات */
QTabWidget::pane {{
    background-color: {COLORS['bg_secondary']};
    border: 2px solid {COLORS['border']};
    border-radius: 12px;
    padding: 10px;
}}

QTabBar::tab {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 12px 24px;
    margin-right: 4px;
    color: {COLORS['text_secondary']};
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['border']};
}}

/* منطقة النص */
QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 12px;
    color: {COLORS['text_primary']};
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}}

/* شريط الحالة */
QStatusBar {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
    padding: 8px;
}}

/* شريط التقدم */
QProgressBar {{
    background-color: {COLORS['bg_tertiary']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    height: 20px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 6px;
}}

/* التمرير */
QScrollBar:vertical {{
    background-color: {COLORS['bg_tertiary']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* الرسائل */
QMessageBox {{
    background-color: {COLORS['bg_primary']};
}}

QMessageBox QLabel {{
    color: {COLORS['text_primary']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}
"""
