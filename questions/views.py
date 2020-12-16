from django.shortcuts import render
from .forms import AddQuestionsForm


def questions_index(request):
    context = {}
    return render(request, 'questions/index.html', context)


def questions_new(request):
    if request.method == 'POST':
        pass

    form = AddQuestionsForm()
    context = {'form': form}
    return render(request, 'questions/new.html', context)

