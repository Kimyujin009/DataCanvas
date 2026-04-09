from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .plot import PlotCanvas


def build_main_ui(window) -> QWidget:
    root = QWidget()
    layout = QHBoxLayout(root)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(18)

    left_panel = QFrame()
    left_panel.setObjectName("leftPanel")
    left_layout = QVBoxLayout(left_panel)
    left_layout.setContentsMargins(22, 22, 22, 22)
    left_layout.setSpacing(12)

    title = QLabel("DataCanvas")
    title.setObjectName("title")
    subtitle = QLabel("Load data, choose columns, and inspect the trend quickly.")
    subtitle.setWordWrap(True)
    subtitle.setObjectName("muted")

    upload_card = QFrame()
    upload_card.setObjectName("softCard")
    upload_layout = QVBoxLayout(upload_card)
    upload_layout.setContentsMargins(18, 18, 18, 18)
    upload_layout.setSpacing(14)

    upload_title = QLabel("Data Source")
    upload_title.setObjectName("section")
    upload_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    upload_hint = QLabel("Use the sample CSV or open your own file.")
    upload_hint.setWordWrap(True)
    upload_hint.setObjectName("muted")
    upload_hint.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    window.open_button = QPushButton("Open CSV")
    window.open_button.setMinimumHeight(42)
    window.open_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    window.sample_button = QToolButton()
    window.sample_button.setText("Load Sample CSV")
    window.sample_button.setProperty("secondary", True)
    window.sample_button.setMinimumHeight(42)
    window.sample_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    window.sample_button.setPopupMode(QToolButton.InstantPopup)
    window.sample_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
    window.file_label = QLabel("Current file: none")
    window.file_label.setObjectName("subtle")
    window.file_label.setWordWrap(True)
    window.file_label.setContentsMargins(0, 0, 0, 0)
    window.file_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    open_button_row = QFrame()
    open_button_row.setObjectName("flatRow")
    open_button_layout = QVBoxLayout(open_button_row)
    open_button_layout.setContentsMargins(0, 2, 0, 2)
    open_button_layout.setSpacing(0)
    open_button_layout.addWidget(window.open_button)

    sample_button_row = QFrame()
    sample_button_row.setObjectName("flatRow")
    sample_button_layout = QVBoxLayout(sample_button_row)
    sample_button_layout.setContentsMargins(0, 2, 0, 2)
    sample_button_layout.setSpacing(0)
    sample_button_layout.addWidget(window.sample_button)

    file_card = QFrame()
    file_card.setObjectName("fileBadge")
    file_layout = QVBoxLayout(file_card)
    file_layout.setContentsMargins(12, 10, 12, 10)
    file_layout.setSpacing(0)
    file_layout.addWidget(window.file_label)

    upload_layout.addWidget(upload_title)
    upload_layout.addWidget(upload_hint)
    upload_layout.addWidget(open_button_row)
    upload_layout.addWidget(sample_button_row)
    upload_layout.addWidget(file_card)

    numeric_title = QLabel("Numeric Columns")
    numeric_title.setObjectName("section")
    window.numeric_text = QTextEdit()
    window.numeric_text.setReadOnly(True)
    window.numeric_text.setFixedHeight(128)

    x_label = QLabel("X Column")
    x_label.setObjectName("fieldLabel")
    y_label = QLabel("Y Column")
    y_label.setObjectName("fieldLabel")
    window.x_combo = QComboBox()
    window.y_combo = QComboBox()
    window.plot_button = QPushButton("Generate Plot")

    left_layout.addWidget(title)
    left_layout.addWidget(subtitle)
    left_layout.addWidget(upload_card)
    left_layout.addWidget(numeric_title)
    left_layout.addWidget(window.numeric_text)
    left_layout.addWidget(x_label)
    left_layout.addWidget(window.x_combo)
    left_layout.addWidget(y_label)
    left_layout.addWidget(window.y_combo)
    left_layout.addSpacing(2)
    left_layout.addWidget(window.plot_button)
    left_layout.addStretch(1)

    left_scroll = QScrollArea()
    left_scroll.setObjectName("sideScroll")
    left_scroll.setWidgetResizable(True)
    left_scroll.setFrameShape(QFrame.NoFrame)
    left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    left_scroll.setWidget(left_panel)
    left_scroll.setMinimumWidth(280)
    left_scroll.setMaximumWidth(360)

    center_panel = QFrame()
    center_panel.setObjectName("panel")
    center_layout = QVBoxLayout(center_panel)
    center_layout.setContentsMargins(22, 22, 22, 22)
    center_layout.setSpacing(14)

    chart_card = QFrame()
    chart_card.setObjectName("softCard")
    chart_card_layout = QVBoxLayout(chart_card)
    chart_card_layout.setContentsMargins(16, 14, 16, 14)
    chart_card_layout.setSpacing(4)
    chart_title = QLabel("Plot")
    chart_title.setObjectName("section")
    chart_desc = QLabel("Scatter plot with a linear regression line.")
    chart_desc.setObjectName("muted")
    chart_card_layout.addWidget(chart_title)
    chart_card_layout.addWidget(chart_desc)

    plot_frame = QFrame()
    plot_frame.setObjectName("plotFrame")
    plot_layout = QVBoxLayout(plot_frame)
    plot_layout.setContentsMargins(14, 14, 14, 14)
    plot_layout.setSpacing(0)
    window.plot_canvas = PlotCanvas()
    plot_layout.addWidget(window.plot_canvas)

    preview_card = QFrame()
    preview_card.setObjectName("softCard")
    preview_layout = QVBoxLayout(preview_card)
    preview_layout.setContentsMargins(16, 14, 16, 14)
    preview_layout.setSpacing(8)
    preview_title = QLabel("Data Preview")
    preview_title.setObjectName("section")
    preview_desc = QLabel("Top rows from the loaded CSV file.")
    preview_desc.setObjectName("muted")
    window.preview_table = QTableWidget()
    window.preview_table.setObjectName("previewTable")
    window.preview_table.setMinimumHeight(180)
    window.preview_table.setAlternatingRowColors(True)
    window.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)

    preview_layout.addWidget(preview_title)
    preview_layout.addWidget(preview_desc)
    preview_layout.addWidget(window.preview_table)

    center_layout.addWidget(chart_card)
    center_layout.addWidget(plot_frame, 1)
    center_layout.addWidget(preview_card)

    right_panel = QFrame()
    right_panel.setObjectName("panel")
    right_panel.setMinimumWidth(250)
    right_panel.setMaximumWidth(340)
    right_layout = QVBoxLayout(right_panel)
    right_layout.setContentsMargins(22, 22, 22, 22)
    right_layout.setSpacing(12)

    result_title = QLabel("Analysis")
    result_title.setObjectName("section")
    result_desc = QLabel("Key regression values appear here after loading data.")
    result_desc.setWordWrap(True)
    result_desc.setObjectName("muted")

    count_card = QFrame()
    count_card.setObjectName("softCard")
    count_layout = QVBoxLayout(count_card)
    count_layout.setContentsMargins(16, 14, 16, 14)
    count_layout.setSpacing(4)
    count_label = QLabel("Data points")
    count_label.setObjectName("metricLabel")
    window.count_value = QLabel("-")
    window.count_value.setObjectName("metricValue")
    count_layout.addWidget(count_label)
    count_layout.addWidget(window.count_value)

    r2_card = QFrame()
    r2_card.setObjectName("softCard")
    r2_layout = QVBoxLayout(r2_card)
    r2_layout.setContentsMargins(16, 14, 16, 14)
    r2_layout.setSpacing(4)
    r2_label = QLabel("R-squared")
    r2_label.setObjectName("metricLabel")
    window.r2_value = QLabel("-")
    window.r2_value.setObjectName("metricValue")
    r2_layout.addWidget(r2_label)
    r2_layout.addWidget(window.r2_value)

    equation_card = QFrame()
    equation_card.setObjectName("softCard")
    equation_layout = QVBoxLayout(equation_card)
    equation_layout.setContentsMargins(16, 14, 16, 14)
    equation_layout.setSpacing(8)
    eq_label = QLabel("Regression equation")
    eq_label.setObjectName("metricLabel")
    window.eq_text = QTextEdit()
    window.eq_text.setReadOnly(True)
    window.eq_text.setFixedHeight(110)
    equation_layout.addWidget(eq_label)
    equation_layout.addWidget(window.eq_text)

    right_layout.addWidget(result_title)
    right_layout.addWidget(result_desc)
    right_layout.addWidget(count_card)
    right_layout.addWidget(r2_card)
    right_layout.addWidget(equation_card)
    right_layout.addSpacing(6)
    window.save_button = QPushButton("Save PNG")
    right_layout.addWidget(window.save_button)
    right_layout.addStretch(1)

    layout.addWidget(left_scroll, 2)
    layout.addWidget(center_panel, 5)
    layout.addWidget(right_panel, 2)
    return root


