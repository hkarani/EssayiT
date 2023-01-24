from email.policy import default
from django.db import models
from django.db.models import F
from typing import Union


# Create your models here.


class UserVerificationDetails(models.Model):
    class Types(models.TextChoices):
        WRITER = "WRITER", "Writer"
        CLIENT = "CLIENT", "Client"
        UNVERIFIED = "UNVERIFIED", "Unverified"
        FIRST_TIME_USER = "FIRST_TIME_USER", "First_time_user"
        
    user_id = models.PositiveBigIntegerField(primary_key=True)
    email = models.CharField( max_length=256, blank=True, default='empty', null=True)
    user_type = models.CharField(max_length=50, choices=Types.choices, default=Types.FIRST_TIME_USER)
    verification_code = models.PositiveBigIntegerField(default=0, null=True)
    verification_status = models.BooleanField(default=False, blank=True)
    email_entry_attempts = models.PositiveBigIntegerField(default=0)
    code_verification_attempts = models.PositiveBigIntegerField(default=0)
    
    def __str__(self) -> str:
         return f'{self.user_id}'
    
    @classmethod
    def create_user_verification_details(cls, user_id, **kwargs ):
        """
            Create user details in UserVerificationDetails
            Includes user_id as primary key
            Only saves email that is valid else email is left as None           
        """
        email = kwargs.get('email')
        verification_code = kwargs.get('verification_code')
        user_type = kwargs.get('user_type')
        cls.objects.update_or_create(user_id=user_id, defaults={
            'email': email,
            'verification_code': verification_code
        })
    
    @classmethod
    def get_user_verification_details_by_user_id(cls, user_id: Union[str, int]):
        return cls.objects.filter(user_id=int(user_id)).first()
    
    @classmethod
    def get_email_entry_attempts(cls, user_id):
        return  cls.objects.get(user_id=int(user_id)).email_entry_attempts
    
    @classmethod
    def get_code_verification_attempts(cls, user_id):
        return  cls.objects.get(user_id=int(user_id)).code_verification_attempts
        
    
    @classmethod
    def get_verification_code(cls, user_id):
        try:
            return  cls.objects.get(user_id=int(user_id)).verification_code
        except cls.DoesNotExist:
            return
         
    @classmethod
    def check_if_email_is_taken(cls, user_id ,email):
        if cls.objects.filter(email=email).exists():
            user_email = cls.get_user_email_by_id(user_id)
            if (user_email == email):
                return False
            return True        
        return False        
     
     
    @classmethod
    def get_user_email_by_id(cls, user_id):
        return  cls.objects.get(user_id=int(user_id)).email
    
    @classmethod
    def increment_code_attempts(cls, user_id):
        user_details = cls.objects.get(user_id=user_id)
        user_details.code_verification_attempts += 1
        user_details.save()
    
    @classmethod
    def get_user_type(cls, user_id):
        try:
            return  cls.objects.get(user_id=int(user_id)).user_type
        except cls.DoesNotExist:
            return None
  
    
    @classmethod
    def update_user_type(cls, user_id, user_type):
        user_details = cls.objects.get(user_id=user_id)
        user_details.user_type = cls.Types[user_type]
        user_details.save()
        
    @classmethod   
    def update_verifcation_code(cls, user_id, new_verfication_code):
        user_details = cls.objects.get(user_id=user_id)
        user_details.verification_code = new_verfication_code
        user_details.save()
    
    @classmethod
    def increment_email_attempts(cls, user_id):
        user_details = cls.objects.get(user_id=user_id)
        user_details.email_entry_attempts += 1
        user_details.save()
    
    
    
    
    