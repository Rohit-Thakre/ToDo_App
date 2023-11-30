from django.urls import path
from main import views

urlpatterns = [
    
    path('' , views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('log_out/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    path('remove_task/<int:id>/', views.remove_task, name='remove_task'),

    path('create_task/', views.create_task, name='create_task'),
    path('create_task/<int:id>/', views.create_task, name='create_task'),
    
]