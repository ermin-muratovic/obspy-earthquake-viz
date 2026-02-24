"""
Iberian Seismology Analysis Tool
Calculates distance, estimates travel time, plots waveforms, 
and maps the epicenter of the Feb 2026 Alenquer Earthquake.
"""

import folium
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from math import radians, cos, sin, asin, sqrt
import os

# --- Setup & Config ---
# Define the Haversine formula for distance calculation on a sphere
def haversine_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in km
    return c * r

# Initialize Clients
client_global = Client("IRIS")
client_eu = Client("EMSC")

# Target Event: Alenquer, Portugal M4.1 on Feb 19, 2026
eq_time = UTCDateTime("2026-02-19T12:14:00")

print("=== Starting Iberian Seismic Analysis ===\n")

# ==========================================
# 1. FETCH METADATA & PERFORM CALCULATIONS
# ==========================================
print("Fetching coordinates and calculating geometry...")
catalog = client_eu.get_events(starttime=eq_time - 120, endtime=eq_time + 120, minmagnitude=4.0)
eq_lat = catalog[0].origins[0].latitude
eq_lon = catalog[0].origins[0].longitude

inventory = client_global.get_stations(network="IU", station="PAB")
sta_lat = inventory[0][0].latitude
sta_lon = inventory[0][0].longitude

# Calculate distance and estimate travel time (assuming ~7 km/s P-wave speed)
distance_km = haversine_distance(eq_lat, eq_lon, sta_lat, sta_lon)
estimated_travel_time = distance_km / 7.0

print(f"-> Epicenter: {eq_lat:.4f}, {eq_lon:.4f}")
print(f"-> Station: {sta_lat:.4f}, {sta_lon:.4f}")
print(f"-> Calculated Distance: {distance_km:.2f} km")
print(f"-> Estimated P-Wave Arrival: +{estimated_travel_time:.1f} seconds after origin\n")


# ==========================================
# 2. FETCH AND PLOT WAVEFORM DATA
# ==========================================
print("Downloading and filtering waveform data...")
st = client_global.get_waveforms(
    network="IU", station="PAB", location="00", channel="BHZ",      
    starttime=eq_time, endtime=eq_time + 1200  
)
# Apply bandpass filter for local events to remove noise
st.filter("bandpass", freqmin=0.5, freqmax=5.0)
print("-> Waveform data acquired. Check popup window for plot.\n")

# Note: In a standard terminal, this opens a window. In notebooks, it plots inline.
st.plot(type="relative", color="red", title="Feb 2026 Alenquer Quake @ IU.PAB")


# ==========================================
# 3. GENERATE ENHANCED MAP
# ==========================================
print("Generating interactive map with expanding rings...")
m = folium.Map(location=[(eq_lat + sta_lat) / 2, (eq_lon + sta_lon) / 2], zoom_start=7)

# Add concentric expansion rings (20km, 50km, 100km)
radii_meters = [20000, 50000, 100000]
for radius in radii_meters:
    folium.Circle(
        location=[eq_lat, eq_lon], radius=radius,
        color="crimson", weight=2, fill=True, fill_opacity=0.1
    ).add_to(m)

# Add Markers
folium.Marker(
    [eq_lat, eq_lon], popup="M4.1 Epicenter", 
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

folium.Marker(
    [sta_lat, sta_lon], 
    popup=f"Station IU.PAB<br>Distance: {distance_km:.1f} km", 
    icon=folium.Icon(color="blue", icon="flag")
).add_to(m)

folium.PolyLine([(eq_lat, eq_lon), (sta_lat, sta_lon)], color="black", dash_array="5, 5", weight=3).add_to(m)

# Save map to HTML file if running as a script
output_file = "seismic_map.html"
m.save(output_file)
print(f"-> Map generated and saved to '{output_file}'. Open this file in your browser.\n")
print("=== Analysis Complete ===")
