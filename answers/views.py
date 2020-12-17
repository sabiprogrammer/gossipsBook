from django.shortcuts import render


def answers_all(request):
    posts = [1, 2, 3]
    context = {'posts': posts}
    return render(request, 'answers/all.html', context)


def answers_new(request):
    # if request.method == 'POST':
    #     pass
    #
    # form = AddQuestionsForm()
    context = {'form': form}
    return render(request, 'answers/new.html', context)

