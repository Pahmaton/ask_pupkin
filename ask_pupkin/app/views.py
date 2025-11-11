from random import randint
from django.shortcuts import render

QUESTIONS = []
for i in range(30):
    QUESTIONS.append({
        'title': f'How to build moon park {i}?',
        'id': i,
        'text': f'guys, i have trouble... I cant build moon park {i}',
        'tags': ['black-jack', 'bender'],
        'answers': [f'you can build moon park {i} with {k} friends' for k in range(randint(0,3))]
    })

# cписок новых вопросов (главная страница) (URL = /)
def questions(request):
    return render(request, "questions.html", {
        "questions": QUESTIONS, 
        "question_type": "new"
    })

# cписок “лучших” вопросов (URL = /hot/)
def hot_questions(request):
    return render(request, "questions.html", {
        "questions": sorted(
            QUESTIONS, 
            key=lambda q: len(q['answers']), 
            reverse=True
        ),
        "question_type": "hot"
    })

# cписок вопросов по тэгу (URL = /tag/blablabla/)
def questions_by_tag(request, tag):
    return render(request, "questions_by_tag.html", {
        "questions": [q for q in QUESTIONS if tag in q['tags']],
        "tag": tag
    })

# cтраница одного вопроса со списком ответов (URL = /question/35/)
def question(request, question_id):
    return render(request, "question.html", {"question": QUESTIONS[question_id]})

# форма логина (URL = /login/)
def login_form(request):
    return render(request, "login.html")
# TODO форма регистрации (URL = /signup/)
# TODO форма создания вопроса (URL = /ask/)
