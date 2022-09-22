from utilmeta.utils import *
from .models import User
from .schema import UserSchema, ProfileSchema


class UserCurrent(Module):
    model = User
    schema = UserSchema
    option = Option(
        filters={
            'id': Filter(auto_user_id=True)     # ensure sole
        }
    )
    method = Method(
        get=Auth(relate='self'),
        put=(
            Auth(relate='self'),
            Schema.Options(ignore_required=True)    # for PUT method, realworld spec treat every field optional
        )
    )

    @api.after('*')
    def add_response(self, result: schema) -> Response(schema, result_data_key='user'): return result


class UserProfile(Module):
    model = User
    schema = ProfileSchema
    option = Option(
        path_param_field=model.username,
    )
    method = Method(get=Auth())

    def get(self, username: str = Request.Path) -> schema:
        if not username:
            raise exc.NotFound(f'profile username not provided', path=self.request.path)
        return self.object

    @api.post('{username}/follow')
    def follow(self, target: model, user: User = Request.User) -> schema:
        if target is user:
            raise exc.BadRequest('cannot follow yourself')
        target.followers.add(user)
        return self.object

    @api.delete('{username}/follow')
    def unfollow(self, target: model, user: User = Request.User) -> schema:
        target.followers.remove(user)
        return self.object

    @api.after('*')
    def add_response(self) -> Response(result_data_key='profile'): pass
