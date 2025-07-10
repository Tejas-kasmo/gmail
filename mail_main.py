import extract_mail
import transform_mail
import load_mail_data

print("connnecting to mail..")
mail, messages = extract_mail.get_mail()
email_ids = messages[0].split()
print('connected and retrived msg ids')
print('-'*100)

for email_id in email_ids:

    status, msg_data = mail.fetch(email_id, "(RFC822)")
    print(f'mail id: {email_id}')

    from_1, cc, subject, body, attachments, all_data_of_this_user = transform_mail.get_details(msg_data=msg_data)
    print('transformation: done')

    load_mail_data.load_to_sql_database(from_1, cc, subject, body, attachments, all_data_of_this_user)
    print("insert to ssms: done")
    print('-'*100)

print("process finished.")
