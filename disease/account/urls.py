from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login, name='login'),
    path('forgot', views.forgot, name='forgot'),
    path('resetpassword/<int:id>', views.resetpassword, name='resetpassword'),
    path('register', views.Register, name='register'),
    path('activate/<uidb64>/<token>', views.Activate, name='activate'),
]
