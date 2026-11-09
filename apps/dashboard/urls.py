from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home & Auth
    path('', views.dashboard_home, name='home'),
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),

    # Projects
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/toggle-featured/', views.project_toggle_featured, name='project_toggle_featured'),

    # Blog Posts
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('blog/<int:pk>/toggle-publish/', views.blog_toggle_publish, name='blog_toggle_publish'),

    # Skills
    path('skills/', views.skills_list, name='skills_list'),
    path('skills/new/', views.skill_create, name='skill_create'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),

    # Experience & Education
    path('experiences/', views.experience_list, name='experience_list'),
    path('experiences/new/', views.experience_create, name='experience_create'),
    path('experiences/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experiences/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    path('education/new/', views.education_create, name='education_create'),
    path('education/<int:pk>/edit/', views.education_edit, name='education_edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),

    # Contact Messages Inbox
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/toggle-read/', views.message_toggle_read, name='message_toggle_read'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),

    # Site Settings
    path('settings/', views.site_settings_edit, name='site_settings_edit'),
]
