"""Django admin registrations for quiz models.

This file registers the project's models with the Django admin site and configures
basic `list_display` columns to make content management easier for administrators.
"""

from django.contrib import admin
from quiz.models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


class QuizAdmin(admin.ModelAdmin):
    """Admin display for Quiz.

    list_display shows key fields in the admin list view so staff can scan quizzes quickly.
    """
    list_display = ('title', 'description', 'created_at', 'updated_at')


admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
    """Admin display for Question objects.

    Showing `quiz` and `question_type` helps identify question context quickly.
    """
    list_display = ('quiz', 'text', 'question_type', 'created_at')


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    """Admin display for Answer objects.

    `is_correct` is shown so admins can validate correct choices at a glance.
    """
    list_display = ('question', 'text', 'is_correct')


admin.site.register(Answer, AnswerAdmin)


class UserSubmissionAdmin(admin.ModelAdmin):
    """Admin display for submissions.

    Useful for reviewing recent attempts and scores.
    """
    list_display = ('quiz', 'user_name', 'score', 'submitted_at')


admin.site.register(UserSubmission, UserSubmissionAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    """Admin display for the per-question answer records attached to a submission."""
    list_display = ('submission', 'question', 'answer', 'is_correct')


admin.site.register(UserAnswer, UserAnswerAdmin)


class EventAdmin(admin.ModelAdmin):
    """Admin display for events.

    Shows basic fields so upcoming events can be administered easily.
    """
    list_display = ('title', 'description', 'date', 'location')


admin.site.register(Event, EventAdmin)