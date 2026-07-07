import random
import smtplib
from email.message import EmailMessage

def generate_otp(to_mail):
    otp = ""

    for i in range(6):
        otp += str(random.randint(0,9))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    from_mail = 'abccc485@gmail.com'

    server.login('abccc485@gmail.com', 'fjsy oqbz sczp bxvy')

    msg = EmailMessage()
    msg['Subject'] = "Your secure login code for attendance"
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg.set_content("Your OTP is "+ otp)

    server.send_message(msg)

    print('Email Sent')
    print(otp)
    return otp

    
