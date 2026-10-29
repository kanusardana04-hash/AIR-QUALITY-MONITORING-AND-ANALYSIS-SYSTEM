import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date
import os

# CSV file for storing data
FILE_NAME = "air_quality_data.csv"

COLUMNS = [
    "Date", "City", "PM2.5", "PM10", "NO2", "SO2", "CO", "AQI", "Category"
]


# Create CSV file if it does not exist
def initialize_file():
    if not os.path.exists(FILE_NAME):
        pd.DataFrame(columns=COLUMNS).to_csv(FILE_NAME, index=False)


# Classify AQI using an illustrative project scale.
# This is a simplified demonstration, not an official AQI calculation.
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"


# Main window
root = tk.Tk()
root.title("Air Quality Monitoring and Analysis System")
root.geometry("1100x750")
root.minsize(900, 650)
root.configure(bg="#edf2f7")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="white",
    foreground="#172554",
    rowheight=28,
    fieldbackground="white"
)
style.configure(
    "Treeview.Heading",
    background="#1e3a8a",
    foreground="white",
    font=("Arial", 10, "bold")
)

# Header
header = tk.Frame(root, bg="#172554", height=85)
header.pack(fill="x")

tk.Label(
    header,
    text="AIR QUALITY MONITORING SYSTEM",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#172554"
).pack(pady=(15, 3))

tk.Label(
    header,
    text="Monitor Pollution | Analyze Data | Understand Air Quality",
    font=("Arial", 10),
    fg="#bfdbfe",
    bg="#172554"
).pack()

# Main container
main = tk.Frame(root, bg="#edf2f7")
main.pack(fill="both", expand=True, padx=15, pady=12)

# Left panel: Data entry
left = tk.LabelFrame(
    main,
    text=" Enter Air Quality Data ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#1e3a8a",
    padx=15,
    pady=12
)
left.pack(side="left", fill="y", padx=(0, 12))

fields = [
    ("City Name", "city"),
    ("PM2.5 (µg/m³)", "pm25"),
    ("PM10 (µg/m³)", "pm10"),
    ("NO2 (µg/m³)", "no2"),
    ("SO2 (µg/m³)", "so2"),
    ("CO (mg/m³)", "co")
]

entries = {}

for row, (label_text, key) in enumerate(fields):
    tk.Label(
        left,
        text=label_text,
        font=("Arial", 10),
        bg="white"
    ).grid(row=row, column=0, sticky="w", pady=9)

    entry = ttk.Entry(left, width=23, font=("Arial", 10))
    entry.grid(row=row, column=1, pady=9, padx=(8, 0))
    entries[key] = entry

# Date entry
tk.Label(
    left,
    text="Date (YYYY-MM-DD)",
    font=("Arial", 10),
    bg="white"
).grid(row=6, column=0, sticky="w", pady=9)

date_entry = ttk.Entry(left, width=23, font=("Arial", 10))
date_entry.grid(row=6, column=1, pady=9, padx=(8, 0))
date_entry.insert(0, date.today().isoformat())

# Right panel
right = tk.Frame(main, bg="#edf2f7")
right.pack(side="left", fill="both", expand=True)

# AQI display
aqi_card = tk.LabelFrame(
    right,
    text=" Air Quality Result ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#1e3a8a",
    padx=12,
    pady=10
)
aqi_card.pack(fill="x", pady=(0, 10))

aqi_label = tk.Label(
    aqi_card,
    text="AQI: --",
    font=("Arial", 25, "bold"),
    fg="#1e3a8a",
    bg="white"
)
aqi_label.pack(pady=5)

category_label = tk.Label(
    aqi_card,
    text="Enter data to calculate the illustrative AQI",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#475569"
)
category_label.pack(pady=5)

recommendation_label = tk.Label(
    aqi_card,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#334155",
    wraplength=650,
    justify="left"
)
recommendation_label.pack(pady=5)


def get_recommendation(category):
    recommendations = {
        "Good": "Air quality is good. Continue normal outdoor activities.",
        "Satisfactory": "Air quality is acceptable. Sensitive individuals should monitor symptoms.",
        "Moderate": "Some sensitive individuals may experience discomfort. Consider reducing prolonged outdoor exertion.",
        "Poor": "Consider limiting prolonged outdoor exertion, especially if sensitive to pollution.",
        "Very Poor": "Reduce outdoor exertion and follow local air-quality advisories.",
        "Severe": "Avoid strenuous outdoor activity and follow official health guidance."
    }
    return recommendations[category]


