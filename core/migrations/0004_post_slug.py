# Generated by Django 4.2.2 on 2024-03-01 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='nill', max_length=255),
        ),
    ]
