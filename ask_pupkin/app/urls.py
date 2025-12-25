from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views

urlpatterns = [
    path('', views.questions, name="questions"),
    path('hot/', views.hot_questions, name="hot_questions"),
    path('tag/<str:tag>/', views.questions_by_tag, name="questions_by_tag"),
    path('question/<int:question_id>', views.question_view, name="question"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="register"),
    path('ask/', views.add_question_view, name="add_question"),
    path('profile/edit/', views.profile_edit, name="profile"),
    path('best_member/<str:username>', views.best_members, name="best_member"),
    path('logout/', views.logout_view, name="logout"),
    path('vote/', views.vote, name='vote'),
    path('mark_correct/', views.mark_correct, name='mark_correct'),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
