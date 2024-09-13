from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Course, Comment


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = ['name', 'price', 'category', 'description', 'image', 'favourite']
    list_display = ['name', 'price', 'category', 'description', 'image']

    exclude = ('slug',)


admin.site.register(Category)
admin.site.register(Comment)
