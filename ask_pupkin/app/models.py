from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Django пользователь")
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name="Аватарка"
    )
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar_url
        return f"{settings.STATIC_URL}images/default.jpg"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name
    
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def hot(self):
        return self.order_by('-rating')

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions', verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name="Тэги")

    objects = QuestionManager()

    class Meta:
        verbose_name="Вопрос"
        verbose_name_plural="Вопросы"

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    class Meta:
        verbose_name="Ответ"
        verbose_name_plural="Ответы"

    def __str__(self):
        return f'Ответ на: {self.question.title}'

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    value = models.SmallIntegerField(default=1, verbose_name="Значение")

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = "Лайк вопроса"
        verbose_name_plural = "Лайки вопроса"

    def __str__(self):
        return f'Лайки от {self.user} на {self.question}: {self.value}'


class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Пользователь")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Ответ")
    value = models.SmallIntegerField(default=1, verbose_name="Значение")

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = "Лайк ответа"
        verbose_name_plural = "Лайки ответа"

    def __str__(self):
        return f'Лайки от {self.user} на {self.answer}: {self.value}'
