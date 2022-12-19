from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["text"]}),
        ("Date information", {"fields": ["publish_at"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("text", "publish_at", "was_published_recently")
    list_filter = ["publish_at"]
    search_fields = ["text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
