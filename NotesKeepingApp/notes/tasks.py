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
from django.core.mail import EmailMessage
from datetime import datetime
import pytz
import threading


class EmailThread(threading.Thread):
    """
    Created a class for email threading
    """
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

@shared_task
def send_activation_mail(data):
    """method to send email to respective user

    Args:
        data (string): email details    
    """
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()
@shared_task
def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()

@shared_task
def check_reminder():
    """[checks notes periodically if any note's reminder is set within the current hour.If yes sends an email informing the same.]
    """

    current_time = datetime.datetime.now()
    utc = pytz.UTC
    current_time = utc.localize(current_time)
    logger.debug(current_time)

    for note in Note.objects.exclude(reminder=None).filter(reminder__gt = current_time):
        difference = note.reminder-current_time
        minutes_remaining = (divmod(difference.days * SECONDS_IN_DAY + difference.seconds, MINUTE_CONVERSION_CONSTANT))

        if(minutes_remaining[0] < MINUTES_IN_HOUR):
            user_email = Account.objects.get(email=note.user).email
            data = {'email_body': 'Hi!Reminder for ' + note.title + ' is scheduled within this hour.',
                    'to_email': user_email,
                    'email_subject': 'Reminder for your note'}
            send_email.delay(data)
            logger.debug('sent reminder for '+note.title)