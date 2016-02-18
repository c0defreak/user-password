from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PasswordLog
from .forms import RegistrationForm
# Create your views here.


def index(request):
    return render(request, 'myapp/index.html', {'user': request.user})


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            user.save()
            member = User.objects.get(username=form.cleaned_data['username'])
            password_log = PasswordLog()
            password_log.user = member
            password_log.password = member.password
            password_log.save()
            return HttpResponseRedirect('/success/')
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def login_page(request):
    state = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            state = 'check username or password'
    variables = {
        'state': state,
    }
    return render(request, 'myapp/login.html', context=variables)


@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def change_password_page(request):
    state = ''
    if request.user.is_authenticated():
        user = request.user
    if 'c_password' in request.POST and 'n_password' in request.POST:
        c_password = request.POST.get('c_password')
        n_password = request.POST.get('n_password')
        validate = _validate_password(n_password, user)
        auth_user = authenticate(username=user.username, password=c_password)
        if auth_user is not None and validate:
            u = User.objects.get(username=user.username)
            u.set_password(n_password)
            u.save()
            update_session_auth_hash(request, u)
            password_log = PasswordLog()
            password_log.user = u
            password_log.password = u.password
            password_log.save()
            state = 'password change success'
        else:
            state = 'wrong current password or \
            entered a previously used password'
    variables = {
        'state': state,
    }
    return render(request, 'myapp/change_password.html', context=variables)


def _validate_password(password, user):
    p_logs = PasswordLog.objects.filter(user=user)
    for p_log in p_logs:
        if check_password(password, p_log.password):
            return False
    return True
