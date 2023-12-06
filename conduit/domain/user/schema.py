from utilmeta.utils import *
from utilmeta.core import orm
from .models import User, Follow
from utilmeta.core.orm.backends.django import expressions as exp


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
    email: str
    password: str = orm.Field(mode='wa')
    token: str = orm.Field(mode='r')


class ProfileSchema(UserBase):
    following: bool = False

    @classmethod
    def get_runtime(cls, user_id):
        if not user_id:
            return cls

        class ProfileRuntimeSchema(cls):
            following: bool = orm.Field(
                exp.Exists(
                    Follow.objects.filter(following=exp.OuterRef('pk'), follower=user_id)
                )
            )

        return ProfileRuntimeSchema
