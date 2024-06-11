# Generated by Django 3.2.23 on 2024-06-11 19:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20240524_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
