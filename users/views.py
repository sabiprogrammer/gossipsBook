from django.shortcuts import render
from .forms import CreateUserForm


# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Account created successfully. Please log in')
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
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
    return redirect('home')


def user_profile(request):
    context = {}
    return render(request, 'users/profile.html', context)
