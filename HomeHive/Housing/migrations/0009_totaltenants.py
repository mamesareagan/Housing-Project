# Generated by Django 5.0.3 on 2024-03-27 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Housing', '0008_tenant_house_number_alter_tenant_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalTenants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_count', models.PositiveIntegerField(default=0)),
                ('building', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Housing.building')),
            ],
        ),
    ]
