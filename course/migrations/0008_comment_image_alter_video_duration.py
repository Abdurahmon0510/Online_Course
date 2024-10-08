# Generated by Django 5.1.1 on 2024-09-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_comment_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='comments/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
