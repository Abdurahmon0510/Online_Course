from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from course.models import Course, Category, Comment, Blog, Video
from users.models import Teacher

from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import CommentForm
from .models import Category, Course


class BaseView(View):
    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        category1 = get_object_or_404(Category, slug=kwargs.get('slug'))
        courses = category1.course.all()

        return render(request, 'course/base/base.html', {
            'categories': categories,
            'courses': courses,
            'category1': category1
        })


class TeacherView(View):

    def get(self, request):
        teachers = Teacher.objects.all()
        categories = Category.objects.all()
        courses = Course.objects.all()
        context = {'teachers':teachers,'categories':categories,'courses':courses}
        return render(request, 'users/teacher.html', context)


class CourseView(View):
    def get(self, request, slug=None):
        if slug:
            category = get_object_or_404(Category, slug=slug)
            courses = Course.objects.filter(category=category).annotate(comment_count=Count('videos__comments'))
        else:
            courses = Course.objects.all().annotate(comment_count=Count('videos__comments'))

        comments = Comment.objects.all()
        categories = Category.objects.annotate(course_count=Count('course'))

        context = {'courses': courses, 'categories': categories, 'comments': comments}
        return render(request, 'course/courses.html', context)

class IndexView(View):
    def get(self, request):
        category_slug = request.GET.get('slug')

        if category_slug:

            category = get_object_or_404(Category, slug=category_slug)
            courses = Course.objects.filter(category=category).annotate(comment_count=Count('videos__comments'))
        else:

            courses = Course.objects.all().annotate(comment_count=Count('videos__comments'))


        blogs = Blog.objects.all()
        comments = Comment.objects.all()
        teachers = Teacher.objects.all()
        categories = Category.objects.all()
        categories_with_course_count = Category.objects.annotate(course_count=Count('course'))

        context = {
            'courses': courses,
            'categories': categories,
            'categories_with_course_count': categories_with_course_count,
            'teachers': teachers,
            'comments': comments,
            'blogs': blogs
        }

        return render(request, 'course/index.html', context)

class CourseVideosView(ListView):
    model = Video
    template_name = 'course/course_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        course = Course.objects.get(slug=self.kwargs['slug'])
        return course.videos.all()

class VideoDetailView(DetailView):
    model = Video
    template_name = 'course/video_detail.html'
    context_object_name = 'video'


class AboutView(View):
      def get(self, request):
          comments = Comment.objects.all()
          courses = Course.objects.all()
          categories = Category.objects.all()
          context = {'comments': comments, 'courses': courses, 'categories': categories}
          return render(request, 'course/about.html',context)
class BlogView(View):
      def get(self, request):
          categories_with_course_count = Category.objects.annotate(course_count=Count('course'))
          blogs = Blog.objects.all().order_by('-updated_at')
          categories = Category.objects.all()
          paginator = Paginator(blogs, 2)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          return render(request,'course/blog.html',{'categories':categories,'blogs':page_obj,'categories_with_course_count':categories_with_course_count})
class ContactView(View):
      def get(self, request):
         return render(request, 'course/contact.html')


class SingleView(View):
    def get(self, request, id):
        categories_with_course_count = Category.objects.annotate(course_count=Count('course'))
        blog = get_object_or_404(Blog, id=id)
        comments = Comment.objects.filter(blog=blog)
        courses = Course.objects.all()
        blogs = Blog.objects.annotate(comment_counts=Count('comment')).order_by('-updated_at')
        categories = Category.objects.all()
        total_comments_count = Comment.objects.aggregate(total=Count('id'))['total']
        comment_form = CommentForm()
        videos = Video.objects.all()

        context = {
            'blog': blog,
            'comments': comments,
            'courses': courses,
            'blogs': blogs,
            'categories': categories,
            'total_comments_count': total_comments_count,
            'categories_with_course_count': categories_with_course_count,
            'comment_form': comment_form,
            'videos': videos
        }

        return render(request, 'course/single.html', context)

    def post(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        comment_form = CommentForm(request.POST, request.FILES)
        videos = Video.objects.all()
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect('single', id=blog.id)


        categories_with_course_count = Category.objects.annotate(course_count=Count('course'))
        comments = Comment.objects.filter(blog=blog)
        courses = Course.objects.all()
        blogs = Blog.objects.annotate(comment_counts=Count('comment')).order_by('-updated_at')
        categories = Category.objects.all()
        total_comments_count = Comment.objects.aggregate(total=Count('id'))['total']

        context = {
            'blog': blog,
            'comments': comments,
            'courses': courses,
            'blogs': blogs,
            'categories': categories,
            'total_comments_count': total_comments_count,
            'categories_with_course_count': categories_with_course_count,
            'comment_form': comment_form,
            'videos': videos
        }

        return render(request, 'course/single.html', context)