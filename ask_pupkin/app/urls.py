from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views

urlpatterns = [
    path('', views.questions, name="questions"),
    path('hot/', views.hot_questions, name="hot_questions"),
    path('tag/<str:tag>/', views.questions_by_tag, name="questions_by_tag"),
    path('question/<int:question_id>', views.question, name="question"),
    path('login/', views.login_form, name="login"),
    path('signup/', views.register_form, name="register"),
    path('ask/', views.add_question_form, name="add_question"),
    path('profile/', views.profile_form, name="profile")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
