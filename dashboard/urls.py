from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
