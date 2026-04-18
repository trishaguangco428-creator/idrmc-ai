from collections import defaultdict
from datetime import datetime

ZONE_COORDS = {
    "Zone 1": {"lat": 8.4945, "lng": 124.6415},
    "Zone 2": {"lat": 8.4932, "lng": 124.6462},
    "Zone 3": {"lat": 8.4908, "lng": 124.6508},
    "Zone 4": {"lat": 8.4893, "lng": 124.6478},
    "Zone 5": {"lat": 8.4872, "lng": 124.6448},
    "Zone 6": {"lat": 8.4860, "lng": 124.6502},
}

ZONE_BASE_SCORE = {
    "Zone 1": 25,
    "Zone 2": 42,
    "Zone 3": 78,
    "Zone 4": 18,
    "Zone 5": 82,
    "Zone 6": 48,
}

SEVERITY_WEIGHT = {"Low": 1, "Medium": 2, "High": 3}
RAINY_MONTHS    = [6, 7, 8, 9, 10, 11]

def analyze_flood_risk(incidents: list[dict]) -> list[dict]:
    zone_flood_count = defaultdict(int)
    zone_flood_score = defaultdict(float)
    zone_total       = defaultdict(int)

    for inc in incidents:
        zone     = inc.get("zone", "")
        inc_type = inc.get("type", "")
        severity = inc.get("severity", "Low")
        date_str = inc.get("date_reported", "") or inc.get("created_at", "")

        if zone not in ZONE_COORDS:
            continue

        zone_total[zone] += 1

        if inc_type == "Flood":
            zone_flood_count[zone] += 1
            score = SEVERITY_WEIGHT.get(severity, 1)

            if date_str:
                try:
                    dt = datetime.fromisoformat(
                        date_str.replace("Z", "+00:00")
                    )
                    if dt.month in RAINY_MONTHS:
                        score += 0.8
                except Exception:
                    pass

            zone_flood_score[zone] += score

    all_scores = [
        ZONE_BASE_SCORE[z] + zone_flood_score.get(z, 0) * 6
        for z in ZONE_COORDS
    ]
    max_score = max(all_scores) if all_scores else 1

    results = []
    for zone, coords in ZONE_COORDS.items():
        base    = ZONE_BASE_SCORE[zone]
        dynamic = zone_flood_score.get(zone, 0) * 6
        total   = min(base + dynamic, 100)
        weight  = round(total / max_score, 2)

        risk_level = (
            "High"   if total >= 65 else
            "Medium" if total >= 35 else
            "Low"
        )

        results.append({
            "zone":            zone,
            "lat":             coords["lat"],
            "lng":             coords["lng"],
            "weight":          weight,
            "risk_level":      risk_level,
            "flood_count":     zone_flood_count.get(zone, 0),
            "total_incidents": zone_total.get(zone, 0),
            "ai_score":        round(total, 1),
            "base_score":      base,
        })

    results.sort(key=lambda x: x["ai_score"], reverse=True)
    return results