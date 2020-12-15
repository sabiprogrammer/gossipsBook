from django.shortcuts import render


def cheaters_index(request):
    context = {}
    return render(request, 'cheaters/index.html', context)


def cheaters_new(request):
    context = {}
    return render(request, 'index.html', context)

