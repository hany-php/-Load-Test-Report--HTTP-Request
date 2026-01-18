"""
Qt Stylesheet for the Load Testing Application
Modern dark theme with professional appearance.
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 14px;
}

QLabel {
    color: #cdd6f4;
    padding: 2px;
}

QLabel#warning-label {
    background-color: #f38ba8;
    color: #1e1e2e;
    padding: 10px;
    border-radius: 6px;
    font-weight: bold;
}

QLabel#title-label {
    font-size: 24px;
    font-weight: bold;
    color: #89b4fa;
    padding: 10px;
}

QLineEdit {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 10px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QLineEdit:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QSpinBox {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 8px;
    color: #cdd6f4;
}

QSpinBox:focus {
    border-color: #89b4fa;
}

QSpinBox:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #45475a;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #89b4fa;
}

QCheckBox {
    spacing: 10px;
    color: #cdd6f4;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #45475a;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QCheckBox::indicator:hover {
    border-color: #89b4fa;
}

QPushButton {
    background-color: #45475a;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    color: #cdd6f4;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #585b70;
}

QPushButton:pressed {
    background-color: #313244;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
}

QPushButton#start-button {
    background-color: #a6e3a1;
    color: #1e1e2e;
}

QPushButton#start-button:hover {
    background-color: #94e2d5;
}

QPushButton#start-button:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#stop-button {
    background-color: #f38ba8;
    color: #1e1e2e;
}

QPushButton#stop-button:hover {
    background-color: #f5c2e7;
}

QPushButton#stop-button:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#export-button {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton#export-button:hover {
    background-color: #b4befe;
}

QTabWidget::pane {
    border: 2px solid #45475a;
    border-radius: 6px;
    background-color: #313244;
    margin-top: -1px;
}

QTabBar::tab {
    background-color: #45475a;
    color: #cdd6f4;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QTabBar::tab:hover:!selected {
    background-color: #585b70;
}

QTextEdit {
    background-color: #11111b;
    border: 2px solid #45475a;
    border-radius: 6px;
    padding: 10px;
    color: #a6e3a1;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

QTextEdit:focus {
    border-color: #89b4fa;
}

QScrollBar:vertical {
    background-color: #313244;
    width: 12px;
    margin: 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    min-height: 30px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #89b4fa;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #313244;
    height: 12px;
    margin: 0;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #45475a;
    min-width: 30px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #89b4fa;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QStatusBar {
    background-color: #181825;
    color: #6c7086;
    border-top: 1px solid #45475a;
    padding: 5px;
}

QMenuBar {
    background-color: #181825;
    color: #cdd6f4;
    border-bottom: 1px solid #45475a;
}

QMenuBar::item {
    padding: 8px 12px;
}

QMenuBar::item:selected {
    background-color: #45475a;
}

QMenu {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 5px;
}

QMenu::item {
    padding: 8px 30px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QGroupBox {
    border: 2px solid #45475a;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 5px;
    color: #89b4fa;
}

QMessageBox {
    background-color: #1e1e2e;
}

QMessageBox QLabel {
    color: #cdd6f4;
}

QDialog {
    background-color: #1e1e2e;
}

QFileDialog {
    background-color: #1e1e2e;
}
"""

# Color palette for reference
COLORS = {
    'base': '#1e1e2e',
    'surface0': '#313244',
    'surface1': '#45475a',
    'surface2': '#585b70',
    'overlay0': '#6c7086',
    'text': '#cdd6f4',
    'blue': '#89b4fa',
    'green': '#a6e3a1',
    'teal': '#94e2d5',
    'red': '#f38ba8',
    'pink': '#f5c2e7',
    'lavender': '#b4befe',
    'crust': '#11111b',
    'mantle': '#181825',
}

