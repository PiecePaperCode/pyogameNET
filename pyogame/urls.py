from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from pyogame import view


urlpatterns = [
    path('', view.webpage.index, name='index'),
    path('about', view.webpage.about, name='about'),
    path('register/', view.user.register, name='register'),
    path('login/', view.user.login, name='login'),
    path('logout/', view.user.logout, name='logout'),
    path('profile/', view.user.profile, name='profile'),
    path('profile/validate', view.user.validate, name='validate'),
    path('recover', view.user.recover, name='recover'),
    path('recover/<str:hash>', view.user.newPassword, name='recover/hash'),
    path('delete/', view.user.delete, name='delete'),

    path('empire/', view.universe.view, name='empire'),
    path('empire/refresh', view.universe.refresh, name='empire/refresh'),
    path('empire/settings', view.empire.settings, name='empire/settings'),
    path('empire/universe/<str:uni>', view.empire.view, name='empireView'),
    path('empire/universe/<str:uni>/refresh/celestial', view.empire.refresh.celestial, name='refresh/celestial'),
    path('empire/universe/<str:uni>/refresh/ship', view.empire.refresh.ship, name='refresh/ship'),
    path('empire/universe/<str:uni>/refresh/defence', view.empire.refresh.defence, name='refresh/defence'),
    path('empire/universe/<str:uni>/refresh/building', view.empire.refresh.building, name='refresh/building'),
    path('empire/bot/<str:uni>', view.bot.settings, name='bot/settings'),

    path('forum/', view.forum, name='forum'),
    path('forum/chat', view.chat, name='forum/chat'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
