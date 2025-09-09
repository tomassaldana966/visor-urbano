import os

def get_logo(folio: str) -> str:    
    default_logo_url = os.getenv("DEFAULT_LOGO_URL", "/logos/visor-urbano.svg")
    return default_logo_url
