from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from .models import Message
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
import sqlite3


@login_required
def homeView(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user))
    users = User.objects.exclude(pk=request.user.id)
    return render(request, 'index.html', {'msgs': messages, 'users': users})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {'form':  AuthenticationForm})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'login.html',
                    {'form': form, 'invalid_creds': True}
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    {'form': form, 'invalid_creds': True}
                )
            login(request, user)

            return redirect(reverse('home'))


class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))

        return render(request, 'signup.html', {'form': form})


def addMessageView(request):
    # Access control flaw here
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # SQL injection flaw
    receiverQuery = cursor.execute(
        "SELECT id FROM auth_user WHERE username = '%s';" % (request.POST.get('receiver')))
    receiver = receiverQuery.fetchone()[0]
    receiverUser = User.objects.get(id=receiver)
    Message.objects.create(sender=request.user, receiver=receiverUser,
                           message=request.POST.get('message'))
    return redirect('/')
