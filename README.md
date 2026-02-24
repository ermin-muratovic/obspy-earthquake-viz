# Iberian Peninsula Seismic Data Visualization

This repository contains Python scripts designed to fetch, filter, and visualize real-world seismic data using global and regional FDSN APIs. 

The project specifically analyzes a Magnitude 4.1 earthquake that occurred near Alenquer, Portugal (Lisbon area) in February 2026, recorded by a broadband seismograph in Toledo, Spain (Network: IU, Station: PAB).

## 📊 Project Visuals

<img width="749" height="237" alt="image" src="https://github.com/user-attachments/assets/5baf43ee-809e-41e7-9e7c-70cdc867d6a4" />

> **Figure 1:** Filtered waveform (0.5 Hz - 5.0 Hz bandpass) showing the P-wave and S-wave arrivals from the Alenquer earthquake at the Spanish sensor.

<img width="1517" height="829" alt="image" src="https://github.com/user-attachments/assets/da554344-b125-4e86-ad41-46198b95e639" />

> **Figure 2:** Interactive Folium map plotting the earthquake epicenter (red) and the monitoring station (blue), connected by the seismic wave's travel path.

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language. |
| **ObsPy** | Framework for processing seismological data and querying FDSN web services. |
| **Folium** | Generating interactive Leaflet.js maps. |
| **FDSN APIs** | Fetching raw waveform data (IRIS) and earthquake event catalogs (EMSC). |
| **FastAPI & Uvicorn** | Exposing the seismic travel-time calculator as a RESTful microservice. |

## 🚀 How to Run

### Option 1: Data Visualization (Colab / Jupyter)
This code is optimized to run in a Jupyter Notebook or **Google Colab** environment. 
1. Open [Google Colab](https://colab.research.google.com/).
2. Create a new notebook and paste the code from `main.ipynb` or `main.py`.
3. Install the required dependencies in the first cell: 
 `!pip install -r requirements.txt` (or simply `!pip install obspy folium`)
4. Run the cells to generate the waveform plots and interactive maps.

### Option 2: Run the API Microservice (Local)
This repository includes a standalone API (`api.py`) that calculates P-wave travel times based on epicenter and station coordinates.

1. Clone this repository and navigate to the folder.
2. Install the requirements: `pip install -r requirements.txt`
3. Start the local server using Uvicorn:
   ```bash
   uvicorn api:app --reload

## 🧠 Methodological Notes
* **Frequency Filtering:** Because local, smaller earthquakes generate sharp, high-frequency waves (unlike distant, massive quakes which generate low, rolling frequencies), a bandpass filter of `0.5 Hz to 5.0 Hz` is applied to the raw data to remove background "cultural noise" and isolate the seismic event.
