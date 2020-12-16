from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    context = {}
    return render(request, 'index.html', context)


def welcome(request):
    if request.method == 'POST':
        box1 = request.POST.get('box1', False)
        box2 = request.POST.get('box2', False)
        box3 = request.POST.get('box3', False)
        print('box 1: ', box1, 'box2:', box2, 'box3:', box3)
        messages.success(request, 'Interests Saved! Welcome To Your Feed')
        return redirect('questions:questions_index')
    context = {}
    return render(request, 'welcome.html', context)


def cheaters(request):
    context = {}
    return render(request, 'cheaters.html', context)
