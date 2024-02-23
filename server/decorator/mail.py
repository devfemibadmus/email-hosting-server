from functools import wraps
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..models import VirtualDomain, VirtualUser
import imaplib, smtplib, email, ssl, hashlib, re


def send_email(sender_email, recipient_email, smtp_password, subject, body):
    smtp_server = 'mail.blackstackhub.com'
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    server = None
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        return 'Email sent successfully!'
    except smtplib.SMTPException as e:
        return f'Error: {e}'
    except Exception as e:
        return 'Unexpected error try again!'
    finally:
        if server:
            server.quit()
def connect_imap(domain, email, password):
    imap_server = 'mail.blackstackhub.com'
    imap_port = 993

    context = ssl.create_default_context()
    imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port, context=context)
    imap_conn.login(email, password)
    imap_conn.select(mailbox=domain)
    return imap_conn

def fetch_emails(imap_conn, search_criteria='ALL'):
    _, email_numbers = imap_conn.search(None, search_criteria)
    email_list = []
    for num in email_numbers[0].split():
        _, email_data = imap_conn.fetch(num, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        email_list.append({
            'subject': email_message['subject'],
            'from': email_message['from'],
            'to': email_message['to'],
            'date': email_message['date'],
            'body': get_email_body(email_message),
        })
    return email_list

def get_email_body(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return email_message.get_payload(decode=True).decode()

def extract_domain(email):
    parts = email.split('@')
    if len(parts) != 2:
        return email
    return parts[1]

def extract_action_and_params(request):
    action = request.GET.get("action") or request.POST.get("action")
    mail_pk = request.GET.get("mail_pk") or request.POST.get("mail_pk")
    sender = request.GET.get("sender") or request.POST.get("sender")
    return action, mail_pk, sender

def create_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            mail_info = {
                'body': request.POST.get("body"),
                'subject': request.POST.get("subject"),
                'from': request.POST.get("from"),
                'to': request.POST.get("to")
            }
            domain_name = extract_domain(mail_info['from'])
            if VirtualDomain.objects.filter(name=domain_name, user=request.user).exists():
                domain_instance = VirtualDomain.objects.get(name=domain_name)
                if validate_mail_info(mail_info):
                    if validate_email(mail_info['to']):
                        email_account = VirtualUser.objects.filter(email=mail_info['from'], domain__name=domain_name)
                        if email_account.exists():
                            response = send_email(mail_info['from'], mail_info['to'], email_account[0].password, mail_info['subject'], mail_info['body'])
                            if 'sent' in response:
                                messages.success(request, response)
                            else:
                                messages.error(request, response)
                        else:
                            messages.error(request, 'username doesn\'t exist')
                        return view_func(request, *args, **kwargs)
                    else:
                        messages.error(request, 'Invalid recipient email address')
                else:
                    messages.error(request, 'Invalid mail information')
            else:
                messages.error(request, f'Domain "{domain_name}" does not exist or belongs to you')

            return view_func(request, *args, **kwargs)

        return view_func(request, *args, **kwargs)
    return wrapper

def get_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action, mail_pk, sender = extract_action_and_params(request)
        if action == 'get_mail':
            domain_name = extract_domain(sender)
            if VirtualDomain.objects.filter(name=domain_name, user=request.user).exists():
                virtual_user = VirtualUser.objects.get(email=sender)
                imap_conn = connect_imap(domain_name, virtual_user.email, virtual_user.password)
                email_list = fetch_emails(imap_conn)
                return view_func(request, email_list=email_list, *args, **kwargs)
            else:
                messages.error(request, f'You don\'t have access to {domain_name} or the requested mail does not exist')
        return view_func(request, *args, **kwargs)
    return wrapper

def delete_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action, mail_pk, sender = extract_action_and_params(request)
        if action == 'delete_mail':
            domain_name = extract_domain(sender)
            if VirtualDomain.objects.filter(name=domain_name, user=request.user).exists():
                virtual_user = VirtualUser.objects.get(email=sender)
                imap_conn = connect_imap(domain_name, virtual_user.email, virtual_user.password)
                imap_conn.store(mail_pk, '+FLAGS', '\\Deleted')
                imap_conn.expunge()
                messages.success(request, 'Mail deleted successfully')
            else:
                messages.error(request, f'You don\'t have access to {domain_name}')
        return view_func(request, *args, **kwargs)
    return wrapper
