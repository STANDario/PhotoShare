from io import BytesIO

import qrcode


def generate_qr_code(url: str):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_img = BytesIO()
    img.save(qr_code_img)
    qr_code_img.seek(0)
    return qr_code_img
