from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages

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
def gossip_reaction(request, pk):
    action = request.GET.get('action', False)
    gossip = get_object_or_404(GossipsModel, id=pk)

    if action == 'true':
        if gossip.false.filter(id=request.user.id).exists():
            gossip.false.remove(request.user)
            gossip.save()
        if gossip.true.filter(id=request.user.id).exists():
            gossip.true.remove(request.user)
            gossip.save()
            messages.info(request, 'You indicated that gossip is true before. But not anymore')
            # gossip.true.all().count();
        else:
            gossip.true.add(request.user)
            gossip.save()
            messages.success(request, 'Thanks! You just indicated that this gossip is true')
            # gossip.true.all().count();
    else:
        if gossip.true.filter(id=request.user.id).exists():
            gossip.true.remove(request.user)
            gossip.save()
        if gossip.false.filter(id=request.user.id).exists():
            gossip.false.remove(request.user)
            gossip.save()
            messages.info(request, 'You indicated that gossip is false before. But not anymore')
            # gossip.true.all().count();
        else:
            gossip.false.add(request.user)
            gossip.save()
            messages.success(request, 'Thanks! You just indicated that this gossip is false')
            # gossip.true.all().count();

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
