from django.urls import path
from app.views import questions

urlpatterns = [
    path('', questions, name="questions")
]
