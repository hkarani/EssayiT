# Generated by Django 4.0.7 on 2022-10-17 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0004_alter_userverificationdetails_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverificationdetails',
            name='email',
            field=models.EmailField(blank=True, default='empty', max_length=256),
        ),
    ]
