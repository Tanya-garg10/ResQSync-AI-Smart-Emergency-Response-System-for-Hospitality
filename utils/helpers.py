"""Common utility functions for ResQSync AI."""
import random
import string
from datetime import datetime, timedelta


def generate_incident_id():
    """Generate a unique incident ID."""
    return random.randint(1000, 9999)


def generate_node_id():
    """Generate a zone/node identifier."""
    return f"NODE-{random.randint(1000, 9999)}"


def get_timestamp():
    """Get current timestamp formatted."""
    return datetime.now().strftime("%I:%M:%S %p")


def get_date_display():
    """Get formatted date for header."""
    return datetime.now().strftime("%a, %b %d")


def severity_color(severity: str) -> str:
    """Return color hex for severity level."""
    return {
        "CRITICAL": "#FF4B4B",
        "PRIORITY": "#FF8C00",
        "MODERATE": "#FFD700",
        "LOW": "#00C853",
    }.get(severity.upper(), "#AAAAAA")


def status_color(status: str) -> str:
    """Return color for status."""
    return {
        "ACTIVE": "#00C853",
        "RESPONDING": "#FF8C00",
        "RESOLVED": "#666666",
        "EN ROUTE": "#00BFFF",
    }.get(status.upper(), "#AAAAAA")


def incident_icon(incident_type: str) -> str:
    """Return emoji icon for incident type."""
    return {
        "FIRE": "🔥",
        "MEDICAL": "🏥",
        "SECURITY": "🚨",
        "EVACUATION": "🚪",
    }.get(incident_type.upper(), "⚠️")


def random_coordinates(center_lat=20.0, center_lon=0.0, spread=60):
    """Generate random coordinates around a center point."""
    lat = center_lat + random.uniform(-spread, spread)
    lon = center_lon + random.uniform(-spread, spread)
    return round(lat, 4), round(lon, 4)


def generate_demo_incidents(count=8):
    """Generate demo incident data."""
    types = ["FIRE", "MEDICAL", "SECURITY", "MEDICAL"]
    severities = ["CRITICAL", "PRIORITY", "MODERATE", "LOW"]
    statuses = ["ACTIVE", "RESPONDING", "ACTIVE", "RESOLVED"]
    incidents = []
    for i in range(count):
        t = types[i % len(types)]
        s = severities[i % len(severities)]
        st = statuses[i % len(statuses)]
        ts = datetime.now() - timedelta(seconds=random.randint(0, 300))
        incidents.append({
            "id": generate_incident_id(),
            "type": t,
            "zone": generate_node_id(),
            "severity": s,
            "status": st,
            "timestamp": ts.strftime("%I:%M:%S %p"),
            "lat": round(random.uniform(10, 50), 4),
            "lon": round(random.uniform(-30, 60), 4),
        })
    return incidents


def generate_network_health():
    """Generate network health metrics."""
    return {
        "DATABASE UPLINK": random.randint(88, 99),
        "SATELLITE LINK-1": random.randint(80, 95),
        "NEURAL CORE": random.randint(85, 99),
        "VOICE ENGINE": 100,
    }
