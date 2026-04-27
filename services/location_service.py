"""Location Tracking & Map Utilities."""
import random


# Demo hotel locations
HOTEL_ZONES = {
    "LOBBY": {"lat": 28.6139, "lon": 77.2090, "floor": "Ground"},
    "POOL": {"lat": 28.6145, "lon": 77.2095, "floor": "Ground"},
    "RESTAURANT": {"lat": 28.6142, "lon": 77.2088, "floor": "1st"},
    "ROOM-101": {"lat": 28.6138, "lon": 77.2092, "floor": "1st"},
    "ROOM-201": {"lat": 28.6140, "lon": 77.2093, "floor": "2nd"},
    "ROOM-301": {"lat": 28.6141, "lon": 77.2091, "floor": "3rd"},
    "PARKING": {"lat": 28.6135, "lon": 77.2085, "floor": "Basement"},
    "CONFERENCE": {"lat": 28.6143, "lon": 77.2087, "floor": "2nd"},
}


def get_zone_location(zone_name: str) -> dict:
    """Get coordinates for a hotel zone."""
    zone = HOTEL_ZONES.get(zone_name.upper())
    if zone:
        return zone
    # Random location within hotel bounds
    return {
        "lat": 28.6139 + random.uniform(-0.001, 0.001),
        "lon": 77.2090 + random.uniform(-0.001, 0.001),
        "floor": "Unknown",
    }


def get_responder_location(incident_lat: float, incident_lon: float, progress: float = 0.5) -> dict:
    """Simulate responder moving toward incident. progress: 0.0 to 1.0"""
    # Responder starts from lobby
    start_lat, start_lon = 28.6139, 77.2090
    current_lat = start_lat + (incident_lat - start_lat) * progress
    current_lon = start_lon + (incident_lon - start_lon) * progress
    return {
        "lat": round(current_lat, 6),
        "lon": round(current_lon, 6),
        "progress": progress,
        "status": "EN ROUTE" if progress < 0.95 else "ARRIVED",
        "eta_seconds": int((1 - progress) * 120),
    }


def get_nearest_exit(lat: float, lon: float) -> dict:
    """Find nearest emergency exit."""
    exits = [
        {"name": "Main Entrance", "lat": 28.6136, "lon": 77.2089},
        {"name": "Fire Exit A", "lat": 28.6141, "lon": 77.2096},
        {"name": "Fire Exit B", "lat": 28.6137, "lon": 77.2083},
        {"name": "Emergency Stairwell", "lat": 28.6144, "lon": 77.2091},
    ]
    nearest = min(exits, key=lambda e: abs(e["lat"] - lat) + abs(e["lon"] - lon))
    return nearest
