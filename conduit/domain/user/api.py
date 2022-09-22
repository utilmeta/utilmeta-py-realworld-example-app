from utilmeta.utils import *
from .schema import UserRegister, UserLogin, UserSchema
from .module import UserCurrent


class UsersAPI(API):
    response = Response(result_data_key='user')

    @property
    def user_data(self):
        if not self.request.user:
            raise exc.PermissionDenied('login failed')
        return UserCurrent(instance=self.request.user).object

    def post(self, data: UserRegister = Request.Body) -> UserSchema:
        Auth.register(data=data, request=self.request)
        return self.user_data

    @api.post(request=Request(max_errors=10))
    def login(self, data: UserLogin = Request.Body) -> UserSchema:
        Auth.login(token=data.email, password=data.password, request=self.request)
        return self.user_data
