import os
import json
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from config.settings import BASE_DIR, EMAIL_DEFAULT_SENDER
from .models import Teacher, User


def pre_save_users(sender, instance, *args, **kwargs):
    print('Before saving users or user')


pre_save.connect(pre_save_users, sender=Teacher)
pre_save.connect(pre_save_users, sender=User)


@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=User)
def post_save_author(sender, instance, created, *args, **kwargs):
    if created:
        print('After saving Teacher or user')
        subject = 'Update Teacher or user'
        message = 'successfully saved Teacher or user'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in User.objects.all()]

        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
                  fail_silently=False)


@receiver(post_delete, sender=Teacher)
@receiver(post_delete, sender=User)
def save_deleted_instance(sender, instance, *args, **kwargs):
    global filename, new_data
    if sender == Teacher:
        filename = os.path.join(BASE_DIR, 'users/Teacher_data', 'Teacher.json')
        new_data = {
            'id': instance.id,
            'full_name': instance.full_name,
            'email': instance.email,
            'phone': instance.phone,
            'slug': instance.slug,
        }
    elif sender == User:
        filename = os.path.join(BASE_DIR, 'users/user_data', 'User.json')
        new_data = {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'password': instance.password,
        }

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)

    with open(filename, 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

        data.append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
