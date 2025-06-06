from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list/', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('toggle/<int:pk>/', views.task_toggle_complete, name='task_toggle'),
]