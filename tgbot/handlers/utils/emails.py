# How To Validate An Email Address In Python
# Using "re" package
import re
from django.conf import settings
from django.core.mail import send_mail

      
def check_if_correct_code():
    pass

def get_user_verifiction_details():
    pass

def send_email(email):
    subject = 'Essayit bot registration'
    message = 'Your code is 3303'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_email(subject,message,email_from, recipient_list)
    print("Email sent!")

def ban_user():
    pass