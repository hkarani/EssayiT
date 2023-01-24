
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
import re


def send_verfication_email(email):
    # subject = 'Essayit bot registration'
    # message = 'Your code is 3303'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [email,]
    # send_mail(subject,message,email_from, recipient_list)
    print("Email sent!")
  
def email_regex_check(email):  
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if(re.search(email_regex,email)):   
        return True  
    else:   
        return False
    
def code_regex_check(code):  
    code_regex = '\d{5}' 
    if(re.match(code_regex,code)):   
        return True
    else:   
        return False


def block_user():
        pass
    
def generate_five_digit_code():
    five_digit_code = randrange(10000, 99999)
    return five_digit_code