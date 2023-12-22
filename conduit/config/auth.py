from .env import env
from utilmeta.core import api, auth
from utilmeta.core.auth import jwt
from utilmeta.core.request import var
from domain.user.models import User


class API(api.API):
    user_config = auth.User(
        User,
        authentication=jwt.JsonWebToken(
            key=env.JWT_SECRET_KEY,
            user_token_field=User.token
        ),
        login_fields=User.email,
        password_field=User.password,
    )

    async def get_user(self) -> User:
        return await self.user_config.getter(self.request)

    async def get_user_id(self) -> int:
        return await var.user_id.get(self.request)
