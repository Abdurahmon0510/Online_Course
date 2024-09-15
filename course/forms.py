from django import forms
from .models import Course, Category, Comment, Request


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'image', 'category', 'quantity', 'favourite']

class CategoryForm(forms.ModelForm):
     class Meta:
         model = Category
         fields = ['title', 'slug']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'rating', 'image', 'blog', 'video', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['blog'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name', 'email', 'subject', 'message']