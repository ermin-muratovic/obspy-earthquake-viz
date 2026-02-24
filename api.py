"""
Seismic Microservice API
A simple FastAPI application to calculate seismic wave travel times.
"""

from fastapi import FastAPI
from math import radians, cos, sin, asin, sqrt

# Initialize the API app
app = FastAPI(
    title="Iberian Seismology API",
    description="Calculates P-wave travel times based on epicenter and station coordinates.",
    version="1.0.0"
)

# Our existing math function
def haversine_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * 6371  # Radius of earth in km

# Create the API Endpoint
@app.get("/travel-time/")
def calculate_travel_time(eq_lat: float, eq_lon: float, sta_lat: float, sta_lon: float):
    """
    Pass the latitude and longitude of the earthquake and the station.
    Returns the distance and estimated P-wave arrival time.
    """
    # Calculate distance
    distance_km = haversine_distance(eq_lat, eq_lon, sta_lat, sta_lon)
    
    # Estimate travel time (assuming 7.0 km/s crustal speed)
    travel_time_sec = distance_km / 7.0
    
    # APIs return data as JSON (dictionaries in Python)
    return {
        "earthquake_coordinates": {"lat": eq_lat, "lon": eq_lon},
        "station_coordinates": {"lat": sta_lat, "lon": sta_lon},
        "metrics": {
            "distance_km": round(distance_km, 2),
            "estimated_p_wave_arrival_seconds": round(travel_time_sec, 2),
            "assumed_speed_km_s": 7.0
        }
    }
