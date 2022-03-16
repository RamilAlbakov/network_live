"""Send email."""

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv('.env')


def send_email(to, subject, message, filepath='', cc=''):
    """
    Send email.

    Args:
        to: string
        subject: string
        message: string
        filepath: string
        cc: string
    """
    fromaddr = os.getenv('EMAIL_ADDRESS')

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = to
    msg['CC'] = cc
    toaddr = to.split(',') + cc.split(',')
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if filepath != '':
        with open(filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)

            filename = os.path.basename(filepath)
            part.add_header('Content-Disposition', 'attachment; filename={filename}'.format(
                filename=filename,
            ))
            msg.attach(part)

    host = os.getenv('EMAIL_HOST')
    server = smtplib.SMTP(host)
    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
