import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def send_email():    
    # SMTP server configuration
    smtp_server = 'blackstackhub.com'
    smtp_port = 587  # Port for TLS (STARTTLS)

    # Sender and recipient email addresses
    sender_email = 'test7@blackstackhub.com'
    recipient_email = 'devfemibadmus@gmail.com'

    # SMTP username and password (authentication credentials)
    smtp_username = 'test7@blackstackhub.com'
    smtp_password = 'password1'

    # Email content
    subject = 'Test Email'
    body = 'This is a test email sent using Python.'

    # Constructing the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach body to the email
    message.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    server = None
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)  # Start TLS encryption
        # Login to the SMTP server using SMTP authentication
        server.login(smtp_username, smtp_password)
        # Send email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print('Email sent successfully!')
    except smtplib.SMTPException as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        if server:
            # Close the connection to the SMTP server
            server.quit()

if __name__ == '__main__':
    send_email()
