# Generated by Django 5.1.7 on 2025-03-30 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0001_initial'),
        ('diary', '0002_remove_enrolment_class_title_remove_enrolment_user_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='eventclass',
            name='unique_class_title_case_insensitive',
        ),
        migrations.AddConstraint(
            model_name='eventclass',
            constraint=models.UniqueConstraint(fields=('event_day', 'start_time'), name='unique_class_title_case_insensitive'),
        ),
    ]
