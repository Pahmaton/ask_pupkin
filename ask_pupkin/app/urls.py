from django.urls import path
from app import views

urlpatterns = [
    path('', views.questions, name="questions"),
    path('hot/', views.hot_questions, name="hot_questions"),
    path('tag/<str:tag>/', views.questions_by_tag, name="questions_by_tag")
]
