import pyogame.services as services
from pyogame.models import Forum
from django.forms import ModelForm
from django.shortcuts import render, redirect


class Forms:
    class Post(ModelForm):
        class Meta:
            model = Forum
            fields = ['message']


def post(request):
    Post = Forms.Post(request.POST).save(commit=False)
    Post.user = request.user
    Post.save()
    return redirect('forum')
