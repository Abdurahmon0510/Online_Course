import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from config import settings
from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import RegisterForm, SendingEmailForm, SignupForm
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import FormView, CreateView, View
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import Customer
from .tokens import AccountTokenGenerator

logger = logging.getLogger(__name__)


class LoginPage(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        try:
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=self.request, username=email, password=password)
            if user is not None:
                auth_login(self.request, user)
                messages.success(self.request, 'Login successful')
            else:
                messages.error(self.request, 'Invalid email or password')
                return self.form_invalid(form)
        except Exception as e:
            logger.error(f'An error occurred during login: {str(e)}')
            messages.error(self.request, 'An error occurred during login')
            return self.form_invalid(form)
        return super().form_valid(form)


class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/course/index/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'protocol': 'http',
            'domain': 'example.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': AccountTokenGenerator.make_token(user),
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


class LogoutPage(LogoutView):
    next_page = reverse_lazy('index')


class SendingEmail(View):
    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        return render(request, 'users/send-email.html', {'form': form, 'sent': False})

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']

            send_mail(
                subject,
                message,
                EMAIL_DEFAULT_SENDER,
                recipient_list,
                fail_silently=False
            )
            return render(request, 'users/send-email.html', {'form': form, 'sent': True})

        return render(request, 'users/send-email.html', {'form': form, 'sent': False})


#
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and AccountTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return render(request, 'users/register.html')

class Signup(LoginRequiredMixin, FormView):
    form_class = SignupForm
    template_name = 'course/index.html'
    success_url = reverse_lazy('blog')
    def form_valid(self, form):
        course = form.cleaned_data['course']
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        customer.purchased_courses.add(course)
        return super().form_valid(form)

