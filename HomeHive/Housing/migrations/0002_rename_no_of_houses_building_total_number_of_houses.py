# Generated by Django 5.0.3 on 2024-03-19 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Housing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='no_of_houses',
            new_name='total_number_of_houses',
        ),
    ]
