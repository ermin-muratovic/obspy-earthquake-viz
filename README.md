# Iberian Peninsula Seismic Data Visualization

This repository contains Python scripts designed to fetch, filter, and visualize real-world seismic data using global and regional FDSN APIs. 

The project specifically analyzes a Magnitude 4.1 earthquake that occurred near Alenquer, Portugal (Lisbon area) in February 2026, recorded by a broadband seismograph in Toledo, Spain (Network: IU, Station: PAB).

## 📊 Project Visuals

<img width="749" height="237" alt="image" src="https://github.com/user-attachments/assets/fa6c94da-c515-4669-9710-feadc710234e" />
> **Figure 1:** Filtered waveform (0.5 Hz - 5.0 Hz bandpass) showing the P-wave and S-wave arrivals from the Alenquer earthquake at the Spanish sensor.

<img width="1715" height="794" alt="image" src="https://github.com/user-attachments/assets/8545e52a-e0b2-4cc9-b8b3-4faf228c573c" />
> **Figure 2:** Interactive Folium map plotting the earthquake epicenter (red) and the monitoring station (blue), connected by the seismic wave's travel path.

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Core programming language. |
| **ObsPy** | Framework for processing seismological data and querying FDSN web services. |
| **Folium** | Generating interactive Leaflet.js maps. |
| **FDSN APIs** | Fetching raw waveform data (IRIS) and earthquake event catalogs (EMSC). |

## 🚀 How to Run

This code is optimized to run in a Jupyter Notebook or **Google Colab** environment. 

1. Open [Google Colab](https://colab.research.google.com/).
2. Create a new notebook and paste the code from `main.ipynb` or `main.py`.
3. Install the required dependencies in the first cell:
   `!pip install -r requirements.txt` (or simply `!pip install obspy folium`)
4. Run the cells to generate the waveform plots and interactive maps.

## 🧠 Methodological Notes
* **Frequency Filtering:** Because local, smaller earthquakes generate sharp, high-frequency waves (unlike distant, massive quakes which generate low, rolling frequencies), a bandpass filter of `0.5 Hz to 5.0 Hz` is applied to the raw data to remove background "cultural noise" and isolate the seismic event.
