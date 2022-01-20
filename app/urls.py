from django.urls import path
from .views import profile , delPost, register, newsfeed
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import  static 
from django.conf import settings


urlpatterns = [
    path('', newsfeed, name="home"),
    path('register', register, name="register"),
    path('login', LoginView.as_view(template_name='twitter/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delPost/<int:pk>/', delPost, name='delPost' ),
    path('profile/<str:username>/', profile, name='profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)