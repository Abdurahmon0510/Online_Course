# Generated by Django 5.1.1 on 2024-09-15 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_alter_video_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='author_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
