from utilmeta.fields import *


class User(Model):
    username = CharField(max_length=40, unique=True)
    password = PasswordField(max_length=60)
    email = EmailField(max_length=60, unique=True)
    followers = ManyToManyField('self', related_name='followed_bys', symmetrical=False)
    favorites = ManyToManyField('article.Article', related_name='favorited_bys', symmetrical=False)
    token = TextField(default=None, null=True)
    bio = TextField(default=None, null=True)
    image = URLField(default=None, null=True)
