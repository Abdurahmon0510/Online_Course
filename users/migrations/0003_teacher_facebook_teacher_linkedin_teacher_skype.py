# Generated by Django 5.1.1 on 2024-09-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='skype',
            field=models.URLField(blank=True, null=True),
        ),
    ]
