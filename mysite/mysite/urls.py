"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from myapp import views 
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('s_register/', views.student_register, name='s_register'),
    path('t_register/', views.teacher_register, name='t_register'),
    path('teacher_h/',views.teacher_h,name='teacher_h'),
    path('student_h/',views.student_h,name='student_h'),
    path('admin_h/',views.admin_h,name='admin_h'),
    path('delete_s/<int:id>/',views.delete_s,name='delete_s'),
    path('delete_t/<int:id>/',views.delete_t,name='delete_t'),
    path('student_admin/', views.student_admin, name='student_admin'),
    
    path('student_edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student_edit_h/<int:id>/', views.student_edit_h, name='student_edit_h'),


    path('teacher_edit/<int:id>/', views.edit_teacher, name='teacher_edit'),
    path("teacher_h/edit/<int:id>/", views.edit_teacher_h, name="edit_teacher_h"), 

    path('teacher_admin/',views.teacher_admin,name='teacher_admin'),
    path('approve_s/<int:id>/', views.approve_student, name='approve_s'),






        

]
