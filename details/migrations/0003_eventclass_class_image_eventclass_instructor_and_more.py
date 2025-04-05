# Generated by Django 5.1.7 on 2025-04-05 15:27

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_remove_eventclass_unique_class_title_case_insensitive_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventclass',
            name='class_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_class_image', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='eventclass',
            name='instructor',
            field=models.CharField(default='Instructor', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventclass',
            name='instructor_bio',
            field=models.TextField(default='Instructor Bio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventclass',
            name='instructor_photo',
            field=cloudinary.models.CloudinaryField(blank=True, default='default_instructor_image', max_length=255, null=True, verbose_name='image'),
        ),
    ]
