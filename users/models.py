from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.text import slugify

from config import settings
from course.models import Course
from .managers import MyUserManager
from django.contrib.auth.models import PermissionsMixin


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    course = models.ManyToManyField(Course, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    skype = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def joined(self):
        return self.created_at.strftime('%d/%m/%Y')

    @property
    def image_url(self):
        if self.image:
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name)
            slug = base_slug
            num = 1
            while Teacher.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{num}'
                num += 1
            self.slug = slug
        super(Teacher, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        unique_together = (('first_name', 'last_name'),)
        ordering = ('first_name', 'last_name', 'phone')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def get_name(self):
        if self.username:
            return self.username
        return self.email.split('@')[0]

    def __str__(self):
        return self.email


class Customer(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    purchased_courses = models.ManyToManyField(Course, related_name='purchased_by')

    def __str__(self):
        return self.purchased_courses.__str__()
