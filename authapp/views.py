from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserEditForm
from authapp.forms import ShopUserRegisterForm
from django.contrib import auth
from django.urls import reverse


def login(request):

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)

                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse('main'))
    else:
        form = ShopUserLoginForm()

    context = {
        'title': 'enter',
        'form': form,
        'next': next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {
        'title': 'Registration',
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    edit_form = ''

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
        else:
            edit_form = ShopUserEditForm(instance=request.user)

    content = {
        'title': 'Editing',
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', content)
