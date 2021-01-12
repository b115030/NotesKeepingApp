# from django.core.mail import EmailMessage
# import threading
# from celery import shared_task


# class EmailThread(threading.Thread):
#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):

#         self.email.send() 


# @shared_task
# def send_email(data):
    
#     email = EmailMessage(
#         subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
#     EmailThread(email).start()  


from celery import shared_task
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail, mail_admins
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings


@shared_task
def send_activation_mail(user_id, context):

    user = User.objects.get(id=user_id)

    context.update({
        'username': user.username,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    subject = render_to_string('djangobin/email/activation_subject.txt', context)
    email = render_to_string('djangobin/email/activation_email.txt', context)

    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])