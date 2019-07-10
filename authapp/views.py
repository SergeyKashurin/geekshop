from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserEditForm
from authapp.forms import ShopUserRegisterForm
from django.db import transaction
from authapp.forms import ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение для подтверждения регистрации отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения для подтверждения регистрации')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


@login_required
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
        'title': 'Редактирование',
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = 'Подтверждение учетной записи {}'.format(user.username)

    message = 'Для подтверждения учетной записи {} на портале {} перейдите по ссылке: \n{}{}'.format(user.username, settings.DOMAIN_NAME, settings.DOMAIN_NAME, verify_link)

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            return render(request, 'authapp/verification.html')
    except Exception as e:
        return HttpResponseRedirect(reverse('main'))


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)
