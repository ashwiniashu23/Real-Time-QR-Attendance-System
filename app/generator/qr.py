import qrcode
import os
# print(os.getcwd())


def generate_qr(token):

    path = f"C:/Users/Ashwini S/Desktop/QR Attendance/Attendance/static/QRCodes{token}.png"
    link = f"127.0.0.1:8000/attendance/{token}"
    print(link)

    myqr = qrcode.make(link)
    myqr.save(path)

    return path