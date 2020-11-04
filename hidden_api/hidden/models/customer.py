from django.db import models
from django.apps import apps
# from .secretbox import SecretBox


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    wishes = models.CharField(
        default="", max_length=800, null=True, blank=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='users', null=True, blank=True)


class SecretBox(models.Model):
    name = models.CharField(max_length=200)
    limit = models.BooleanField(default=False)
    limitValue = models.IntegerField(default=0, null=True, blank=True)
    description = models.CharField(max_length=800, null=True, blank=True)
    admin = models.ForeignKey(
        'auth.User', related_name='admin', on_delete=models.CASCADE, null=True, blank=True)


class Membership(models.Model):
    secretbox = models.ForeignKey(
        'hidden.SecretBox', models.DO_NOTHING, related_name='secretboxs')
    santa = models.ForeignKey(
        'hidden.Member', models.DO_NOTHING, related_name='santas', null=True, blank=True)
    exception = models.ForeignKey(
        'hidden.Member', models.DO_NOTHING, related_name='exceptions', null=True, blank=True)
    member = models.ForeignKey(
        'hidden.Member', models.DO_NOTHING, related_name='members')
