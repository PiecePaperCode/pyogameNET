from django.forms import ModelForm
from django import forms
from django.shortcuts import render
from pyogame.models import Lobby, Celestial, Universum
from pyogame import services


class Forms:
    class Lobby(ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)

        class Meta:
            model = Lobby
            fields = ['email', 'password']


def update(request):
    lobby = Lobby.objects.filter(user=request.user)
    if lobby.exists():
        lobby = Forms.Lobby(request.POST, instance=lobby.first()).save(commit=False)
    else:
        lobby = Forms.Lobby(request.POST).save(commit=False)
        lobby.user = request.user
    lobby.password = services.encryption.encrypt(lobby.password)
    lobby.token = None
    lobby.save()
    Universum.objects.filter(user=request.user).delete()
    Celestial.objects.filter(user=request.user).delete()
    return services.universe.view(request=request, message=services.messages.OK)


def show(request, message=None):
    lobby = Lobby.objects.filter(user=request.user)
    if lobby.exists():
        form_data = {'form': Forms.Lobby(instance=lobby.first()), 'message': message}
        return render(request, 'empire/settings.html', form_data)
    else:
        form_data = {'form': Forms.Lobby, 'message': services.messages.Missing}
        return render(request, 'empire/settings.html', form_data)
