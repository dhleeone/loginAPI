from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('verification', PhoneVerify.as_view()),
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('profile', UserProfile.as_view()),
    path('reset-password', ResetPassword.as_view()),
]