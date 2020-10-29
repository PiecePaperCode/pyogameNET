from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pyogame import services


class Request:
    POST = None


class webpage:
    def index(self):
        return render(self, "welcome_page/index.html", {'runningBots': services.bot.settings.runningBots()})

    def about(self):
        return render(self, "welcome_page/about.html")


class user(Request):
    def login(self):
        form = services.user.Forms.Login(self.POST)
        if self.POST and form.is_valid():
            return services.user.login(self, form=form.clean())
        else:
            return render(self, 'user_functionality/login.html', {'form': services.user.Forms.Login})

    def register(self):
        form = services.user.Forms.Register(self.POST)
        if self.POST and form.is_valid():
            return services.user.register(self, form=form.clean())
        else:
            return render(self, 'user_functionality/register.html', {'form': services.user.Forms.Register})

    def logout(self):
        return services.user.logout(self)

    def recover(self):
        form = services.user.Forms.Recover(self.POST)
        if self.POST and form.is_valid():
            return services.user.recover.validate(self, form.clean())
        else:
            return render(self, 'user_functionality/recover.html', {'form': services.user.Forms.Recover})

    def newPassword(self, hash):
        form = services.user.Forms.NewPassword(self.POST)
        if self.POST and form.is_valid():
            return services.user.recover.newPassword(self, hash, form.clean())
        else:
            return render(self, 'user_functionality/recover.html', {'form': services.user.Forms.NewPassword})

    @login_required(login_url='/login/')
    def profile(self):
        form = services.user.Forms.Profile(self.POST)
        if self.POST and form.is_valid():
            return services.user.profile.update(self)
        else:
            return services.user.profile.show(self)

    @login_required(login_url='/login/')
    def validate(self):
        form = services.user.Forms.Validate(self.POST)
        if self.POST and form.is_valid():
            return services.user.valid.validate(self, form=form.clean())
        else:
            return services.user.valid.show(self)

    @login_required(login_url='/login/')
    def delete(self):
        if self.POST:
            return services.user.profile.delete(self)
        else:
            return render(self, 'user_functionality/delete.html')


class empire(Request):
    class refresh:
        @login_required(login_url='/login/')
        def celestial(self, uni):
            return services.empire.celestial(self, universum=uni)

        @login_required(login_url='/login/')
        def ship(self, uni):
            return services.empire.ship(self, universum=uni)

        @login_required(login_url='/login/')
        def defence(self, uni):
            return services.empire.defence(self, universum=uni)

        @login_required(login_url='/login/')
        def building(self, uni):
            return services.empire.building(self, universum=uni)

    @login_required(login_url='/login/')
    def settings(self):
        form = services.empire.settings.Forms.Lobby(self.POST)
        if self.POST and form.is_valid():
            return services.empire.settings.update(self)
        else:
            return services.empire.settings.show(self)

    @login_required(login_url='/login/')
    def view(self, uni):
        return services.empire.view(self, universum=uni)


class universe:
    @login_required(login_url='/login/')
    def view(self):
        return services.universe.view(self)

    @login_required(login_url='/login/')
    def refresh(self):
        return services.universe.refresh(self)


class bot(Request):
    @login_required(login_url='/login/')
    def settings(self, uni):
        form = services.bot.settings.Forms.BotSettings(self.POST)
        expeditionfleet = services.bot.settings.Forms.Fleet(self.POST, prefix="expedition")
        builderfleet = services.bot.settings.Forms.Fleet(self.POST, prefix="builder")
        raiderfleet = services.bot.settings.Forms.Fleet(self.POST, prefix="raider")
        builderdefences = services.bot.settings.Forms.Defences(self.POST)

        if self.POST \
                and form.is_valid() \
                and expeditionfleet.is_valid() \
                and builderfleet.is_valid() \
                and builderdefences.is_valid() \
                and raiderfleet.is_valid():
            return services.bot.settings.update(self, universum=uni)
        else:
            return services.bot.settings.show(self, universum=uni)


@login_required(login_url='/login/')
def forum(self):
    post = services.forum.Forms.Post(self.POST)
    if self.POST and post.is_valid():
        return services.forum.post(self)
    else:
        return render(self, 'forum/forum.html', {'form': services.forum.Forms.Post})


@login_required(login_url='/login/')
def chat(self):
    messages = reversed(services.forum.Forum.objects.all().order_by('-id')[:15])
    return render(self, 'forum/chat.html', {'forum': messages})
