from django.contrib import admin

from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('views',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
