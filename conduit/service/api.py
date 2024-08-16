import utype
from utilmeta.utils import exceptions, Error
from domain.user.api import UserAPI, ProfileAPI, AuthenticationAPI
from domain.article.api import ArticleAPI
from utilmeta.core import api, response
from typing import List
from utilmeta.core.api.specs.openapi import OpenAPI


@api.CORS(allow_origin='*', allow_headers=['Authorization'])
class RootAPI(api.API):
    user: UserAPI
    users: AuthenticationAPI
    profiles: ProfileAPI
    articles: ArticleAPI

    docs: OpenAPI.as_api('openapi.json')

    class TagsSchema(utype.Schema):
        tags: List[str]

    @api.get
    async def tags(self) -> TagsSchema:
        from domain.article.models import Tag
        return self.TagsSchema(
            tags=[name async for name in Tag.objects.values_list('name', flat=True)]
        )

    class ErrorResponse(response.Response):
        message_key = 'msg'
        result_key = 'errors'

    @api.handle('*', Exception)
    def handle_errors(self, e: Error) -> ErrorResponse:
        print('ERROR:', e.type)
        print(e.full_info)
        detail = None
        exception = e.exception
        if isinstance(exception, exceptions.BadRequest):
            detail = exception.detail
            status = 422
        else:
            status = e.status
        return self.ErrorResponse(detail, error=e, status=status)
