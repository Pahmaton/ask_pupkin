from django.contrib import admin

from app.models import (
    Answer,
    AnswerLike,
    Profile,
    Question,
    QuestionLike,
    Tag,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "rating",
    )
    search_fields = (
        "user__username",
        "user__email",
    )
    list_select_related = ("user",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = (
        "author",
        "text",
        "rating",
        "created_at",
    )
    readonly_fields = (
        "created_at",
    )

class QuestionLikeInline(admin.TabularInline):
    model = QuestionLike
    extra = 0

class AnswerLikeInline(admin.TabularInline):
    model = AnswerLike
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "rating",
        "created_at",
    )
    list_filter = (
        "created_at",
        "tags",
    )
    search_fields = (
        "title",
        "text",
        "author__user__username",
    )
    ordering = ("-created_at",)
    list_select_related = ("author",)

    filter_horizontal = ("tags",)

    readonly_fields = (
        "created_at",
        "rating",
    )

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "title",
                "text",
                "author",
                "tags",
            )
        }),
        ("Служебные поля", {
            "fields": (
                "rating",
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )

    inlines = (
        AnswerInline,
        QuestionLikeInline,
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_text",
        "question",
        "author",
        "rating",
        "created_at",
    )
    list_filter = (
        "created_at",
    )
    search_fields = (
        "text",
        "author__user__username",
        "question__title",
    )
    list_select_related = (
        "author",
        "question",
    )

    readonly_fields = (
        "created_at",
        "rating",
    )

    inlines = (
        AnswerLikeInline,
    )

    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = "Текст"

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "question",
        "value",
    )
    list_filter = (
        "value",
    )
    search_fields = (
        "user__user__username",
        "question__title",
    )
    list_select_related = (
        "user",
        "question",
    )

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "answer",
        "value",
    )
    list_filter = (
        "value",
    )
    search_fields = (
        "user__user__username",
        "answer__question__title",
    )
    list_select_related = (
        "user",
        "answer",
    )
