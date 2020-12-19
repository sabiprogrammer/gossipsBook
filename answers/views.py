from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from questions.models import QuestionsModel
from .models import AnswersModel


def answers_all(request):
    posts = [1, 2, 3]
    context = {'posts': posts}
    return render(request, 'answers/all.html', context)


@login_required()
def answers_new(request):
    if request.method == 'POST':
        answer = request.POST.get('answer_question', False)
        question_id = request.POST.get('questionId', False)
        user = request.user

        try:
            question = QuestionsModel.objects.get(id=question_id)
            AnswersModel.objects.create(question=question, author=user, content=answer)
            messages.success(request, 'Well done! You just answered a question')
        except:
            messages.warning(request, 'Oops! Sorry but an error occured.')
        return redirect('questions:questions_index')
    else:
        messages.warning(request, 'You need to log in to answer this question')
        return redirect('questions:questions_index')


