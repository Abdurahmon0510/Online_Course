from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Course, Comment, Video, Blog


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Slug maydonini avto-tayyorlash
    fields = ['name', 'price', 'category', 'description', 'image', 'favourite', 'slug']
    list_display = ['name', 'price', 'category', 'description', 'image']
    # exclude = ('slug',)  # Exclude qilmaslik kerak, chunki biz slugni generatsiya qilamiz


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ['title', 'slug','image']
    list_display = ['title', 'slug','image']



@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('user',)}
    fields = ['user', 'message', 'video', 'slug','rating', 'image','blog']
    list_display = ['user', 'message', 'video']



@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'duration', 'file', 'course', 'slug']
    list_display = ['name', 'duration', 'file', 'course']

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ['title', 'content', 'image', 'author', 'slug','category','is_published','author_bio','author_name','author_image']
    list_display = ['title', 'author', 'slug', 'category', 'is_published']



