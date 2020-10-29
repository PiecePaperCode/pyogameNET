from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import auth
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from pyogame.models import Lobby

import pyogame.services as services


class messages:
    class create:
        OK = {'OK': 'User Created'}
        Fail = {'Fail': 'There is already an User with the same Username'}

    class login:
        OK = {'OK': 'User Created please log in'}
        Fail = {'Fail': 'Please enter a correct username and password. Note that both fields may be case-sensitive.'}

    class update:
        OK = {'OK': 'Profile Updated'}
        Fail = {'Fail': 'Your supplied Data was incorrect please try again'}


class Forms:
    class Register(forms.Form):
        Username = forms.CharField(label='Username*', max_length=100)
        Email = forms.EmailField()
        Password = forms.CharField(label='Password*', max_length=32, widget=forms.PasswordInput)

    class Login(forms.Form):
        Username = forms.CharField(label='Username*', max_length=100)
        Password = forms.CharField(label='Password*', max_length=32, widget=forms.PasswordInput)

    class Profile(ModelForm):
        Old = forms.CharField(label='Old Password*', max_length=32, widget=forms.PasswordInput)
        New = forms.CharField(label='New Password*', max_length=32, widget=forms.PasswordInput)

        class Meta:
            model = User
            fields = ['email']

    class Validate(forms.Form):
        pin = forms.CharField(label='pin')

    class Recover(forms.Form):
        username = forms.CharField(label='username')
        email = forms.EmailField(label='email')

    class NewPassword(forms.Form):
        password1 = forms.CharField(label='New Password*', max_length=32, widget=forms.PasswordInput)
        password2 = forms.CharField(label='Repeat*', max_length=32, widget=forms.PasswordInput)


def register(request, form):
    try:
        User.objects.create_user(username=form['Username'], email=form['Email'], password=form['Password']).save()
    except IntegrityError:
        return render(request,
                      'user_functionality/register.html',
                      {'form': Forms.Login, 'messages': messages.create.Fail})
    return login(request=request, form=form)


def login(request, form):
    user = auth.authenticate(request=request, username=form['Username'], password=form['Password'])
    if user is not None:
        auth.login(request, user)
        lobby = Lobby.objects.get_or_create(user=request.user)[0]
        if not lobby.auth:
            services.email.send_verification(request)
            return redirect('validate')
        else:
            return redirect('/empire')
    else:
        data = {'form': Forms.Login, 'message': services.messages.Fail}
        return render(request, 'user_functionality/login.html', data)


def logout(request):
    auth.logout(request)
    return redirect('/')


class profile:
    user = None
    POST = None

    def update(self):
        passwords = Forms.Profile(self.POST)
        if passwords.is_valid():
            passwords = passwords.clean()
            validPassword = auth.authenticate(self, username=self.user, password=passwords['Old'])
            if validPassword is not None:
                user = User.objects.get(username=self.user)
                Forms.Profile(self.POST, instance=user).save()
                user.set_password(passwords['New'])
                user.save()
                lobby = Lobby.objects.get(user=self.user)
                lobby.auth = False
                lobby.save()
                return redirect('/login')
            else:
                return profile.show(self=self, message=services.messages.Fail)
        else:
            return profile.show(self=self, message=services.messages.Fail)

    def show(self, message=None):
        user = User.objects.get(username=self.user)
        user = Forms.Profile(instance=user)
        validUser = Lobby.objects.get(user=self.user).auth
        return render(self, 'user_functionality/profile.html', {'form': user, 'auth': validUser, 'message': message})

    def delete(self):
        User.objects.get(username=self.user).delete()
        return logout(self)


class recover:
    def validate(self, form):
        user = User.objects.filter(email=form['email'], username=form['username'])
        if user.exists():
            services.email.send_recovery(user.first())
            data = {'form': Forms.Recover, 'message': services.messages.CheckEmail}
            return render(self, 'user_functionality/recover.html', data)
        else:
            data = {'form': Forms.Recover, 'message': services.messages.Fail}
            return render(self, 'user_functionality/recover.html', data)

    def newPassword(self, recoverurl, form):
        if form['password1'] == form['password2']:
            users = User.objects.all()
            for user in users:
                if recoverurl == services.encryption.hash(user):
                    user.set_password(form['password1'])
                    user.save()
                    return login(self, {'Username': user.username, 'Password': form['password1']})
            data = {'form': services.user.Forms.NewPassword, 'message': services.messages.Fail}
            return render(self, 'user_functionality/recover.html', data)
        else:
            data = {'form': services.user.Forms.NewPassword, 'message': services.messages.BadRecovery}
            return render(self, 'user_functionality/recover.html', data)


class valid:
    user = None

    def show(self):
        form = Forms.Validate()
        validUser = Lobby.objects.get(user=self.user).auth
        data = {'form': form, 'auth': validUser, 'message': services.messages.CheckEmail}
        return render(self, 'user_functionality/validate.html', data)

    def validate(self, form):
        if form['pin'] == services.encryption.hash_pin(self):
            lobby = Lobby.objects.get(user=self.user)
            lobby.auth = True
            lobby.save()
            return services.universe.view(self, message=services.messages.OK)
        else:
            data = {'form': Forms.Validate(), 'auth': auth,
                    'message': services.messages.Fail}
            return render(self, 'user_functionality/validate.html', data)
