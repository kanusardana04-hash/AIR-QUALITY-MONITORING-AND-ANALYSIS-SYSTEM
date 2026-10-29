# Air Quality Monitoring and Analysis System

A Python desktop application (Tkinter) to record, classify and analyse air-quality readings of different cities. Built as an MCA mini project for **Python Programming (26CAH606)** at Chandigarh University.

> **Note:** The AQI value used here is a simplified, illustrative indicator made for this academic project. It is **not** the official AQI formula and should not be used for health decisions.

## Features

- Enter city, date and pollutant values (PM2.5, PM10, NO2, SO2, CO) through a GUI
- Input validation (empty city, non-numeric or negative values, invalid date)
- Calculates an AQI indicator and classifies it as Good, Satisfactory, Moderate, Poor, Very Poor or Severe, with a health recommendation
- Saves every record permanently in `air_quality_data.csv` using pandas
- Shows the latest 100 records in a table (newest first)
- Imports air-quality data in bulk from a CSV file
- Bar graph of the latest record's pollutant values (Matplotlib)
- Summary analysis: total records, average AQI indicator, average of each pollutant and the pollutant with the highest average

## Tech Stack

| Purpose | Library |
|---|---|
| GUI | Tkinter (ttk, messagebox, filedialog) |
| Data handling | pandas, NumPy |
| Graph | Matplotlib |
| Storage | CSV file |

## Requirements

- Python 3.8 or higher
- Tkinter (comes with Python on Windows and macOS; on Ubuntu/Debian install with `sudo apt install python3-tk`)

## Installation and Run

````bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

# 2. Install the required libraries
pip install pandas numpy matplotlib

# 3. Run the application
python air_quality_monitor.py
````

The file `air_quality_data.csv` is created automatically on the first run.

## How to Use

1. Enter the city name, date (`YYYY-MM-DD`, default is today) and the five pollutant values.
2. Click **Calculate & Save** to see the AQI indicator, category and recommendation. The record is saved and added to the table.
3. Click **Import CSV** to load many records at once.
4. Click **Show Graph** for the bar chart of the latest record.
5. Click **Show Analysis** for the summary of all saved records.
6. Click **Clear Fields** to reset the form.

### CSV format for import

The file must contain these columns (AQI and Category are calculated automatically):

````
Date,City,PM2.5,PM10,NO2,SO2,CO
2026-10-20,Ludhiana,85,140,40,12,1.1
````

All pollutant values must be non-negative numbers.

> **Important:** Importing a CSV file replaces the records already saved in `air_quality_data.csv`. Keep a backup if you need the old data.

## AQI Indicator Calculation

````
indicator = mean(PM2.5/5, PM10/10, NO2/2, SO2/2, CO*10)
AQI       = round(min(indicator, 500))
````

| AQI Indicator | Category |
|---|---|
| 0 – 50 | Good |
| 51 – 100 | Satisfactory |
| 101 – 200 | Moderate |
| 201 – 300 | Poor |
| 301 – 400 | Very Poor |
| 401 – 500 | Severe |

## Project Structure

````
├── air_quality_monitor.py   # main application
├── air_quality_data.csv     # generated data file
├── screenshots/             # application screenshots
└── README.md
````

## Screenshots

Add your screenshots to the `screenshots/` folder and link them here:

````
![Main window](screenshots/main_window.png)
![Result](screenshots/result.png)
![Graph](screenshots/graph.png)
````

## Limitations

- AQI indicator is a simplified formula, not the official AQI
- Data is entered manually or imported; no real-time sensor support
- Graph shows only the latest record (no trends over time)
- CSV storage is not suitable for very large data or multiple users

## Future Scope

- Official AQI calculation with pollutant breakpoints
- Real-time data from air-quality APIs
- Trend graphs and city-wise comparison
- Database storage (SQLite/MySQL) and PDF/Excel export

## Author

**Kashish** — UID: 26MCA20152
MCA (General), Semester I, Chandigarh University
Submitted to: Ms. Deepali Saini, Department of Computer Applications