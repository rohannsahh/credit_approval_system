# Generated by Django 5.1.3 on 2024-11-15 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
    ]