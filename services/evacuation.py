"""Auto-Evacuation Guidance Service."""
from services.location_service import get_nearest_exit


EVACUATION_INSTRUCTIONS = {
    "FIRE": [
        "🔥 FIRE EVACUATION PROTOCOL",
        "1. Stay low to avoid smoke inhalation",
        "2. Do NOT use elevators",
        "3. Follow illuminated exit signs",
        "4. Close doors behind you",
        "5. Proceed to assembly point",
        "6. Do NOT re-enter the building",
    ],
    "MEDICAL": [
        "🏥 MEDICAL EMERGENCY PROTOCOL",
        "1. Do not move the patient unless in danger",
        "2. Clear the area for medical team",
        "3. Keep airways open if trained",
        "4. Apply pressure to any bleeding",
        "5. Stay with patient until help arrives",
    ],
    "SECURITY": [
        "🚨 SECURITY THREAT PROTOCOL",
        "1. RUN – Evacuate if safe path exists",
        "2. HIDE – Find secure room, lock doors",
        "3. FIGHT – Last resort only",
        "4. Silence your phone",
        "5. Wait for all-clear from security",
    ],
}


def get_evacuation_plan(incident_type: str, lat: float, lon: float) -> dict:
    """Generate evacuation plan for an incident."""
    nearest_exit = get_nearest_exit(lat, lon)
    instructions = EVACUATION_INSTRUCTIONS.get(
        incident_type.upper(),
        ["⚠️ Follow staff instructions", "Proceed to nearest exit calmly"]
    )
    return {
        "incident_type": incident_type,
        "nearest_exit": nearest_exit,
        "instructions": instructions,
        "assembly_point": "Hotel Main Parking Lot – Section A",
    }
