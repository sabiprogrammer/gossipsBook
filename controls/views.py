from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from .models import FalseInformation

from users.models import Interests
from users.forms import InterestsForm
from gossips.models import GossipsModel
from cheaters.models import CheatersModel


def index(request):
    if request.user.is_authenticated:
        return redirect('gossips:gossips_index')
    else:
        return redirect('/accounts/login')


@login_required()
def welcome(request):
    interests = Interests.objects.all()
    if request.method == 'POST':
        form = InterestsForm(request.POST or None, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Interests saved successfully")
            return redirect('gossips:gossips_index')

    context = {'interests': interests}
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


def false_information(request):
    return render(request, 'false_information.html', {'posts': FalseInformation.objects.all().order_by('-date_published')})