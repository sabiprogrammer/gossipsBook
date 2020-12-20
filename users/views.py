from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfileUpdateForm


def login_user(request):
    print('i am here')
    form = CreateUserForm()
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password1')
        # user = authenticate(request, username=username, password=password)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('controls:welcome')
            else:
                messages.warning(request, 'Disabled Account')
                return HttpResponse('Disabled Account')
        else:
            messages.warning(request, 'Incorrect Details Provided!')
            return redirect('login')

    context = {'form': form, 'title': 'Log In'}
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Log Out Successful')
    return redirect('/questions')


@login_required()
def user_profile(request):
    email = request.user.email
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.email = email
            user.save()
            # u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request, 'Some errors occured while updating your profile')
            return render(request, 'users/profile.html', context={'u_form': u_form, 'p_form': p_form})
        return redirect('users:user_profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    context = {'p_form': p_form, 'u_form': u_form, 'email': email}
    return render(request, 'users/profile.html', context)
