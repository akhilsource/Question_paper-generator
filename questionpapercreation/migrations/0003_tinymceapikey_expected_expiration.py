# Generated by Django 5.0.1 on 2024-04-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionpapercreation', '0002_tinymceapikey'),
    ]

    operations = [
        migrations.AddField(
            model_name='tinymceapikey',
            name='expected_expiration',
            field=models.DateField(blank=True, null=True),
        ),
    ]
