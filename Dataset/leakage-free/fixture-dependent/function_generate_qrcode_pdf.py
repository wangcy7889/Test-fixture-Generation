
import os, qrcode, io
from reportlab.pdfgen import canvas
from pathlib import Path

def generate_qrcode_pdf(data: str,
                        out_path: str,
                        env_tmp: str = 'QR_TMP') -> str:

    tmp_dir = os.getenv(env_tmp)
    if not tmp_dir:
        raise EnvironmentError('Error: QR_TMP is not set')
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)
    img = qrcode.make(data)
    png_path = Path(tmp_dir) / 'code.png'
    img.save(png_path)

    c = canvas.Canvas(out_path)
    c.drawImage(str(png_path), 100, 500, width=200, height=200)
    c.save()
    return str(Path(out_path).resolve())
