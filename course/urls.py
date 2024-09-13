from django.urls import path

from course import views

urlpatterns = [
    path('teachers/', views.TeacherView.as_view(), name='teacher'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('courses/', views.CourseView.as_view(), name='courses'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('single/', views.SingleView.as_view(), name='single'),
    ]