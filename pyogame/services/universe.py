import requests
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from pyogame.models import Lobby, Universum
from pyogame import services


def view(request, template=None, message=None):
    lobby = Lobby.objects.filter(user=request.user)
    if lobby.exists() and lobby.first().email is not None:
        universum = Universum.objects.filter(user=request.user)
        if template is None:
            template = 'empire/universum.html'
        return render(request, template, {'universum': universum, 'message': message})
    else:
        return render(request, 'empire/universum.html', {'message': services.messages.Missing})


def refresh(request):
    # This is dump needs to be in the lib
    def login():
        session.get('https://lobby.ogame.gameforge.com/')
        login_data = {'identity': request.user.lobby.email,
                      'password': services.encryption.decrypt(request.user.lobby.password),
                      'locale': 'en_EN',
                      'gfLang': 'en',
                      'platformGameId': '1dfd8e7e-6e1a-4eb1-8c64-03c3b62efd2f',
                      'gameEnvironmentId': '0a31d605-ffaf-43e7-aa02-d06df7116fc8',
                      'autoGameAccountCreation': False}
        response = session.post('https://gameforge.com/api/v1/auth/thin/sessions', json=login_data)
        if response.status_code is not 201:
            return False
        else:
            token = response.json()['token']
            session.headers.update({'authorization': 'Bearer {}'.format(token)})
            lobby = Lobby.objects.get(user=request.user)
            lobby.token = response.json()['token']
            lobby.save()
            return True

    session = requests.Session()
    session.proxies.update({'https': services.proxy.randomProxy()})
    user_agent = {
        'User-Agent':
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/80.0.3987.100 Mobile Safari/537.36'}
    session.headers.update(user_agent)
    if request.user.lobby.password is None:
        valid = False
    elif request.user.lobby.token is None:
        valid = login()
    else:
        session.headers.update({'authorization': 'Bearer {}'.format(request.user.lobby.token)})
        if 'error' in session.get('https://lobby.ogame.gameforge.com/api/users/me/accounts').json():
            del session.headers['authorization']
            valid = login()
        else:
            valid = True

    if not valid:
        return view(request, message=services.messages.BadLogin)

    servers = session.get('https://lobby.ogame.gameforge.com/api/servers').json()
    accounts = session.get('https://lobby.ogame.gameforge.com/api/users/me/accounts').json()
    for account in accounts:
        for server in servers:
            if account['server']['number'] == server['number']:
                account['server']['name'] = server['name']
                try:
                    universum = Universum.objects.get(user=request.user, name=server['name'])
                except ObjectDoesNotExist:
                    universum = Universum.objects.create(user=request.user, name=server['name'])
                universum.rank = account['details'][0]['value']
                universum.blocked = account['blocked']
                universum.save()
    return redirect('empire')
