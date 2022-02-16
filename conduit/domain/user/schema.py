from utilmeta.utils import *


class UserBase(Schema):
    username: str
    bio: str
    image: str


class UserLogin(Schema):
    email: str
    password: str


class UserRegister(UserLogin):
    username: str


class UserSchema(UserBase):
    email: str
    token: str = Field(readonly=True)


class ProfileSchema(UserBase):
    following: bool = Field(request_expression=lambda request: exp.Count('id', filter=exp.Q(followers=request.user)))
