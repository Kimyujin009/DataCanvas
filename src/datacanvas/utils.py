from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression


def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def numeric_columns(dataframe: pd.DataFrame) -> list[str]:
    return dataframe.select_dtypes(include="number").columns.tolist()


def regression_summary(dataframe: pd.DataFrame, x_col: str, y_col: str) -> dict:
    clean = dataframe[[x_col, y_col]].dropna().copy()
    clean[x_col] = pd.to_numeric(clean[x_col], errors="coerce")
    clean[y_col] = pd.to_numeric(clean[y_col], errors="coerce")
    clean = clean.dropna()

    x = clean[[x_col]].to_numpy()
    y = clean[y_col].to_numpy()

    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    r2 = model.score(x, y)
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)

    sign = "+" if intercept >= 0 else "-"
    equation = f"y = {slope:.4f}x {sign} {abs(intercept):.4f}"

    return {
        "data": clean,
        "x": x.flatten(),
        "y": y,
        "y_pred": y_pred,
        "equation": equation,
        "r2": float(r2),
        "count": int(len(clean)),
    }
