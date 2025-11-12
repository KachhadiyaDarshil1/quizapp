from django.db import models


"""Database models for the quiz application.

This module defines the core data models used by the app:
- Quiz: container for questions
- Question: individual question attached to a Quiz
- Answer: possible answer for a question (used for MCQs and reference for text questions)
- UserSubmission: records a user's attempt at a Quiz and the total score
- UserAnswer: records the user's answer to a specific Question within a UserSubmission
- Event: simple model for upcoming events

Keep model responsibilities small. Validation and grading logic is performed in views; models primarily store data and relationships.
"""


class Quiz(models.Model):
    """A quiz containing many questions.

    Fields:
    - title: short human-readable title
    - description: long description/instructions
    - created_at/updated_at: timestamps managed by Django
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """A single question that belongs to a Quiz.

    The `question_type` distinguishes MCQ from free-text questions. For MCQ questions the
    related `Answer` rows should include exactly one with `is_correct=True` (enforced by
    application logic, not at DB level here).
    """
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('text', 'Text'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=512)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class Answer(models.Model):
    """A possible answer for a Question.

    For MCQ questions, `is_correct` marks the correct choice. For text questions, answers
    may be used as canonical correct text to compare against user input.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} -> {self.text[:30]}"


class UserSubmission(models.Model):
    """Represents a user's attempt at a Quiz and the computed score.

    The `score` is stored after grading in the view layer. `user_name` is a simple identifier
    (no auth/foreign key used in this project). `submitted_at` records when the attempt occurred.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.quiz.title} ({self.score})"


class UserAnswer(models.Model):
    """Stores a single answer provided by a user as part of a UserSubmission.

    - `answer` may be null for text questions where the user's typed response is stored elsewhere
      (in this simple app we only record correctness boolean for text answers).
    - `is_correct` is computed when the submission is graded and saved here for auditability.
    """
    submission = models.ForeignKey(UserSubmission, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission {self.submission.id} - Q{self.question.id} -> {self.is_correct}"


class Event(models.Model):
    """Simple model to list upcoming events related to quizzes.

    Used by the `events` view to show future events ordered by date.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.date})"

