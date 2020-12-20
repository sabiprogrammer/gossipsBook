from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from users.models import Interests


def index(request):
    if request.user.is_authenticated:
        return redirect('questions:questions_index')
    else:
        return redirect('/accounts/login')


@login_required()
def welcome(request):
    if request.method == 'POST':
        questions = request.POST.get('questions', False)
        gossips = request.POST.get('gossips', False)
        cheaters = request.POST.get('cheaters', False)
        travels = request.POST.get('travels', False)
        sports = request.POST.get('sports', False)
        politics = request.POST.get('politics', False)

        try:
            if questions:
                interest = Interests.objects.get(title='Questions')
                request.user.profile.interests.add(interest)

            if gossips:
                interest = Interests.objects.get(title='Gossips')
                request.user.profile.interests.add(interest)

            if cheaters:
                interest = Interests.objects.get(title='Cheaters')
                request.user.profile.interests.add(interest)

            if travels:
                interest = Interests.objects.get(title='Travels')
                request.user.profile.interests.add(interest)

            if sports:
                interest = Interests.objects.get(title='Sports')
                request.user.profile.interests.add(interest)

            if politics:
                interest = Interests.objects.get(title='Politics')
                request.user.profile.interests.add(interest)
            messages.success(request, 'Interests Saved! Welcome To Your Feed')
        except:
            pass
        return redirect('controls:index_page')

    context = {}
    return render(request, 'welcome.html', context)

