# Generated by Django 5.0.7 on 2024-08-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert_job', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('studies_degree', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=255)),
            ],
        ),
    ]
