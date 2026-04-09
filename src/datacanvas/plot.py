from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self) -> None:
        self.figure = Figure(figsize=(6, 5), dpi=100, facecolor="white")
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self._apply_padding()

    def _apply_padding(self) -> None:
        self.figure.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.22)

    def show_placeholder(self, message: str) -> None:
        self.axes.clear()
        self.axes.set_axis_off()
        self._apply_padding()
        self.axes.text(0.5, 0.63, "[]", ha="center", va="center", fontsize=16, color="#B8C4D6")
        self.axes.text(
            0.5,
            0.50,
            message,
            ha="center",
            va="center",
            fontsize=13,
            color="#607080",
            wrap=True,
        )
        self.axes.text(
            0.5,
            0.39,
            "Load a CSV file to render the scatter plot and regression line.",
            ha="center",
            va="center",
            fontsize=10,
            color="#98A2B3",
            wrap=True,
        )
        self.draw_idle()

    def draw_regression(self, x, y, y_pred, x_label: str, y_label: str) -> None:
        self.axes.clear()
        self.axes.set_axis_on()
        self._apply_padding()
        self.axes.set_facecolor("#FCFDFE")
        self.axes.scatter(x, y, s=54, color="#2F6FED", alpha=0.88, edgecolors="white", linewidths=0.9)
        order = x.argsort()
        self.axes.plot(x[order], y_pred[order], color="#2F6FED", linewidth=2.3)
        self.axes.set_xlabel(x_label, labelpad=10)
        self.axes.set_ylabel(y_label, labelpad=8)
        self.axes.set_title(f"{y_label} vs {x_label}", fontsize=13, fontweight="bold", color="#17212B", pad=8)
        self.axes.grid(True, linestyle="--", linewidth=0.5, alpha=0.22, color="#94A3B8")
        for spine in self.axes.spines.values():
            spine.set_color("#D8E0EA")
        self.draw_idle()
