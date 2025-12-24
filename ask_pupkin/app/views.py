from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from app.forms import AnswerForm, LoginForm, ProfileForm, QuestionForm, RegistrationForm
from app.models import Answer, AnswerLike, Profile, Question, QuestionLike, Tag


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

# выход
def logout_view(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'questions'))

# форма создания вопроса (URL = /ask/)
@login_required(login_url="/login/", redirect_field_name="continue")
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

# страница одного вопроса со списком ответов (URL = /question/<id>/)
def question_view(request, question_id):
    q = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = q
            answer.save()
            return redirect(f"{reverse('question', args=[q.id])}#answer-{answer.id}")
    else:
        form = AnswerForm()

    answers_qs = q.answers.all().order_by('created_at')
    answers_page = paginate(answers_qs, request, per_page=30)
    return render(request, "question.html", {
        "question": q,
        "form": form,
        "answers": answers_page.object_list,
        "page_obj": answers_page
    })

# форма редактирования профиля
@login_required(login_url="/login/", redirect_field_name="continue")
def profile_edit(request):
    if request.method == 'POST':
        user_instance = User.objects.get(pk=request.user.pk)
        form = ProfileForm(request.POST, request.FILES, instance=user_instance, profile=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user, profile=request.user.profile)

    return render(request, "profile.html", {"form": form})

# вьюха изменения рейтинга пользователем
@login_required
@require_POST
def vote(request):
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type')
    action = request.POST.get('action')
    val = 1 if action == 'like' else -1

    user_profile = request.user.profile

    if obj_type == 'question':
        obj = get_object_or_404(Question, pk=obj_id)
        like_model = QuestionLike
        lookup = {'question': obj, 'user': user_profile}
    else:
        obj = get_object_or_404(Answer, pk=obj_id)
        like_model = AnswerLike
        lookup = {'answer': obj, 'user': user_profile}

    existing_like = like_model.objects.filter(**lookup).first()

    if existing_like:
        if existing_like.value == val:
            existing_like.delete()
        else:
            existing_like.value = val
            existing_like.save()
    else:
        like_model.objects.create(**lookup, value=val)

    new_rating = like_model.objects.filter(**{obj_type: obj}).aggregate(Sum('value'))['value__sum'] or 0
    obj.rating = new_rating
    obj.save()

    return JsonResponse({'new_rating': new_rating})

# отметить что ответ правильный
@login_required
@require_POST
def mark_correct(request):
    q_id = request.POST.get('question_id')
    a_id = request.POST.get('answer_id')

    question = get_object_or_404(Question, id=q_id)

    if question.author.user != request.user:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    question.answers.all().update(is_correct=False)

    answer = get_object_or_404(Answer, id=a_id, question=question)
    answer.is_correct = True
    answer.save()

    return JsonResponse({'status': 'ok'})
