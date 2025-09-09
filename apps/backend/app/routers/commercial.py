from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import unquote
import base64
import httpx
import pdfkit
import io
import os
from config.settings import settings

router = APIRouter()

templates_path = "templates"
env = Environment(
    loader=FileSystemLoader(templates_path),
    autoescape=select_autoescape(['html', 'xml'])
)

@router.get("/commercial/{url}/{image}/{municipality}/{area}/{businesses}")
async def generate_commercial_pdf(
    url: str,
    image: str,
    municipality: str,
    area: str,
    businesses: str
):
    try:
        decoded_url = base64.b64decode(url).decode("utf-8").replace(" ", "%20")
        decoded_url = decoded_url.replace(
            settings.DEFAULT_GEOSERVER,
            settings.URL_GEOSERVER
        )

        decoded_image = base64.b64decode(image).decode("utf-8")
        decoded_municipality = base64.b64decode(municipality).decode("utf-8")
        decoded_area = base64.b64decode(area).decode("utf-8")
        decoded_businesses = base64.b64decode(businesses).decode("utf-8")

        async with httpx.AsyncClient() as client:
            response = await client.get(decoded_url)
            geo_data = response.json().get("features", [])

        template = env.get_template("comercial.html")
        rendered_html = template.render(
            data=geo_data,
            municipality=decoded_municipality,
            logo=settings.APP_LOGO,
            area=decoded_area,
            image=decoded_image,
            businesses=decoded_businesses,
            url_minimapa=settings.URL_MINIMAPA
        )

        pdf_output = pdfkit.from_string(rendered_html, False, options={
            "enable-local-file-access": "",
            "quiet": ""
        })

        return StreamingResponse(io.BytesIO(pdf_output), media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=commercial.pdf"
        })

    except Exception as e:
        return Response(content=f"Error generating PDF: {str(e)}", status_code=500)
