import email
from email.header import decode_header
import pandas as pd
import load_mail_data
import re

def get_details(msg_data):

    bucket_name = 'work-mail-data'
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            from_ = msg.get("From")
            match = re.search(r"<(.*?)>", from_)
            if match:
                from_1 = match.group(1)
            else:
                from_1 = from_.strip()


            cc = msg.get("Cc")
            cc_match = re.search(r"<(.*?)>", cc) if cc else None
            cc = cc_match.group(1) if cc_match else ""

            body = ""
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            load_mail_data.upload_to_s3(part, filename, from_1, attachments)
                            
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            attachments = ", ".join(attachments)
            all_data_of_this_user = f"s3://{bucket_name}/{from_1}/"
            
    return from_1, cc, subject, body, attachments, all_data_of_this_user