from django.urls import path


from course import views
from course.views import CourseVideosView, VideoDetailView, CourseView

urlpatterns = [
    path('teachers/', views.TeacherView.as_view(), name='teacher'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/<slug:slug>/', CourseView.as_view(), name='courses_with_slug'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('single/<int:id>/', views.SingleView.as_view(), name='single'),
    path('videos/<slug:slug>/', CourseVideosView.as_view(), name='course_videos'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    ]