def app_stylesheet() -> str:
    return """
    QWidget {
        background: #F2F4F7;
        color: #182230;
        font-family: 'Segoe UI';
        font-size: 14px;
    }
    QLabel {
        background: transparent;
    }
    #sideScroll {
        background: transparent;
        border: none;
    }
    #leftPanel {
        background: #E8EDF4;
        border: 1px solid #D7E0EA;
        border-radius: 18px;
    }
    #panel {
        background: #FFFFFF;
        border: 1px solid #DFE5EC;
        border-radius: 18px;
    }
    #softCard {
        background: #F8FAFC;
        border: 1px solid #E4EAF1;
        border-radius: 14px;
    }
    #fileBadge {
        background: #FFFFFF;
        border: 1px solid #DCE4EE;
        border-radius: 12px;
    }
    #plotFrame {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
    }
    #title {
        font-size: 32px;
        font-weight: 800;
        color: #142033;
    }
    #section {
        font-size: 18px;
        font-weight: 700;
        color: #142033;
    }
    #fieldLabel {
        color: #4A5565;
        font-size: 13px;
        font-weight: 700;
    }
    #muted {
        color: #607086;
        font-size: 13px;
        font-weight: 500;
        line-height: 1.4;
    }
    #subtle {
        color: #536274;
        font-size: 13px;
        font-weight: 600;
    }
    #metricLabel {
        color: #5F6F82;
        font-size: 13px;
        font-weight: 700;
    }
    #metricValue {
        font-size: 26px;
        font-weight: 800;
        color: #2F6FED;
    }
    QPushButton, QComboBox {
        min-height: 40px;
        border-radius: 12px;
    }
    QPushButton, QToolButton {
        background: #2F6FED;
        color: white;
        border: none;
        font-weight: 700;
        padding: 0 16px;
        min-height: 40px;
        border-radius: 12px;
    }
    QPushButton:hover, QToolButton:hover {
        background: #265ED0;
    }
    QPushButton[secondary="true"], QToolButton[secondary="true"] {
        background: #FFFFFF;
        color: #2F6FED;
        border: 1px solid #D4DEF3;
    }
    QPushButton[secondary="true"]:hover, QToolButton[secondary="true"]:hover {
        background: #F7FAFF;
    }
    QComboBox, QTextEdit, QTableWidget {
        background: #FFFFFF;
        border: 1px solid #D6DEE8;
        border-radius: 12px;
        padding: 8px 10px;
        color: #182230;
        font-weight: 600;
    }
    QToolButton::menu-indicator {
        subcontrol-origin: padding;
        subcontrol-position: center right;
        right: 12px;
    }
    QMenu {
        background: #FFFFFF;
        border: 1px solid #D6DEE8;
        color: #182230;
        padding: 6px;
    }
    QMenu::item {
        padding: 8px 24px 8px 12px;
        border-radius: 8px;
        margin: 2px 4px;
    }
    QMenu::item:selected {
        background: #E8F0FF;
        color: #2F6FED;
    }
    QComboBox::drop-down {
        border: none;
        width: 26px;
    }
    QTextEdit {
        selection-background-color: #DCE7FF;
    }
    QTableWidget {
        gridline-color: #E4EAF1;
        alternate-background-color: #F8FAFC;
    }
    QHeaderView::section {
        background: #EEF3F9;
        color: #304256;
        border: none;
        border-bottom: 1px solid #DCE4EE;
        padding: 8px;
        font-weight: 700;
    }
    """
