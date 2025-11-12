from django.contrib import admin
from quiz.models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event   
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
admin.site.register(Quiz, QuizAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text', 'question_type', 'created_at')
admin.site.register(Question, QuestionAdmin)    

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
admin.site.register(Answer, AnswerAdmin)

class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user_name', 'score', 'submitted_at')
admin.site.register(UserSubmission, UserSubmissionAdmin)

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'answer', 'is_correct')
admin.site.register(UserAnswer, UserAnswerAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'location')
admin.site.register(Event, EventAdmin)