from utilmeta.types import *
from utilmeta.utils import *
from domain.user.schema import ProfileSchema
from domain.user.models import User


class BaseContentSchema(Schema):
    body: str
    created_at: datetime
    updated_at: datetime
    author: ProfileSchema
    public: bool = Field(readonly=True)


class CommentSchema(BaseContentSchema):
    pass


class ArticleSchema(BaseContentSchema):
    slug: str = Field(readonly=True, allow_creation=False, require=False)
    title: str = ''
    description: str
    tag_list: List[str] = Field('tags.name', readonly=False, allow_creation=True, default=list)
    favorites_count: int = exp.Count('favorited_bys')

    favorited: bool = Field(request_expression=lambda request: exp.Exists(
        User.objects.filter(pk=request.user_id, favorites=exp.OuterRef('pk'))
    ))

    # favorited: bool = Field(request_expression=lambda request: exp.Count(
    #     'id', filter=exp.Q(favorited_bys=request.user)))

    comments: List[CommentSchema] = Field(retain=False, module='CommentMain', mount=True)
