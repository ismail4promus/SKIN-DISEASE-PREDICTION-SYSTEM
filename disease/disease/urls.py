from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('account/', include('account.urls')),
    path('dashboard', views.dashboard, name='dashboard'),
    path('adminarea', views.adminarea, name='adminarea'),
    path('reports', views.reports, name='reports'),
    path('edit-report/<int:id>', views.editreport, name='editreport'),
    path('<int:id>', views.details, name='details'),
    path('userdetails/<int:id>', views.userdetails, name='userdetails'),
    path('logout/', views.LogoutUser, name='logout'),
    path('profile', views.Profile, name='profile'),
    path('disease', include('diagnose.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
