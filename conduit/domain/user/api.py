from typing import Optional
from utilmeta.core import response, request, api, orm
from utilmeta.utils import exceptions
from config.auth import Auth, API
from .models import User, Follow
from .schema import UserRegister, UserLogin, UserSchema, ProfileSchema


class ProfileResponse(response.Response):
    result_key = 'profile'
    result: ProfileSchema


class UserResponse(response.Response):
    result_key = 'user'
    result: UserSchema


@api.route('profiles/{username}')
class ProfileAPI(API):
    username: str = request.PathParam(regex='[A-Za-z0-9_]{1,60}')       # wild range regex
    response = ProfileResponse

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile: Optional[User] = None
        self.user: Optional[User] = None

    @api.get
    async def get(self):
        return await ProfileSchema.get_runtime(self.user.pk).ainit(self.profile)

    @api.post
    async def follow(self):
        await Follow.objects.aget_or_create(
            following=self.profile,
            follower=self.user
        )
        return await self.get()

    @api.delete(follow)
    async def unfollow(self):
        await Follow.objects.filter(
            following=self.profile,
            follower=self.user
        ).adelete()
        return await self.get()

    @api.before('*')
    async def handle_profile(self, user: User = Auth.user_config):
        profile = await User.objects.filter(username=self.username).afirst()
        if not profile:
            raise exceptions.NotFound(f'profile({repr(self.username)}) not found')
        self.profile = profile
        self.user = user


class UserAPI(API):
    response = UserResponse

    @api.get
    async def get(self):      # get current user
        user_id = await self.get_user_id()
        if not user_id:
            raise exceptions.Unauthorized('authentication required')
        return await UserSchema.ainit(user_id)

    @api.put
    async def put(self, user: UserSchema[orm.WP] = request.BodyParam):
        user.id = await self.get_user_id()
        await user.asave()
        return await self.get()


class AuthenticationAPI(API):
    response = UserResponse

    @api.post
    async def post(self, user: UserRegister = request.BodyParam):        # signup
        if await User.objects.filter(username=user.username).aexists():
            raise exceptions.BadRequest(f'duplicate username: {repr(user.username)}')
        if await User.objects.filter(email=user.email).aexists():
            raise exceptions.BadRequest(f'duplicate email: {repr(user.username)}')
        await user.asave()
        await self.user_config.login_user(
            request=self.request,
            user=user.get_instance(),
        )
        return await UserSchema.ainit(user.pk)

    @api.post
    async def login(self, user: UserLogin = request.BodyParam):
        user_inst = await self.user_config.login(self.request, token=user.email, password=user.password)
        if not user_inst:
            raise exceptions.PermissionDenied('email or password wrong')
        return await UserSchema.ainit(user_inst)
