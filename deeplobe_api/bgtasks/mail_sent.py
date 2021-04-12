from django.conf import settings
from django.core.mail import EmailMessage

def mail_sending(to_email, subject, body):

    email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [to_email])
    email.content_subtype = "html"
    email.send()