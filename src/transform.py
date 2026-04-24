from datetime import datetime, timezone

def normalize_export(raw: dict) -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "garminconnect",
        "device": raw.get("device", "Garmin Venu SQ2"),
        "range": raw.get("range", {}),
        "days": raw.get("days", []),
    }

def validate_export(payload: dict) -> None:
    required = ["schema_version", "generated_at", "source", "device", "range", "days"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Hiányzó mezők: {missing}")
    if not isinstance(payload["days"], list):
        raise TypeError("A days mezőnek listának kell lennie")
