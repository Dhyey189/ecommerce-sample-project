# Generated by Django 4.1.2 on 2022-12-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='Aa@1Bb*2', max_length=50),
        ),
    ]
