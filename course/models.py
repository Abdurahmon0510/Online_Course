from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ['-id']

class Course(BaseModel):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='course', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    favourite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Video(BaseModel):
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    file = models.FileField(upload_to='course', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    message = models.TextField(null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(max_length=100, null=True, blank=True)

    def get_user(self):
        return self.user

class Attribute(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class AttributeValue(BaseModel):
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.value

class CourseAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attributes')
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='values')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attributes')
