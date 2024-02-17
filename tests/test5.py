import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(sender_email, recipient_email, subject, body, smtp_username, smtp_password, smtp_server, smtp_port):
    # Email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sender_email = "fuckyou@blackstackhub.com"
    recipient_email = "devfemibadmus@gmail.com"
    subject = "greeting"
    body = "test"
    smtp_username = "fuckyou"
    smtp_password = "Helloworld1$"
    smtp_server = "blackstackhub.com"  # Corrected SMTP server address
    smtp_port = 25

    send_mail(sender_email, recipient_email, subject, body, smtp_username, smtp_password, smtp_server, smtp_port)


    send_mail(sender_email, recipient_email, subject, body, smtp_username, smtp_password, smtp_server, smtp_port)
