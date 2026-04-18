import httpx
from core.config import settings

HEADERS = {
    "ngrok-skip-browser-warning": "true",
    "Content-Type": "application/json",
}

async def get_incidents() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{settings.DJANGO_API_URL}/api/incidents/",
            headers=HEADERS,
        )
        response.raise_for_status()
        return response.json()

async def get_residents() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{settings.DJANGO_API_URL}/api/residents/",
            headers=HEADERS,
        )
        response.raise_for_status()
        return response.json()

async def get_evac_centers() -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{settings.DJANGO_API_URL}/api/evacuation-centers/",
            headers=HEADERS,
        )
        response.raise_for_status()
        return response.json()