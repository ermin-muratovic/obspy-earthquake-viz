"""
Seismic Data Visualization: Alenquer Earthquake (Feb 2026)
Queries FDSN APIs to plot waveform data and map the event epicenter.
"""

import folium
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# Initialize FDSN clients for global (IRIS) and European (EMSC) data
client_global = Client("IRIS")
client_eu = Client("EMSC")

# Define the event time (Alenquer, Portugal M4.1 on Feb 19, 2026)
eq_time = UTCDateTime("2026-02-19T12:14:00")

# ==========================================
# 1. FETCH AND PLOT WAVEFORM DATA
# ==========================================
print("Downloading seismic waveform data...")

# Fetch 20 minutes of data from Station PAB (San Pablo, Spain)
st = client_global.get_waveforms(
    network="IU",       
    station="PAB",      
    location="00",      
    channel="BHZ",      
    starttime=eq_time, 
    endtime=eq_time + 1200  
)

# Apply a bandpass filter (0.5 - 5.0 Hz) to isolate local earthquake frequencies
st.filter("bandpass", freqmin=0.5, freqmax=5.0)

# Plot the waveform
st.plot(type="relative", color="red", title="Feb 2026 Alenquer Quake recorded at IU.PAB (Spain)")

# ==========================================
# 2. GENERATE INTERACTIVE EPICENTER MAP
# ==========================================
print("Fetching event coordinates and generating map...")

# Fetch earthquake metadata from EMSC
catalog = client_eu.get_events(starttime=eq_time - 120, endtime=eq_time + 120, minmagnitude=4.0)
eq_lat = catalog[0].origins[0].latitude
eq_lon = catalog[0].origins[0].longitude

# Fetch station metadata from IRIS
inventory = client_global.get_stations(network="IU", station="PAB")
sta_lat = inventory[0][0].latitude
sta_lon = inventory[0][0].longitude

# Create the Folium map centered between the two points
m = folium.Map(location=[(eq_lat + sta_lat) / 2, (eq_lon + sta_lon) / 2], zoom_start=6)

# Add markers for the earthquake (red) and station (blue)
folium.Marker(
    [eq_lat, eq_lon], 
    popup="Magnitude 4.1 Earthquake (Alenquer)", 
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

folium.Marker(
    [sta_lat, sta_lon], 
    popup="Seismic Station: IU.PAB (Spain)", 
    icon=folium.Icon(color="blue", icon="flag")
).add_to(m)

# Draw the wave path
folium.PolyLine([(eq_lat, eq_lon), (sta_lat, sta_lon)], color="black", dash_array="5, 5").add_to(m)

# Display the map (if in Colab/Jupyter)
m

# If not on Jupyter/Colab instead of just m do this (which works on any computer):
# m.save("earthquake_map.html")
