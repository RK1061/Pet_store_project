# Generated by Django 5.2 on 2025-04-21 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petstoreapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
