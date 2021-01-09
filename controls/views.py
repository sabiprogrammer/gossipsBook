from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from users.models import Interests
from gossips.models import GossipsModel
from cheaters.models import CheatersModel


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


def rfr(request):
    if request.method == 'POST':
        section = request.POST.get('section', False)
        post_id = request.POST.get('post_id', False)
        reason = request.POST.get('reason', False)

        if section == 'gossip':
            gossip = get_object_or_404(GossipsModel, id=post_id)
            print(f'i want to removed gossip: {gossip}')
        elif section == 'cheater':
            cheater = get_object_or_404(CheatersModel, id=post_id)
            print(f'i want to removed cheater: {cheater}')
        messages.success(request, 'Your request has been submitted and will be reviewed')
    return redirect('questions:questions_index')


def feedback(request):
    feedback_message = request.GET.get('feedback_message', False)
    if feedback_message:
        if request.user.is_authenticated:
            username = request.user.username
            email = request.user.email
        else:
            username = "AnonymousUser"
            email = "AnonymousUser"
        
        messages.success(request, 'Feedback received. Thank you!')
    return redirect('gossips:gossips_index')


