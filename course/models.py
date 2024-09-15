from django.db import models
from django.db.models import Avg, Sum
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.contrib.auth.models import User
from config import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/',default='course/img/cat-1.jpg')
    slug = models.SlugField(max_length=100,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ['-id']

class Course(BaseModel):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='course/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,related_name='course')
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    favourite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def average_rating(self):
        videos = self.videos.all()
        avg_rating = videos.aggregate(Avg('comments__rating'))['comments__rating__avg']
        return avg_rating if avg_rating is not None else 0

    def get_total_duration(self):

        total_duration = self.videos.aggregate(Sum('duration'))['duration__sum'] or 0
        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours}h {minutes}m {seconds}s" if total_duration > 0 else "No videos"

    def __str__(self):
        return self.name

class Video(BaseModel):
      name = models.CharField(max_length=100)
      duration = models.PositiveIntegerField(null=True, blank=True)
      file = models.FileField(upload_to='course', blank=True, null=True)
      course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE, null=True, blank=True)
      slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

      def save(self, *args, **kwargs):
          if not self.slug:
              self.slug = slugify(self.name)
          if self.file:
              video = VideoFileClip(self.file.path)
              duration_in_seconds = int(video.duration)
              self.duration = duration_in_seconds
              video.close()
              super(Video, self).save(*args, **kwargs)


      @property
      def convert_duration(self):
        seconds = self.duration

        days = seconds // 86400
        seconds %= 86400

        hours = seconds // 3600
        seconds %= 3600

        minutes = seconds // 60
        seconds %= 60


        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"



      @property
      def average_rating(self):
        avg_rating = self.comments.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0


class Blog(BaseModel):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    author_bio = models.TextField(null=True, blank=True)
    author_name = models.TextField(null=True, blank=True)
    author_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    message = models.TextField(null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments',null=True,blank=True)
    user = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero)
    image = models.ImageField(upload_to='comments/', blank=True, null=True)
    blog = models.ForeignKey(Blog,parent_link='comment', on_delete=models.CASCADE, null=True, blank=True)

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
