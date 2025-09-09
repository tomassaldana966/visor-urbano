from fastapi import APIRouter, Request, Depends, HTTPException, Query
from config.settings import settings
import httpx
import logging

router = APIRouter()

@router.get("/geocode")
async def geocode_address(
    address: str = Query(..., min_length=6),  # domicilio
    municipality: str = Query(...),           # municipio
    request: Request = None
):
    address = f"{address}, {municipality}, Jalisco"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": settings.GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
    except httpx.RequestError as e:
        logging.error(f"HTTP request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

    if data.get("status") == "OVER_QUERY_LIMIT":
        user_ip = request.client.host if request else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")

        logging.warning("Google Maps API rate limit exceeded.", {
            "ip": user_ip,
            "user_agent": user_agent
        })

        raise HTTPException(status_code=429, detail=f"API rate limit exceeded. IP: {user_ip} - Logging this event.")

    if data.get("results"):
        return data["results"][0]

    raise HTTPException(status_code=404, detail="No results found")


@router.get("/reverse-geocode")
async def reverse_geocode(
    lat: float = Query(..., ge=-90, le=90, description="Latitude must be between -90 and 90"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude must be between -180 and 180")
):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": settings.GOOGLE_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
    except httpx.RequestError as e:
        logging.error(f"HTTP request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

    if data.get("results"):
        return data["results"][0]

    raise HTTPException(status_code=404, detail="No results found")
