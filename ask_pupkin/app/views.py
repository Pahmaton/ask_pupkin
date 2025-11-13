from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Tag


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

# cписок новых вопросов (главная страница) (URL = /)
def questions(request):
    qs = Question.objects.new().select_related('author__user').prefetch_related('tags')
    page = paginate(qs, request, per_page=20)
    return render(request, "questions.html", {"questions": page.object_list, "page_obj": page, "question_type": "new"})


# список “лучших” вопросов (URL = /hot/)
def hot_questions(request):
    qs = Question.objects.hot().select_related('author__user').prefetch_related('tags')
    page = paginate(qs, request, per_page=20)
    return render(request, "questions.html", {"questions": page.object_list, "page_obj": page, "question_type": "hot"})


# список вопросов по тэгу (URL = /tag/<tag>/)
def questions_by_tag(request, tag):
    tag_obj = get_object_or_404(Tag, name=tag)
    qs = tag_obj.questions.all().select_related('author__user').prefetch_related('tags')
    page = paginate(qs, request, per_page=20)
    return render(request, "questions_by_tag.html", {"questions": page.object_list, "page_obj": page, "tag": tag_obj})


# страница одного вопроса со списком ответов (URL = /question/<id>/)
def question(request, question_id):
    q = get_object_or_404(Question.objects.select_related('author__user').prefetch_related('tags', 'answers__author__user'), pk=question_id)
    answers_page = paginate(q.answers.all().order_by('created_at'), request, per_page=30)
    return render(request, "question.html", {"question": q, "answers": answers_page.object_list, "page_obj": answers_page})

# форма входа
def login_form(request):
    return render(request, "login.html")

# форма регистрации (URL = /signup/)
def register_form(request):
    return render(request, "register.html")

# форма создания вопроса (URL = /ask/)
def add_question_form(request):
    return render(request, "add_question.html")

# форма профиля
def profile_form(request):
    return render(request, "profile.html")
