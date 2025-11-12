from random import randint

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = []
for i in range(30):
    QUESTIONS.append({
        'title': f'How to build moon park {i}?',
        'id': i,
        'text': f'guys, i have trouble... I cant build moon park {i}',
        'tags': ['black-jack', 'bender'],
        'answers': [f'you can build moon park {i} with {k} friends' for k in range(randint(0,3))]
    })

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
    page = paginate(QUESTIONS, request, 20)
    return render(request, "questions.html", {
        "questions": QUESTIONS, 
        "question_type": "new",
        "page_obj": page
    })

# cписок “лучших” вопросов (URL = /hot/)
def hot_questions(request):
    sorted_questions = sorted(
        QUESTIONS, 
        key=lambda q: len(q['answers']), 
        reverse=True
    )
    page = paginate(sorted_questions, request, 20)
    return render(request, "questions.html", {
        "questions": page,
        "question_type": "hot",
        "page_obj": page,
    })

# cписок вопросов по тэгу (URL = /tag/blablabla/)
def questions_by_tag(request, tag):
    filtered_questions = [q for q in QUESTIONS if tag in q['tags']]
    page = paginate(filtered_questions, request, 20)
    return render(request, "questions_by_tag.html", {
        "questions": page,
        "tag": tag,
        "page_obj": page,
    })

# cтраница одного вопроса со списком ответов (URL = /question/35/)
def question(request, question_id):
    question_obj = QUESTIONS[question_id]
    
    answers_page = paginate(question_obj['answers'], request, 30)
    return render(request, "question.html", {
        "question": question_obj,
        "answers": answers_page,
        "page_obj": answers_page,
    })

# форма логина (URL = /login/)
def login_form(request):
    return render(request, "login.html")

# форма регистрации (URL = /signup/)
def register_form(request):
    return render(request, "register.html")

# форма создания вопроса (URL = /ask/)
def add_question_form(request):
    return render(request, "add_question.html")
