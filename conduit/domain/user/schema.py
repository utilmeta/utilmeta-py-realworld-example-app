from utilmeta.core import orm
from .models import User, Follow
from django.db import models
from utype.types import EmailStr


class UsernameMixin(orm.Schema[User]):
    username: str = orm.Field(regex='[A-Za-z0-9][A-Za-z0-9_]{2,18}[A-Za-z0-9]')


class UserBase(UsernameMixin):
    bio: str
    image: str


class UserLogin(orm.Schema[User]):
    email: str
    password: str


class UserRegister(UserLogin, UsernameMixin): pass


class UserSchema(UserBase):
    id: int = orm.Field(no_input=True)
    email: EmailStr
    password: str = orm.Field(mode='wa')
    token: str = orm.Field(mode='r')


class ProfileSchema(UserBase):
    following: bool = False

    @classmethod
    def get_runtime(cls, user_id):
        if not user_id:
            return cls

        class ProfileRuntimeSchema(cls):
            following: bool = models.Exists(
                Follow.objects.filter(following=models.OuterRef('pk'), follower=user_id)
            )

        return ProfileRuntimeSchema