def calculate_aqi():
    try:
        city = entries["city"].get().strip()

        if not city:
            messagebox.showerror("Input Error", "Please enter the city name.")
            return

        pm25 = float(entries["pm25"].get())
        pm10 = float(entries["pm10"].get())
        no2 = float(entries["no2"].get())
        so2 = float(entries["so2"].get())
        co = float(entries["co"].get())

        values = [pm25, pm10, no2, so2, co]

        if not all(np.isfinite(v) and v >= 0 for v in values):
            messagebox.showerror(
                "Input Error",
                "Enter valid, non-negative pollution measurements."
            )
            return

        entered_date = date.fromisoformat(date_entry.get().strip())

        # Simplified illustrative indicator for this student project.
        # It is NOT an official AQI formula.
        indicator = np.mean([
            pm25 / 5,
            pm10 / 10,
            no2 / 2,
            so2 / 2,
            co * 10
        ])

        aqi = int(round(min(indicator, 500)))
        category = classify_aqi(aqi)

        aqi_label.config(text=f"AQI Indicator: {aqi}")
        category_label.config(text=f"Category: {category}")
        recommendation_label.config(
            text=get_recommendation(category)
        )

        # Store the entered measurements and result
        record = pd.DataFrame([{
            "Date": entered_date.isoformat(),
            "City": city,
            "PM2.5": pm25,
            "PM10": pm10,
            "NO2": no2,
            "SO2": so2,
            "CO": co,
            "AQI": aqi,
            "Category": category
        }], columns=COLUMNS)

        if os.path.exists(FILE_NAME):
            old_data = pd.read_csv(FILE_NAME)
            data = pd.concat([old_data, record], ignore_index=True)
        else:
            data = record

        data.to_csv(FILE_NAME, index=False)

        load_data()
        messagebox.showinfo(
            "Success",
            f"Record saved successfully!\n"
            f"City: {city}\n"
            f"AQI indicator: {aqi}\n"
            f"Category: {category}"
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Check your measurements and date.\n"
            "Use numbers for pollution values and YYYY-MM-DD for the date."
        )
    except Exception as error:
        messagebox.showerror("Error", str(error))


def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)

    date_entry.delete(0, tk.END)
    date_entry.insert(0, date.today().isoformat())

    aqi_label.config(text="AQI: --")
    category_label.config(text="Enter data to calculate the illustrative AQI")
    recommendation_label.config(text="")


def load_data():
    for item in table.get_children():
        table.delete(item)

    if not os.path.exists(FILE_NAME):
        return

    try:
        data = pd.read_csv(FILE_NAME).fillna("")
        for _, row in data.tail(100).iloc[::-1].iterrows():
            table.insert(
                "",
                tk.END,
                values=[row.get(column, "") for column in COLUMNS]
            )
    except Exception as error:
        messagebox.showerror("File Error", str(error))


