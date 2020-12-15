from django.shortcuts import render


def questions_index(request):
    context = {}
    return render(request, 'questions/index.html', context)


def questions_new(request):
    context = {}
    return render(request, 'index.html', context)

