from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project-list'),
    path('create/', views.project_create, name='project-create'),
    path('<int:pk>/detail/', views.project_detail, name='project-detail'),
    path('<int:pk>/update/', views.project_update, name='project-update'),
    path('<int:pk>/delete/', views.project_delete, name='project-delete'),
]