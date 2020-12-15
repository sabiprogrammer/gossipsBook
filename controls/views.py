from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def gossips(request):
    context = {}
    return render(request, 'gossips.html', context)


def cheaters(request):
    context = {}
    return render(request, 'cheaters.html', context)
