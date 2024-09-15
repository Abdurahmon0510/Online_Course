from django import forms
from .models import Course, Category


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'image', 'category', 'quantity', 'favourite']

class CategoryForm(forms.ModelForm):
     class Meta:
         model = Category
         fields = ['title', 'slug']