# RTL Arabic Dark Theme
DARK_THEME_RTL = """
QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Cairo', 'Tahoma', 'Arial', sans-serif;
    font-size: 14px;
}

QLabel {
    color: #cdd6f4;
    padding: 2px;
}

QLabel#warning-label {
    background-color: #f38ba8;
    color: #1e1e2e;
    padding: 12px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 13px;
}

QLabel#title-label {
    font-size: 28px;
    font-weight: bold;
    color: #89b4fa;
    padding: 15px;
}

QLineEdit {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 12px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QLineEdit:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QSpinBox {
    background-color: #313244;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 10px;
    color: #cdd6f4;
}

QSpinBox:focus {
    border-color: #89b4fa;
}

QSpinBox:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #45475a;
    border: none;
    width: 24px;
    border-radius: 4px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #89b4fa;
}

QCheckBox {
    spacing: 12px;
    color: #cdd6f4;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #45475a;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QCheckBox::indicator:hover {
    border-color: #89b4fa;
}

QPushButton {
    background-color: #45475a;
    border: none;
    border-radius: 8px;
    padding: 14px 28px;
    color: #cdd6f4;
    font-weight: bold;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #585b70;
}

QPushButton:pressed {
    background-color: #313244;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
}

QPushButton#start-button {
    background-color: #a6e3a1;
    color: #1e1e2e;
    font-size: 15px;
}

QPushButton#start-button:hover {
    background-color: #94e2d5;
}

QPushButton#start-button:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#stop-button {
    background-color: #f38ba8;
    color: #1e1e2e;
}

QPushButton#stop-button:hover {
    background-color: #f5c2e7;
}

QPushButton#stop-button:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#export-button {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QPushButton#export-button:hover {
    background-color: #b4befe;
}

QTabWidget::pane {
    border: 2px solid #45475a;
    border-radius: 8px;
    background-color: #313244;
    margin-top: -1px;
}

QTabBar::tab {
    background-color: #45475a;
    color: #cdd6f4;
    padding: 12px 24px;
    margin-left: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QTabBar::tab:hover:!selected {
    background-color: #585b70;
}

QTextEdit {
    background-color: #11111b;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 12px;
    color: #a6e3a1;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

QTextEdit:focus {
    border-color: #89b4fa;
}

QScrollBar:vertical {
    background-color: #313244;
    width: 14px;
    margin: 0;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    min-height: 30px;
    border-radius: 7px;
}

QScrollBar::handle:vertical:hover {
    background-color: #89b4fa;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #313244;
    height: 14px;
    margin: 0;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background-color: #45475a;
    min-width: 30px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #89b4fa;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QStatusBar {
    background-color: #181825;
    color: #a6adc8;
    border-top: 1px solid #45475a;
    padding: 8px;
    font-size: 13px;
}

QMenuBar {
    background-color: #181825;
    color: #cdd6f4;
    border-bottom: 1px solid #45475a;
    padding: 2px;
}

QMenuBar::item {
    padding: 10px 16px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #45475a;
}

QMenu {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 8px;
}

QMenu::item {
    padding: 10px 35px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: #89b4fa;
    color: #1e1e2e;
}

QGroupBox {
    border: 2px solid #45475a;
    border-radius: 10px;
    margin-top: 15px;
    padding: 20px;
    padding-top: 25px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top right;
    right: 15px;
    padding: 5px 15px;
    background-color: #89b4fa;
    color: #1e1e2e;
    border-radius: 6px;
}

QMessageBox {
    background-color: #1e1e2e;
}

QMessageBox QLabel {
    color: #cdd6f4;
    font-size: 14px;
}

QMessageBox QPushButton {
    min-width: 90px;
    padding: 10px 20px;
}

QDialog {
    background-color: #1e1e2e;
}

QFileDialog {
    background-color: #1e1e2e;
}

QSplitter::handle {
    background-color: #45475a;
    width: 3px;
    border-radius: 1px;
}

QSplitter::handle:hover {
    background-color: #89b4fa;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
}
"""
