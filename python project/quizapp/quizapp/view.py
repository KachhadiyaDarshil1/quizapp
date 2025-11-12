from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Quiz, Answer, UserSubmission, UserAnswer, Event

def home(request):
    return render(request, 'index.html')

def quizlist(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizlist.html', {'quizzes': quizzes})

def quizattempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('answers').all()
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '')
        score = 0
        
        submission = UserSubmission.objects.create(
            quiz=quiz,
            user_name=user_name,
            score=0
        )
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            correct_answer = None
            is_correct = False
            if question.question_type == 'mcq' and answer_id:
                selected = Answer.objects.filter(id=answer_id, question=question).first()
                if selected and selected.is_correct:
                    is_correct = True
                    score += 1
                UserAnswer.objects.create(submission=submission, question=question, answer=selected, is_correct=is_correct)
            elif question.question_type == 'text':
                user_input = request.POST.get(f'question_{question.id}', '').strip().lower()
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer and user_input == correct_answer.text.strip().lower():
                    is_correct = True
                    score += 1
                UserAnswer.objects.create(submission=submission, question=question, is_correct=is_correct)
        submission.score = score
        submission.save()
        return redirect('result', quiz_id=quiz.id)
    return render(request, 'quizattempt.html', {'quiz': quiz, 'questions': questions})

def result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    submission = UserSubmission.objects.filter(quiz=quiz).order_by('-submitted_at').first()
    user_name = submission.user_name if submission else ''
    score = submission.score if submission else 0
    total = quiz.questions.count()
    return render(request, 'result.html', {'quiz': quiz, 'user_name': user_name, 'score': score, 'total': total})

def events(request):
    from django.utils import timezone
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    return render(request, 'event.html', {'events': events})
