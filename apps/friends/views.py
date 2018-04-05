# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import *

# Create your views here.
def index(req):
    if req.session == True:
        req.session.clear()
    return render(req, 'friends/index.html')

def create(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/main')
    User.objects.create(name=req.POST['name'], alias=req.POST['alias'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()), birth = req.POST['birth'])
    req.session['active_alias'] = User.objects.last().alias
    req.session['active_id'] = User.objects.last().id
    return redirect('/friends')

def login(req):
    errors = User.objects.login_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/main')
    loggedUser = User.objects.get(email = req.POST['email'])
    req.session['active_alias'] = loggedUser.alias
    req.session['active_id'] = loggedUser.id
    return redirect('/friends')

def logoff(req):
    req.session.clear()
    return redirect('/main')

def friends(req):
    if req.session == False:
        return redirect('/main')
    
    friends_id_list = []
    other_users_id_list = []
    not_friended = []

    friends_list = Friend.objects.filter(friender = User.objects.get(id = req.session['active_id']))
    print len(friends_list)
    for person in friends_list:
        friends_id_list.append(person.friendee.id)
    print friends_id_list
    other_users = User.objects.exclude(id = req.session['active_id'])
    for other_user in other_users:
        other_users_id_list.append(other_user.id)
    print other_users_id_list
    not_friended = list(set(other_users_id_list) - set(friends_id_list))
    print not_friended

    context = {
        'active_alias': req.session['active_alias'],
        'friends': friends_list,
        'users': User.objects.exclude(id = req.session['active_id']),
        'not_friended': not_friended
    }
    return render(req, 'friends/friends.html', context)

def view(req, user_id):
    if req.session == False:
        return redirect('/main')
    context = {
        'friend': User.objects.get(id = user_id),
    }
    return render(req, 'friends/view.html', context)

def add(req, user_id):
    Friend.objects.create(friender = User.objects.get(id = req.session['active_id']), friendee = User.objects.get(id = user_id))
    Friend.objects.create(friender = User.objects.get(id = user_id), friendee = User.objects.get(id = req.session['active_id']))
    return redirect('/friends')

def delete(req, user_id):
    Friend.objects.get(friender = User.objects.get(id = req.session['active_id']), friendee = User.objects.get(id = user_id)).delete()
    Friend.objects.get(friender = User.objects.get(id = user_id), friendee = User.objects.get(id = req.session['active_id'])).delete()
    return redirect('/friends')