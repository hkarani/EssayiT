from django.db import models

class UserVerificationDetails(models.Model):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    email = models.CharField(max_length=256)
    verification_code = models.PositiveBigIntegerField()
    verification_status = models.BooleanField(default=False)
    email_entry_attempts = models.PositiveBigIntegerField(default=0)
    code_verification_attempts = models.PositiveBigIntegerField(default=0)
    
    
    @classmethod
    def create_user_verification_details():
        pass
    
    @classmethod
    def get_user_verification_details_by_user_id():
        pass
    
    def check_email_entry_attempts():
        pass
    
    def get_verification_code():
        pass
    
    def check_verification_attempts():
        pass
    
    def generate_verification_code():
        pass
    
    def block_user():
        pass
    
    
    
    