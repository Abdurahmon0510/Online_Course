# Generated by Django 5.1.1 on 2024-09-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=100),
        ),
    ]
