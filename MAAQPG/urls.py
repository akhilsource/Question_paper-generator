"""
URL configuration for MAAQPG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Login_signupApp import views
from questionpapercreation.views import question_paper_preview,create_question_paper,automatic_view,question_papers,notesgeneration,apihelp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view,name='login_signup'),
    path('forgetpassword', views.forgetpass_view,name='forgetpass_view'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('preview/<int:question_paper_id>/', question_paper_preview,name='preview'),
    
    path('create/',create_question_paper,name='create'),
    path('automatic/',automatic_view,name='automatic'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('question_papers/',question_papers, name='question_papers'),
    path('notesgeneration/',notesgeneration, name='notesgeneration'),
    path('apihelp/',apihelp, name='apihelp'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
