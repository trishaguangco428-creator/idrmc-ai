from fastapi import APIRouter, HTTPException
from services import django_client, flood_ai
from schemas.flood import (
    HeatmapResponse, SummaryResponse,
    PredictRequest, PredictResponse,
)

router = APIRouter(prefix="/ai/flood", tags=["Flood AI"])

RAINY_MONTHS = [6, 7, 8, 9, 10, 11]


@router.get("/heatmap", response_model=HeatmapResponse)
async def flood_heatmap():
    """Called by MapPage.jsx (web) and MapScreen.js (mobile)"""
    try:
        incidents = await django_client.get_incidents()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach Django: {str(e)}"
        )

    heatmap      = flood_ai.analyze_flood_risk(incidents)
    total_floods = sum(z["flood_count"] for z in heatmap)

    return {
        "total_flood_incidents": total_floods,
        "total_zones":           len(heatmap),
        "heatmap":               heatmap,
    }


@router.get("/summary", response_model=SummaryResponse)
async def flood_summary():
    """Called by Dashboard and Reports pages"""
    try:
        incidents = await django_client.get_incidents()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach Django: {str(e)}"
        )

    heatmap = flood_ai.analyze_flood_risk(incidents)
    zones   = []

    for z in heatmap:
        total  = z["total_incidents"]
        floods = z["flood_count"]
        zones.append({
            "zone":            z["zone"],
            "flood_incidents": floods,
            "total_incidents": total,
            "flood_rate":      round(
                floods / total * 100 if total > 0 else 0, 1
            ),
            "risk_level":      z["risk_level"],
            "ai_score":        z["ai_score"],
        })

    return {"zones": zones}


@router.post("/predict", response_model=PredictResponse)
async def flood_predict(body: PredictRequest):
    """Called by RiskScreen (mobile) and RiskIntelligencePage (web)"""
    try:
        incidents = await django_client.get_incidents()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach Django: {str(e)}"
        )

    heatmap   = flood_ai.analyze_flood_risk(incidents)
    zone_data = next(
        (z for z in heatmap if z["zone"] == body.zone), None
    )

    if not zone_data:
        raise HTTPException(
            status_code=404,
            detail=f"Zone '{body.zone}' not found"
        )

    severity_boost = {"Low": 0, "Medium": 8, "High": 18}.get(
        body.severity, 0
    )
    rainy_boost = 8 if body.month in RAINY_MONTHS else 0
    final_score = min(
        zone_data["ai_score"] + severity_boost + rainy_boost, 100
    )

    predicted_risk = (
        "High"   if final_score >= 65 else
        "Medium" if final_score >= 35 else
        "Low"
    )

    confidence = round(min(60 + zone_data["flood_count"] * 5, 95), 1)

    recommendations = {
        "High":   "⚠️ Pre-position resources, notify residents, prepare evacuation routes.",
        "Medium": "📋 Monitor water levels, alert barangay officials, check evac centers.",
        "Low":    "✅ No immediate action needed. Continue regular monitoring.",
    }

    return {
        "zone":           body.zone,
        "predicted_risk": predicted_risk,
        "confidence":     confidence,
        "recommendation": recommendations[predicted_risk],
    }