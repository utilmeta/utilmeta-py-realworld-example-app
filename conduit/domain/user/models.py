from django.db import models
from utilmeta.core.orm.backends.django import models as amodels
from utilmeta.core.orm.backends.django.models import PasswordField


class User(amodels.AwaitableModel):
    username = models.CharField(max_length=40, unique=True)
    password = PasswordField(max_length=100)
    email = models.EmailField(max_length=60, unique=True)
    followers = models.ManyToManyField(
        'self', related_name='followed_bys', through='Follow', through_fields=('following', 'follower'),
        symmetrical=False
    )
    favorites = models.ManyToManyField('article.Article', through='Favorite', related_name='favorited_bys')
    token = models.TextField(default='')
    bio = models.TextField(default='')
    image = models.URLField(default='')


class Favorite(amodels.AwaitableModel):
    user = models.ForeignKey(User, related_name='article_favorites', on_delete=amodels.ACASCADE)
    article = models.ForeignKey('article.Article', related_name='user_favorites', on_delete=amodels.ACASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')


class Follow(amodels.AwaitableModel):
    following = models.ForeignKey(User, related_name='user_followers', on_delete=amodels.ACASCADE)
    follower = models.ForeignKey(User, related_name='user_followings', on_delete=amodels.ACASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('following', 'follower')
