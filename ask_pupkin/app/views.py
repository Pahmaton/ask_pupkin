from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from app.forms import LoginForm, QuestionForm, RegistrationForm
from app.models import Profile, Question, Tag


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
    qs = Question.objects.new().select_related('author__user').prefetch_related('tags').annotate(answers_count=Count('answers'))
    page = paginate(qs, request, per_page=20)
    return render(request, "questions.html", {"questions": page.object_list, "page_obj": page, "question_type": "new"})


# список “лучших” вопросов (URL = /hot/)
def hot_questions(request):
    qs = Question.objects.hot().select_related('author__user').prefetch_related('tags').annotate(answers_count=Count('answers'))
    page = paginate(qs, request, per_page=20)
    return render(request, "questions.html", {"questions": page.object_list, "page_obj": page, "question_type": "hot"})


# список вопросов по тэгу (URL = /tag/<tag>/)
def questions_by_tag(request, tag):
    tag_obj = get_object_or_404(Tag, name=tag)
    qs = tag_obj.questions.all().select_related('author__user').prefetch_related('tags').annotate(answers_count=Count('answers'))
    page = paginate(qs, request, per_page=20)
    return render(request, "questions_by_tag.html", {"questions": page.object_list, "page_obj": page, "tag": tag_obj})


# страница одного вопроса со списком ответов (URL = /question/<id>/)
def question(request, question_id):
    q = get_object_or_404(
        Question.objects.select_related('author__user').prefetch_related('tags'),
        pk=question_id
    )

    answers_qs = q.answers.select_related('author__user').order_by('created_at')

    answers_page = paginate(answers_qs, request, per_page=30)
    return render(request, "question.html", {
        "question": q,
        "answers": answers_page.object_list,
        "page_obj": answers_page
    })

# форма профиля
def profile_form(request):
    return render(request, "profile.html")

# страница лучших пользователей сайта
def best_members(request, username):
    if username not in ["MrFreeman", "DrHouse", "Bender", "QueenVictoria", "V_Pupkin"]:
        return redirect("questions")
    member = get_object_or_404(Profile, user__username=username)
    return render(request, "best_members.html", {"member": member})

# форма входа
def login_view(request):
    continue_url = request.GET.get('continue', 'questions')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(continue_url)
            else:
                form.add_error(None, "Incorrect login or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "continue_url": continue_url})

# форма регистрации (URL = /signup/)
def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(user=user, avatar=form.cleaned_data['avatar'])
            auth.login(request, user)
            return redirect('questions')
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

# форма создания вопроса (URL = /ask/)
@login_required
def add_question_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()

            tags_raw = form.cleaned_data['tags']
            if tags_raw:
                for tag_name in [t.strip() for t in tags_raw.split(',')]:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)

            return redirect('question', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, "add_question.html", {"form": form})
