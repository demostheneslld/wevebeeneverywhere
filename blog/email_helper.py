from django.core.mail import EmailMessage

def send_email(recipient, subject, body):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='no-reply@wevebeeneverywhere.com',
        to=[recipient]
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)
