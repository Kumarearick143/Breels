from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Optional
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Place this BEFORE the dynamic route
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('profile/<str:username>/counts/', views.profile_counts, name='profile_counts'),
]

