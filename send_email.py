from email import message
import json 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from dotenv import load_dotenv
import os
load_dotenv()

USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
TOEMAIL = os.environ['TOEMAIL']

msg = MIMEMultipart()

password = PASSWORD
msg['From'] = USER
msg['To'] = TOEMAIL
msg['Subject'] = 'Minhapikagrossa'

def SendEmail(aaaa:str):
    msg.attach(MIMEText(aaaa, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()