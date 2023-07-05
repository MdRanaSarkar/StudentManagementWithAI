from django.contrib import admin
from StudentQuiz.models import Quiz,Question,Answer,FinalResult
# Register your models here.

admin.site.register(Quiz)

class AnswerInline(admin.TabularInline):
    model = Answer
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)

admin.site.register(FinalResult)