from fastapi import APIRouter
import secrets

router = APIRouter()

@router.get("/key")
def generate_key():
    """Generates a secure 32-character random key."""
    return {"key": secrets.token_hex(16)}  # Equivalent to Str::random(32)

@router.get("/news")
def get_news():
    """Returns image and link info for news section."""
    return {
        "data": {
            "href": "https://visorurbano.com",
            "src": "https://visorurbano.jalisco.gob.mx/assets/images/planes.png",
            "src_xs": "https://visorurbano.jalisco.gob.mx/assets/images/planes.png"
        },
        "status": True
    }