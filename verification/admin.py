from django.contrib import admin

from verification.models import UserVerificationDetails

# Register your models here.

class UserVerificationDetailsAdmin(admin.ModelAdmin):
    model = UserVerificationDetails
    list_display = [
        'user_id', 'email', 'user_type', 'verification_code', 'verification_status',
        'email_entry_attempts', 'code_verification_attempts'
    ]
admin.site.register(UserVerificationDetails, UserVerificationDetailsAdmin)