from django.forms import ModelForm
from django import forms
from pyogame.models import BotSettings, Ships, Defences
from django.shortcuts import render
from pyogame import services


class Forms:
    class BotSettings(ModelForm):
        active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
        nextRepeat = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
        saiver = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
        expedition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
        collector = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
        collectorTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
        raider = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)
        builder = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), required=False)

        class Meta:
            model = BotSettings
            fields = ['active', 'base', 'repeat', 'nextRepeat',
                      'saiver', 'expedition', 'collector', 'collectorTime', 'raider', 'builder']

    class Fleet(ModelForm):
        class Meta:
            model = Ships
            fields = ['small_transporter', 'large_transporter', 'colonyShip', 'recycler', 'light_fighter',
                      'heavy_fighter', 'cruiser', 'battleship', 'interceptor', 'bomber', 'destroyer', 'deathstar',
                      'reaper', 'explorer', 'espionage_probe']

    class Defences(ModelForm):
        class Meta:
            model = Defences
            fields = ['rocket_launcher', 'laser_cannon_light', 'laser_cannon_heavy', 'gauss_cannon', 'ion_cannon',
                      'plasma_cannon', 'shield_dome_small', 'shield_dome_large', 'missile_interceptor',
                      'missile_interplanetary']


def show(request, universum, message=None):
    botsettings = BotSettings.objects.filter(user=request.user, universum=universum)
    if botsettings.exists():
        form_data = {'universum': universum,
                     'form': Forms.BotSettings(instance=botsettings.first()),
                     'expeditionFleet':
                         Forms.Fleet(prefix="expedition", instance=botsettings.first().expeditionFleet),
                     'builderFleet':
                         Forms.Fleet(prefix="builder", instance=botsettings.first().builderFleet),
                     'raiderFleet':
                         Forms.Fleet(prefix="raider", instance=botsettings.first().raiderFleet),
                     'builderdefences':
                         Forms.Defences(instance=botsettings.first().builderDefences),
                     'message': message,
                     'nextRepeat': botsettings.first()}
        return render(request, 'empire/../../templates/bot/settings.html', form_data)
    else:
        form_data = {'universum': universum,
                     'form': Forms.BotSettings,
                     'expeditionFleet': Forms.Fleet(prefix="expedition"),
                     'builderFleet': Forms.Fleet(prefix="builder"),
                     'raiderFleet': Forms.Fleet(prefix="raider"),
                     'builderdefences': Forms.Defences,
                     'nextRepeat': botsettings.first()}
        return render(request, 'empire/../../templates/bot/settings.html', form_data)


def update(request, universum):
    botsettings = BotSettings.objects.filter(user=request.user, universum=universum)
    if botsettings.exists():
        builderfleet = Forms.Fleet(
            request.POST,
            prefix="builder",
            instance=botsettings.first().builderFleet
        ).save()
        expeditionfleet = Forms.Fleet(
            request.POST,
            prefix="expedition",
            instance=botsettings.first().expeditionFleet
        ).save()
        raiderfleet = Forms.Fleet(
            request.POST,
            prefix="raider",
            instance=botsettings.first().raiderFleet
        ).save()
        builderdefences = Forms.Defences(request.POST, instance=botsettings.first().builderDefences).save()
        botsettings = Forms.BotSettings(request.POST, instance=botsettings.first()).save(commit=False)
    else:
        builderdefences = Forms.Defences(request.POST).save()
        builderfleet = Forms.Fleet(request.POST, prefix="builder").save()
        expeditionfleet = Forms.Fleet(request.POST, prefix="expedition").save()
        raiderfleet = Forms.Fleet(request.POST, prefix="raider").save()
        botsettings = Forms.BotSettings(request.POST).save(commit=False)
        botsettings.user = request.user
        botsettings.universum = universum
    botsettings.expeditionFleet = expeditionfleet
    botsettings.builderFleet = builderfleet
    botsettings.raiderFleet = raiderfleet
    botsettings.builderDefences = builderdefences
    botsettings.active = False
    botsettings.save()
    return show(request=request, universum=universum, message=services.messages.OK)


def runningBots():
    return len(BotSettings.objects.filter(active=True))
