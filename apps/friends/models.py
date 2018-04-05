# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime
from datetime import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['birth']) < 1:
            errors["empty_date"] = "Date cannot be empty!"
            return errors
        now = datetime.now()
        form_dt = datetime.strptime("{}".format(postData['birth']), "%Y-%m-%d")
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']:
                errors['duplicate_email'] = "Email already in database"
        if len(postData['email']) < 1:
            errors["empty_email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid Email Address!"
        if len(postData['name']) < 3:
            errors["empty_name"] = "First name must be at least 3 characters long!"
        if any(i.isdigit() for i in postData['name']) == True:
            errors["invalid_name"] = "Invalid first name!"
        if len(postData['alias']) < 1:
            errors["empty_alias"] = "Alias cannot be empty!"
        if len(postData['password']) < 8:
            errors["short_password"] = "Password must contain at least eight characters!"
        if postData['confirm_password'] != postData['password']:
            errors["password_does_not_match"] = "Passwords must match!"
        if now < form_dt:
            errors["future_birth"] = "Cannot select a future birthday!"
        return errors
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData['email']):
            errors['unregistered'] = "Invalid Email!"
        else:
            user = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == True:
                pass
            else:
                errors['invalid_password'] = "Invalid Password!"
        return errors
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Friend(models.Model):
    friender = models.ForeignKey(User, related_name='follower')
    friendee = models.ForeignKey(User, related_name='followee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)