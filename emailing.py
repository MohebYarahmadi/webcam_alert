import smtplib
import imghdr
from email.message import EmailMessage
import glob, os

host = 'smtp.gmail.com'
port = 587  # for ssl use 465

SENDER = 'momobitcoin1986@gmail.com'
PASSWORD = '******************'

reciever = SENDER



def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = 'New customer showedup!'
    email_message.set_content("Hey, we just have a new customer!")

    with open(image_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image',
                                subtype=imghdr.what(None, content))

    with smtplib.SMTP(host, port) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(SENDER, PASSWORD)
        smtp_server.sendmail(SENDER, reciever, email_message.as_string())

    _clean_images()


def image_to_send():
    all_images = glob.glob('images/*.png')
    index = int(len(all_images) / 2)
    return all_images[index]


def _clean_images():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
