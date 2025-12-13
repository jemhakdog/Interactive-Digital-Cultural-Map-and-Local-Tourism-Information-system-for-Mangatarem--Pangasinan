import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, recipient, body, html_body=None, sender_email=None, sender_password=None, smtp_server='smtp.gmail.com', smtp_port=587):
    """
    Sends an email using SMTP.
    
    Args:
        subject (str): The subject of the email.
        recipient (str): The recipient's email address.
        body (str): The plain text body of the email.
        html_body (str, optional): The HTML body of the email.
        sender_email (str, optional): The sender's email address. Defaults to env var SMTP_EMAIL.
        sender_password (str, optional): The sender's password. Defaults to env var SMTP_PASSWORD.
        smtp_server (str, optional): The SMTP server address. Defaults to 'smtp.gmail.com'.
        smtp_port (int, optional): The SMTP port. Defaults to 587.
    
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    sender_email = sender_email or os.environ.get('SMTP_EMAIL')
    sender_password = sender_password or os.environ.get('SMTP_PASSWORD')

    if not sender_email or not sender_password:
        print("Error: SMTP credentials not provided.")
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    if html_body:
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.close()
        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
