import configparser 
import boto3
import os
import pyodbc


def upload_to_s3(part, filename, from_1, attachments):

    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    aws_access_key_id = config['AWS']['aws_access_key_id']
    aws_secret_access_key = config['AWS']['aws_secret_access_key']
    region_name = config['AWS']['region']

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    bucket_name = 'work-mail-data'

    local_path = f"./{filename}"
    with open(local_path, "wb") as f:
        f.write(part.get_payload(decode=True))
    s3_key = f"{from_1}/{filename}"
    s3.upload_file(local_path, bucket_name, s3_key)
    s3_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{s3_key}"
    attachments.append(s3_url)
    os.remove(local_path)

def load_to_sql_database(from_1, cc, subject, body, attachments, all_data_of_this_user):

    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    DRIVER = config['ssms']['DRIVER']
    SERVER = config['ssms']['SERVER']
    DATABASE = config['ssms']['DATABASE']
    UID = config['ssms']['UID']
    PWD = config['ssms']['PWD']

    conn = pyodbc.connect(
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={UID};'
            f'PWD={PWD}'
    )

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO gmail_data ([from], cc, subject, body, attachments, all_data_of_this_user)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(
    insert_query,
    from_1, 
    cc, 
    subject, 
    body, 
    attachments, 
    all_data_of_this_user
    )

    conn.commit()
    cursor.close()
    conn.close()

