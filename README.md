# DataCanvas

DataCanvas is a Windows desktop utility that loads CSV data, lets the user choose numeric X/Y columns, draws a scatter plot, and shows a linear regression equation with R-squared.

## 1. Run Environment

- Operating system: Windows 10 or later
- Python: 3.11 recommended
- Tested libraries: `PySide6`, `pandas`, `matplotlib`, `scikit-learn`

## 2. Installation

Install the required packages with:

```powershell
python -m pip install -r requirements.txt
```

Optional release build:

```powershell
scripts\build.bat
```

## 3. How To Run

### Source execution

1. Open PowerShell in the project folder.
2. Install the dependencies with `python -m pip install -r requirements.txt`.
3. Run the app with `python .\src\main.py`.
4. In the app, click `Open CSV` for your own file or `Load Sample CSV` for a built-in sample dataset.
5. Check the plot, regression equation, R-squared, and data preview.

### Release execution

1. Open the `Release\DataCanvas` folder after building.
2. Run `DataCanvas.exe`.
3. Use `Open CSV` or `Load Sample CSV` inside the app.

## 4. Project Structure

```text
DataCanvas/
├─ src/
│  ├─ main.py
│  └─ datacanvas/
├─ data/
│  ├─ sample_experiment.csv
│  ├─ sample_drag_force.csv
│  └─ sample_sensor.csv
├─ Release/ or dist/DataCanvas/
├─ README.md
└─ report.html
```

## 5. Main Features

- Load a user CSV file
- Load one of three built-in sample CSV datasets
- Detect numeric columns automatically
- Select X and Y columns
- Draw a scatter plot
- Draw a linear regression line
- Show regression equation and R-squared
- Preview top rows of the loaded CSV
- Save the plot as PNG

## 6. Administrator Permission

Administrator permission is **not required**.
