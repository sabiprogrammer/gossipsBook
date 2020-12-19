from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages

from .forms import AddQuestionsForm
from .models import QuestionsModel


def questions_index(request):
    questions_all = QuestionsModel.objects.all().order_by('-date_published')
    context = {'questions': questions_all}
    return render(request, 'questions/index.html', context)


@login_required()
def questions_new(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        image = request.FILES.get('image', False)
        user = request.user

        slugs = QuestionsModel.objects.filter(slug=slugify(title))

        if slugs:
            messages.warning(request, 'Sorry, but a user already asked that same question')
        else:
            if image:
                question_model = QuestionsModel.objects.create(title=title, author=user, image=image)
            else:
                question_model = QuestionsModel.objects.create(title=title, author=user)

            messages.success(request, 'Well Done! You just asked a question')
        return redirect('questions:questions_index')
    else:
        messages.warning(request, 'Please log in')
        return redirect('questions:questions_index')
