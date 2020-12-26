from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


class acccount_exception(Exception):
    """[summary]
        Custom exception.
    Args:
        Exception ([Class]): [Exception]
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message