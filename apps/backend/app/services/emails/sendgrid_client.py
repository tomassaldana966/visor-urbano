import os
from sendgrid import SendGridAPIClient #type: ignore
from sendgrid.helpers.mail import Mail, Email, To, Content #type: ignore
from fastapi.templating import Jinja2Templates
from jinja2 import Template #type: ignore

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAIL_FROM_ADDRESS = os.getenv("MAIL_FROM_ADDRESS", "notificaciones-visorurbano@jalisco.gob.mx")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Visor Urbano Notificaciones")

# Use absolute path for templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def send_email(to_email: str, subject: str, html_content: str):
    message = Mail(
        from_email=Email(MAIL_FROM_ADDRESS, MAIL_FROM_NAME),
        to_emails=To(to_email),
        subject=subject,
        html_content=Content("text/html", html_content)
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return {
            "status_code": response.status_code,
            "body": response.body,
            "headers": response.headers,
        }
    except Exception as e:
        return {"error": str(e)}

def render_email_template(template_name: str, context: dict) -> str:
    with open(f"{TEMPLATES_DIR}/{template_name}", "r", encoding="utf-8") as file:
        template_content = file.read()
        template = Template(template_content)
        return template.render(**context)
