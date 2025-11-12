"""View handlers for the quiz application.

This module contains the high-level request handlers used by the site. Each view
returns an HttpResponse built from the corresponding template. Important notes:

- `quizattempt` handles both GET (render the form) and POST (grade submission).
- Grading currently happens synchronously in the view and stores `UserSubmission` and
  `UserAnswer` records. No authentication is required; `user_name` is a plain text field.
- Text question matching is case-insensitive and trims surrounding whitespace.

Edge cases / considerations:
- If multiple correct `Answer` rows exist for a text question, the first is used for comparison.
- There is no rate-limiting or duplicate-submission protection here; consider adding middleware
  or server-side guards for production.
"""

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Quiz, Answer, UserSubmission, UserAnswer, Event


def home(request):
    """Render the homepage.

    Template: `index.html` (no context required).
    """
    return render(request, 'index.html')


def quizlist(request):
    """List available quizzes.

    Template: `quizlist.html` expects a context variable `quizzes` which is a queryset
    of `Quiz` objects.
    """
    quizzes = Quiz.objects.all()
    return render(request, 'quizlist.html', {'quizzes': quizzes})


def quizattempt(request, quiz_id):
    """Render a quiz attempt page (GET) or grade a submission (POST).

    GET:
    - Loads the Quiz and its questions (prefetching answers for efficiency) and renders
      `quizattempt.html` with `quiz` and `questions` in context.

    POST:
    - Expects form fields named `question_<id>` for each question. For MCQs the value
      should be the selected Answer id. For text questions the value is the user text.
    - Creates a `UserSubmission` and multiple `UserAnswer` records, computes the score,
      saves it to the submission, and redirects to the `result` view.

    Important implementation details:
    - MCQ grading checks the selected Answer's `is_correct` flag.
    - Text grading compares normalized text (strip + lower) against the first Answer
      with `is_correct=True` for that question.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Prefetch answers to avoid N+1 queries in templates and grading loop
    questions = quiz.questions.prefetch_related('answers').all()

    if request.method == 'POST':
        # Simple username field (no authentication integration here)
        user_name = request.POST.get('user_name', '')
        score = 0

        # Create the submission record first so UserAnswer can FK to it
        submission = UserSubmission.objects.create(
            quiz=quiz,
            user_name=user_name,
            score=0
        )

        # Iterate through questions and grade each one
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            is_correct = False

            if question.question_type == 'mcq' and answer_id:
                # For MCQ: selected answer id should match an Answer for this question
                selected = Answer.objects.filter(id=answer_id, question=question).first()
                if selected and selected.is_correct:
                    is_correct = True
                    score += 1
                UserAnswer.objects.create(submission=submission, question=question, answer=selected, is_correct=is_correct)

            elif question.question_type == 'text':
                # For text: normalize user input and compare to the canonical correct answer (if any)
                user_input = request.POST.get(f'question_{question.id}', '').strip().lower()
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer and user_input == correct_answer.text.strip().lower():
                    is_correct = True
                    score += 1
                # We do not store the raw text answer in this minimal app; only correctness.
                UserAnswer.objects.create(submission=submission, question=question, is_correct=is_correct)

        # Persist the computed score
        submission.score = score
        submission.save()
        # Redirect to a result page (shows the most recent submission)
        return redirect('result', quiz_id=quiz.id)

    # GET: render the quiz attempt form
    return render(request, 'quizattempt.html', {'quiz': quiz, 'questions': questions})


def result(request, quiz_id):
    """Show the most recent submission result for a quiz.

    Template: `result.html` expects `quiz`, `user_name`, `score`, and `total` in context.
    If no submission exists, returns empty/default values.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
    submission = UserSubmission.objects.filter(quiz=quiz).order_by('-submitted_at').first()
    user_name = submission.user_name if submission else ''
    score = submission.score if submission else 0
    total = quiz.questions.count()
    return render(request, 'result.html', {'quiz': quiz, 'user_name': user_name, 'score': score, 'total': total})


def events(request):
    """List upcoming events (date >= today).

    Template: `event.html` expects `events` in context.
    """
    from django.utils import timezone
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    return render(request, 'event.html', {'events': events})
