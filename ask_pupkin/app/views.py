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
    return render(request, "questions.html", {"questions": QUESTIONS})

# TODO cписок “лучших” вопросов (URL = /hot/)
# TODO cписок вопросов по тэгу (URL = /tag/blablabla/)
# TODO cтраница одного вопроса со списком ответов (URL = /question/35/)
# TODO форма логина (URL = /login/)
# TODO форма регистрации (URL = /signup/)
# TODO форма создания вопроса (URL = /ask/)
