from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse

from .models import GossipsModel, Comments


def gossips_index(request):
    gossips_all = GossipsModel.objects.all().order_by('-date_published')
    context = {'gossips': gossips_all}
    return render(request, 'gossips/index.html', context)


@login_required()
def gossips_new(request):
    if request.method == 'POST':
        title = request.POST.get('title', False)
        content = request.POST.get('content', False)
        image = request.FILES.get('image', False)
        user = request.user

        slugs = GossipsModel.objects.filter(slug=slugify(title))

        if slugs:
            messages.warning(request, 'Sorry, but a user already shared this same gossip')
        else:
            if image:
                gossip_model = GossipsModel.objects.create(title=title, author=user, content=content, image=image)
            else:
                gossip_model = GossipsModel.objects.create(title=title, author=user, content=content)

            messages.success(request, 'Well Done! You just shared a gossips!!')
        return redirect('gossips:gossips_index')
    else:
        # messages.warning(request, 'Invalid HTTP request')
        return redirect('gossips:gossips_index')


def gossip_detail(request, gossip_slug):
    gossip = get_object_or_404(GossipsModel, slug=gossip_slug).order_by('-date_published')
    context = {'gossip': gossip}
    return render(request, 'gossips/gossip_detail.html', context)


@login_required()
def gossip_reaction(request):
    action = request.GET.get('action', False)
    gossip_id = request.GET.get('gossip_id', False)

    gossip = get_object_or_404(GossipsModel, id=gossip_id)

    try:
        if action == 'true':
            if gossip.false.filter(id=request.user.id).exists():
                messages.warning(request, "You've initially said that this gossip is False!")
                return redirect('gossips:gossips_index')
            if not gossip.true.filter(id=request.user.id).exists():    
                gossip.true.add(request.user)
                gossip.save()
                messages.success(request, 'Thanks! You just indicated that this gossip is true')
            else:
                messages.warning(request, "You have earlier indicated that this gossip is true")
        else:
            if gossip.true.filter(id=request.user.id).exists():
                messages.warning(request, "You've initially said that this gossip is True!")
                return redirect('gossips:gossips_index')
            if not gossip.false.filter(id=request.user.id).exists():
                gossip.false.add(request.user)
                gossip.save()
                messages.success(request, 'Thanks! You just indicated that this gossip is false')
            else:
                messages.warning(request, "You have earlier indicated that this gossip is false")

        return redirect('gossips:gossips_index')
    except:
        messages.warning(request, "An error occured while processing your request")
        return redirect('gossips:gossips_index')


@login_required()
def gossip_add_comment(request):
    if request.method == 'POST':
        gossip_id = request.POST.get('gossipId', False)
        content = request.POST.get('commentContent', False)
        user = request.user

        try:
            gossip = get_object_or_404(GossipsModel, id=gossip_id)
            Comments.objects.create(gossip=gossip, author=user, content=content)
            messages.success(request, "You've successfully made you comment")
        except:
            return redirect('gossips:gossips_index')
    else:
        messages.warning(request, 'Invalid HTTP request')
    return redirect('gossips:gossips_index')
