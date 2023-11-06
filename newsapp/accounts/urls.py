from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('login/manager/', views.manager_login, name='manager_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('save_interests/', views.save_interests, name='save_interests'),
    path('profile/<int:userid>', views.user_profile, name='user_profile'),
    path('save_interests/', views.save_interests, name='save_interests'),
    path('edit_profile/<int:userid>', views.edit_profile, name='edit_profile'),
]

