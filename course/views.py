from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from course.models import Course, Category
from users.models import Teacher


class TeacherView(View):

    def get(self, request):
        teachers = Teacher.objects.all()
        paginator = Paginator(teachers, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'teacher': page_obj}
        return render(request, 'users/teacher.html', context)
class CourseView(View):
    def get(self, request):
        courses = Course.objects.all()
        paginator = Paginator(courses, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'course': page_obj}
        return render(request, 'course/courses.html', context)
class IndexView(View):
      def get(self, request):
          courses = Course.objects.all()
          categories = Category.objects.all()
          paginator = Paginator(courses, 4)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)
          context = {'course': page_obj, 'categories': categories}
          return render(request, 'course/index.html', context)
class AboutView(View):
      def get(self, request):

          return render(request, 'course/about.html')
class BlogView(View):
      def get(self, request):
          categories = Category.objects.all()
          return render(request,'course/about.html',{'categories':categories})
class ContactView(View):
      def get(self, request):
         return render(request, 'course/contact.html')
class SingleView(View):
      def get(self, request):

          return render(request, 'course/single.html')


