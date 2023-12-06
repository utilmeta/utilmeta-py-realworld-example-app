from .env import env
from utilmeta.core import request, api, auth
from utilmeta.core.auth import jwt
from utilmeta.core.request import var
from domain.user.models import User


__all__ = ['Auth', 'API']


class Auth:
    user_config = auth.User(
        User,
        authentication=jwt.JsonWebToken(
            key=env.JWT_SECRET_KEY,
            user_token_field=User.token
        ),
        login_fields=User.email,
        password_field=User.password,
    )
    login_required = auth.Require(name='login')
    admin_required = auth.Require(lambda user: user.admin, name='admin')


class APIMixin(Auth):
    request: request.Request

    async def get_user(self) -> User:
        return await self.user_config.getter(self.request)

    async def get_user_id(self) -> User:
        return await var.user_id.get(self.request)


class API(api.API, APIMixin):
    pass
