from utilmeta.utils import *
from .models import User
from .schema import UserSchema, ProfileSchema


class UserCurrent(Module):
    model = User
    schema = UserSchema
    option = Option(
        filters={
            'id': Filter(auto_user_id=True)
        }
    )
    method = Method(
        get=Auth(relate='self'),
        put=Auth(relate='self'),
    )

    @api.after(method.PUT)
    def add_user_result(self) -> schema:
        return self.object

    @api.after('*')
    def add_response(self) -> Response(result_data_key='user'): pass


class UserProfile(Module):
    model = User
    schema = ProfileSchema
    option = Option(
        path_param_field=model.username,
        path_param_rule=str     # mark as required
    )
    method = Method(get=Auth())

    @api.post(request=Request(login=True))
    def follow(self, target: model) -> schema:
        target.followers.add(self.user)
        return self.object

    @api.delete(follow, request=Request(login=True))
    def unfollow(self, target: model) -> schema:
        target.followers.remove(self.user)
        return self.object

    @api.after('*')
    def add_response(self) -> Response(result_data_key='profile'): pass
