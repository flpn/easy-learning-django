from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('views', 'score')


admin.site.register(Question, QuestionAdmin)
