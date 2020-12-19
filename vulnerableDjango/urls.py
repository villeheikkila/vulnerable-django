from .views import SignUpView, homeView, SignUpView, addMessageView
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add/', addMessageView, name='add'),
    path('', homeView, name='home'),
]
