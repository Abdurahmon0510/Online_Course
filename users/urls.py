from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    path('send-email/', views.SendingEmail.as_view(), name='sending_email'),
    path('activation-link/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('signup/', views.Signup.as_view(), name='signup'),
]
