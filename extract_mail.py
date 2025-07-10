import configparser
import imaplib
import email
from email.header import decode_header
import datetime

def get_mail():

    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    username = config['gmail']['USER']
    password = config['gmail']['PASSWORD']

    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    since_date = seven_days_ago.strftime("%d-%b-%Y")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")

    status, messages = mail.search(None, f'(UNSEEN SINCE {since_date})')

    return mail, messages
