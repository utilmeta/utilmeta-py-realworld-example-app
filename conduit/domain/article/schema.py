from utype.types import *
from utilmeta.core import orm
from domain.user.schema import ProfileSchema
from domain.user.models import Favorite
from .models import Comment, Article
from ..base import BaseORMSchema
from django.db import models


class BaseContentSchema(BaseORMSchema):
    body: str
    created_at: datetime
    updated_at: datetime
    author: ProfileSchema
    # public: bool = orm.Field(readonly=True)
    author_id: int = orm.Field(mode='a', no_input=True)


class CommentSchema(BaseContentSchema[Comment]):
    id: int = orm.Field(mode='r')
    article_id: int = orm.Field(mode='a', no_input=True)


class ArticleSchema(BaseContentSchema[Article]):
    id: int = orm.Field(no_input=True)
    slug: str = orm.Field(no_input='aw', default=None, defer_default=True)
    title: str = orm.Field(default='', defer_default=True)
    description: str = orm.Field(default='', defer_default=True)
    tag_list: List[str] = orm.Field('tags.name', mode='rwa', no_output='aw', default_factory=list)
    favorites_count: int = models.Count('favorited_bys')
    favorited: bool = orm.Field(mode='r', default=False)
    # to be inherited

    async def check_slug(self):
        if self.title:
            self.slug = '-'.join(filter(bool, [''.join(filter(str.isalnum, v)) for v in self.title.split()])).lower()
            while await Article.objects.filter(slug=self.slug).exclude(id=self.pk).aexists():
                self.slug += '1'  # use to avoid slug conflict

    @classmethod
    def get_runtime(cls, user_id):
        if not user_id:
            return cls

        class ArticleRuntimeSchema(cls):
            favorited: bool = models.Exists(
                Favorite.objects.filter(article=models.OuterRef('pk'), user=user_id)
            )

        return ArticleRuntimeSchema

    def __validate__(self):
        self.tag_list.sort()
