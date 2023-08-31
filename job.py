import argparse
import imapclient
import yaml
import sqlite3

def download_emails(yml_file):
    # Load email credentials from the .yml file
    with open(yml_file, 'r') as file:
        email_config = yaml.safe_load(file)

    # Connect to the email server
    server = imapclient.IMAPClient(email_config['server'])
    server.login(email_config['username'], email_config['password'])

    # Select the mailbox and search for emails with "factura" in the subject
    server.select_folder('INBOX')
    messages = server.search(['SUBJECT "factura"'])

    # Connect to the SQLite database
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()

    # Create a table to store the emails if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails
                      (subject TEXT, sender TEXT, body TEXT)''')

    # Download and save the emails
    for msg_id, data in server.fetch(messages, ['ENVELOPE', 'BODY[TEXT]']).items():
        envelope = data[b'ENVELOPE']
        body = data[b'BODY[TEXT]'].decode('utf-8')

        # Extract the subject and sender from the email
        subject = envelope.subject.decode('utf-8')
        sender = envelope.sender[0].mailbox.decode('utf-8') + "@" + envelope.sender[0].host.decode('utf-8')

        # Insert the email into the SQLite database
        cursor.execute("INSERT INTO emails VALUES (?, ?, ?)", (subject, sender, body))

    # Commit and close the database connection
    conn.commit()
    conn.close()

    print("Emails downloaded and saved successfully!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and save emails with specific subject.')
    parser.add_argument('yml_file', help='Path to the .yml file containing email credentials')
    args = parser.parse_args()

    download_emails(args.yml_file)