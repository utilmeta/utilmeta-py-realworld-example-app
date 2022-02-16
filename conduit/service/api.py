from utilmeta.utils import *
from utilmeta.types import *
from utilmeta.util.common import CaseStyle
from domain.user.api import UsersAPI
from domain.user.module import UserCurrent, UserProfile
from domain.article.module import ArticleMain


class RootAPI(API):
    request = Request(csrf_exempt=True)
    response = Response(case_style=CaseStyle.camelCase)

    class Router:
        user = UserCurrent
        users = UsersAPI
        profiles = UserProfile
        articles = ArticleMain

    @api.get
    def tags(self) -> Response(List[str], result_data_key='tags'):
        from domain.article.models import Tag
        return Tag.objects.values_list('name', flat=True)

    @api.before(Router.user, Router.users)
    def alter_user_body(self):
        if self.request.data:
            self.request.data = self.request.data.get('user', self.request.data)

    @api.before(Router.articles)
    def alter_content_body(self):
        if self.request.data:
            self.request.data = self.request.data.get(
                'article', self.request.data.get('comment', self.request.data)
            )

    @api.handle('*', exc.BadRequest)
    def handle_bad_request(self, e: Error) -> Response(error_message_key='error', status=422):
        return self.response(message=str(e))
