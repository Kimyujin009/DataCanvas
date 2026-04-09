from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QHeaderView, QMainWindow, QMenu, QMessageBox, QTableWidgetItem

from .ui import app_stylesheet, build_main_ui
from .utils import load_csv, numeric_columns, regression_summary


class DataCanvasWindow(QMainWindow):
    SAMPLE_FILES = {
        "Experiment Yield": "sample_experiment.csv",
        "Drag Force": "sample_drag_force.csv",
        "Motor Sensor": "sample_sensor.csv",
    }

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DataCanvas")
        self.resize(1360, 760)
        self.setMinimumSize(980, 640)

        self.dataframe = None
        self.current_path: Path | None = None

        self.setCentralWidget(build_main_ui(self))
        self.setStyleSheet(app_stylesheet())
        self._connect_events()
        self._build_sample_menu()
        self.plot_canvas.show_placeholder("Load the sample CSV or your own CSV to begin.")
        self.eq_text.setPlainText("Regression details will appear here after data is loaded.")
        self._configure_preview_table()

    def _resource_root(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parents[2]

    def _connect_events(self) -> None:
        self.open_button.clicked.connect(self.open_csv)
        self.plot_button.clicked.connect(self.generate_plot)
        self.save_button.clicked.connect(self.save_png)

    def _build_sample_menu(self) -> None:
        menu = QMenu(self)
        for sample_name in ["Motor Sensor", "Drag Force", "Experiment Yield"]:
            action = QAction(sample_name, self)
            action.triggered.connect(lambda checked=False, name=sample_name: self.load_sample_csv(name))
            menu.addAction(action)
        self.sample_button.setMenu(menu)

    def _configure_preview_table(self) -> None:
        header = self.preview_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.preview_table.verticalHeader().setVisible(False)

    def _populate_preview_table(self, max_rows: int = 6) -> None:
        if self.dataframe is None or self.dataframe.empty:
            self.preview_table.setRowCount(0)
            self.preview_table.setColumnCount(0)
            return

        preview = self.dataframe.head(max_rows)
        self.preview_table.setRowCount(len(preview))
        self.preview_table.setColumnCount(len(preview.columns))
        self.preview_table.setHorizontalHeaderLabels([str(col) for col in preview.columns])

        for row_index, (_, row) in enumerate(preview.iterrows()):
            for col_index, value in enumerate(row):
                self.preview_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def open_csv(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV",
            str(self._resource_root() / "data"),
            "CSV Files (*.csv)",
        )
        if file_name:
            self.load_dataframe(Path(file_name))

    def load_sample_csv(self, sample_name: str | None = None) -> None:
        sample_name = sample_name or "Experiment Yield"
        sample_file = self.SAMPLE_FILES.get(sample_name, "sample_experiment.csv")
        sample_path = self._resource_root() / "data" / sample_file
        if not sample_path.exists():
            QMessageBox.critical(self, "Sample Missing", f"Built-in sample CSV was not found.\n\n{sample_path}")
            return
        self.load_dataframe(sample_path)

    def load_dataframe(self, path: Path) -> None:
        try:
            dataframe = load_csv(path)
        except Exception as exc:
            QMessageBox.critical(self, "Load Failed", f"Could not read the CSV file.\n\n{exc}")
            return

        columns = numeric_columns(dataframe)
        if len(columns) < 2:
            QMessageBox.warning(self, "Not Enough Numeric Columns", "At least two numeric columns are required.")
            return

        self.dataframe = dataframe
        self.current_path = path
        self.file_label.setText(f"Current file: {path.name}")
        self.numeric_text.setPlainText("\n".join(columns))
        self._populate_preview_table()

        self.x_combo.clear()
        self.y_combo.clear()
        self.x_combo.addItems(columns)
        self.y_combo.addItems(columns)
        self.x_combo.setCurrentIndex(0)
        self.y_combo.setCurrentIndex(1 if len(columns) > 1 else 0)

        self.count_value.setText("-")
        self.r2_value.setText("-")
        self.eq_text.setPlainText("Auto-generating the first plot from the default X and Y columns.")
        self.generate_plot()

    def generate_plot(self) -> None:
        if self.dataframe is None:
            QMessageBox.information(self, "No Data", "Load the sample CSV or your own CSV first.")
            return

        x_col = self.x_combo.currentText()
        y_col = self.y_combo.currentText()
        if not x_col or not y_col:
            QMessageBox.warning(self, "Missing Selection", "Please confirm both X and Y columns.")
            return
        if x_col == y_col:
            QMessageBox.warning(self, "Invalid Selection", "Choose different columns for X and Y.")
            return

        try:
            result = regression_summary(self.dataframe, x_col, y_col)
        except Exception as exc:
            QMessageBox.critical(self, "Analysis Failed", f"Plotting or regression failed.\n\n{exc}")
            return

        self.plot_canvas.draw_regression(result["x"], result["y"], result["y_pred"], x_col, y_col)
        self.eq_text.setPlainText(result["equation"])
        self.r2_value.setText(f"{result['r2']:.4f}")
        self.count_value.setText(str(result["count"]))

    def save_png(self) -> None:
        if self.dataframe is None:
            QMessageBox.information(self, "Nothing To Save", "Load data and generate a plot first.")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save PNG",
            "datacanvas_plot.png",
            "PNG Files (*.png)",
        )
        if not file_name:
            return

        try:
            self.plot_canvas.figure.savefig(file_name, dpi=180, bbox_inches="tight")
        except Exception as exc:
            QMessageBox.critical(self, "Save Failed", f"PNG export failed.\n\n{exc}")
