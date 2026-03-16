
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/export/', views.export_history, name="export_history"),
    path('career/<slug:career_slug>/', views.career_resources, name="career_resources"),
    path('career/comparison/', views.career_comparison, name="career_comparison"),
    path('chatbot/', views.career_chatbot, name="career_chatbot"),
    path('personality/', views.personality_test, name="personality_test"),
    path('resume/', views.resume_analyzer, name="resume_analyzer"),
    path('test/', views.test, name="test"),
]
