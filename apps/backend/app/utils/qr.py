import base64
from io import BytesIO
import qrcode

def generate_qr_code(data: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return f"data:image/png;base64,{qr_base64}"
