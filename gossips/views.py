from django.shortcuts import render


def gossips_index(request):
    context = {}
    return render(request, 'gossips/index.html', context)


def gossips_new(request):
    context = {}
    return render(request, 'index.html', context)

