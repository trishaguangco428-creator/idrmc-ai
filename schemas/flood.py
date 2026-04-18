from pydantic import BaseModel
from typing import List

class HeatmapPoint(BaseModel):
    zone:            str
    lat:             float
    lng:             float
    weight:          float
    risk_level:      str
    flood_count:     int
    total_incidents: int
    ai_score:        float
    base_score:      int

class HeatmapResponse(BaseModel):
    total_flood_incidents: int
    total_zones:           int
    heatmap:               List[HeatmapPoint]

class ZoneSummary(BaseModel):
    zone:            str
    flood_incidents: int
    total_incidents: int
    flood_rate:      float
    risk_level:      str
    ai_score:        float

class SummaryResponse(BaseModel):
    zones: List[ZoneSummary]

class PredictRequest(BaseModel):
    zone:     str
    severity: str = "Medium"
    month:    int = 7

class PredictResponse(BaseModel):
    zone:           str
    predicted_risk: str
    confidence:     float
    recommendation: str