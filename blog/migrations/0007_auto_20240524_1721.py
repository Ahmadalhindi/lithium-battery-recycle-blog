# Generated by Django 3.2.23 on 2024-05-24 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
