# Generated by Django 4.0.7 on 2022-10-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0002_alter_userverificationdetails_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverificationdetails',
            name='email',
            field=models.CharField(default=None, max_length=256),
        ),
    ]