def import_csv():
    file_path = filedialog.askopenfilename(
        title="Select air quality CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    try:
        data = pd.read_csv(file_path)

        required = ["Date", "City", "PM2.5", "PM10", "NO2", "SO2", "CO"]

        if not all(column in data.columns for column in required):
            messagebox.showerror(
                "Invalid File",
                "CSV must contain these columns:\n" + ", ".join(required)
            )
            return

        for column in ["PM2.5", "PM10", "NO2", "SO2", "CO"]:
            data[column] = pd.to_numeric(data[column], errors="raise")

        measurements = data[["PM2.5", "PM10", "NO2", "SO2", "CO"]].to_numpy()

        if not np.isfinite(measurements).all() or (measurements < 0).any():
            messagebox.showerror(
                "Invalid Data",
                "Measurements must be finite, non-negative numbers."
            )
            return

        # Calculate illustrative indicators for imported records
        data["AQI"] = np.rint(np.minimum(
            np.mean(
                np.column_stack([
                    data["PM2.5"].to_numpy() / 5,
                    data["PM10"].to_numpy() / 10,
                    data["NO2"].to_numpy() / 2,
                    data["SO2"].to_numpy() / 2,
                    data["CO"].to_numpy() * 10
                ]),
                axis=1
            ),
            500
        )).astype(int)

        data["Category"] = data["AQI"].apply(classify_aqi)

        # Keep the required columns and save imported records
        data = data[COLUMNS]
        data.to_csv(FILE_NAME, index=False)

        load_data()
        messagebox.showinfo(
            "Success",
            "CSV data imported and saved successfully."
        )

    except Exception as error:
        messagebox.showerror("Import Error", str(error))


def show_graph():
    if not os.path.exists(FILE_NAME):
        messagebox.showwarning(
            "No Data",
            "Enter or import data before generating graphs."
        )
        return

    try:
        data = pd.read_csv(FILE_NAME)

        if data.empty:
            messagebox.showwarning("No Data", "No records are available.")
            return

        latest = data.iloc[-1]

        pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO"]
        values = [float(latest[column]) for column in pollutants]

        graph_window = tk.Toplevel(root)
        graph_window.title("Air Quality Analysis Graph")
        graph_window.geometry("800x550")
        graph_window.configure(bg="white")

        figure, axis = plt.subplots(figsize=(8, 4.5))
        axis.bar(pollutants, values)
        axis.set_title(f"Pollutant Measurements - {latest['City']}")
        axis.set_xlabel("Pollutants")
        axis.set_ylabel("Recorded concentration")
        axis.grid(axis="y", linestyle="--", alpha=0.4)
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(figure)

    except Exception as error:
        messagebox.showerror("Graph Error", str(error))


def show_analysis():
    if not os.path.exists(FILE_NAME):
        messagebox.showwarning("No Data", "No records available.")
        return

    try:
        data = pd.read_csv(FILE_NAME)

        if data.empty:
            messagebox.showwarning("No Data", "No records available.")
            return

        pollutant_columns = ["PM2.5", "PM10", "NO2", "SO2", "CO"]
        averages = data[pollutant_columns].mean(numeric_only=True)
        highest = averages.idxmax()

        result = (
            f"Total records: {len(data)}\n\n"
            f"Average AQI indicator: {data['AQI'].mean():.2f}\n\n"
            f"Highest average measurement: {highest}\n\n"
            f"Average pollutant measurements:\n"
        )

        for pollutant, average in averages.items():
            result += f"{pollutant}: {average:.2f}\n"

        messagebox.showinfo("Air Quality Analysis", result)

    except Exception as error:
        messagebox.showerror("Analysis Error", str(error))


# Buttons
button_frame = tk.Frame(left, bg="white")
button_frame.grid(row=7, column=0, columnspan=2, pady=18)

tk.Button(
    button_frame,
    text="Calculate & Save",
    command=calculate_aqi,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=7
).pack(fill="x", pady=4)

tk.Button(
    button_frame,
    text="Import CSV",
    command=import_csv,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=7
).pack(fill="x", pady=4)

tk.Button(
    button_frame,
    text="Show Graph",
    command=show_graph,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=7
).pack(fill="x", pady=4)

tk.Button(
    button_frame,
    text="Show Analysis",
    command=show_analysis,
    bg="#0f766e",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=7
).pack(fill="x", pady=4)

tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    bg="#64748b",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=7
).pack(fill="x", pady=4)

# Data table
table_frame = tk.LabelFrame(
    right,
    text=" Recent Air Quality Records ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#1e3a8a",
    padx=8,
    pady=8
)
table_frame.pack(fill="both", expand=True)

table_scroll = ttk.Scrollbar(table_frame, orient="vertical")
table_scroll.pack(side="right", fill="y")

table = ttk.Treeview(
    table_frame,
    columns=COLUMNS,
    show="headings",
    yscrollcommand=table_scroll.set
)

table_scroll.config(command=table.yview)

for column in COLUMNS:
    table.heading(column, text=column)
    table.column(column, width=85, minwidth=65, anchor="center")

table.pack(fill="both", expand=True)

# Footer
footer = tk.Label(
    root,
    text="Air Quality Monitoring and Analysis System | Python Mini Project",
    bg="#172554",
    fg="white",
    font=("Arial", 9),
    pady=7
)
footer.pack(fill="x")

# Start application
initialize_file()
load_data()
root.mainloop()

