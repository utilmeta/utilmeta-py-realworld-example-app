# from utilmeta.utils import *
from utilmeta.core import api, request, orm, response
from domain.user.models import User, Favorite
from .models import Article, Comment, Tag
from .schema import ArticleSchema, CommentSchema
from config.auth import API
from utilmeta.utils import exceptions
from typing import List, Optional


@api.route('{slug}/comments')
class CommentAPI(API):
    slug: str = request.SlugPathParam

    class ListResponse(response.Response):
        result_key = 'comments'
        name = 'list'
        result: List[CommentSchema]

    class ObjectResponse(response.Response):
        result_key = 'comment'
        name = 'object'
        result: CommentSchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article: Optional[Article] = None

    @api.get
    async def get(self) -> ListResponse:
        return self.ListResponse(
            await CommentSchema.aserialize(
                Comment.objects.filter(article=self.article)
            )
        )

    @api.post
    async def post(self, comment: CommentSchema[orm.A] = request.BodyParam,
                   user: User = API.user_config) -> ObjectResponse:
        comment.article_id = self.article.pk
        comment.author_id = user.pk
        await comment.asave()
        return self.ObjectResponse(
            await CommentSchema.ainit(comment.pk)
        )

    @api.delete('/{id}')
    async def delete_comment(self, id: int, user: User = API.user_config):
        comment = await Comment.objects.filter(
            id=id,
        ).afirst()
        if not comment:
            raise exceptions.NotFound('comment not found')
        if comment.author_id != user.pk:
            raise exceptions.PermissionDenied('permission denied')
        await comment.adelete()

    @api.before('*')
    async def handle_article_slug(self):
        article = await Article.objects.filter(slug=self.slug).afirst()     # async, so cannot merge in __init__
        if not article:
            raise exceptions.NotFound('article not found')
        self.article = article


class MultiArticlesResponse(response.Response):
    result_key = 'articles'
    count_key = 'articlesCount'
    description = 'list of objects when path param [slug] is not provided'
    name = 'multi'
    result: List[ArticleSchema]


class SingleArticleResponse(response.Response):
    result_key = 'article'
    description = 'single object when path param [slug] is provided or new object is created'
    name = 'single'
    result: ArticleSchema


class ArticleAPI(API):
    comments: CommentAPI

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []
        self.article: Optional[Article] = None

    class BaseArticleQuery(orm.Query[Article]):
        offset: int = orm.Offset(default=0)
        limit: int = orm.Limit(default=20, le=100)

    class ListArticleQuery(BaseArticleQuery):
        tag: str = orm.Filter('tags.name')
        author: str = orm.Filter('author.username')
        favorited: str = orm.Filter('favorited_bys.username')

    @api.get
    async def get(self, query: ListArticleQuery) -> MultiArticlesResponse:
        count = await query.acount()
        schema = ArticleSchema.get_runtime(
            await self.get_user_id()
        )
        return MultiArticlesResponse(
            result=await schema.aserialize(
                query.get_queryset()
            ),
            count=count
        )

    @api.get
    async def feed(self, query: BaseArticleQuery) -> MultiArticlesResponse:
        user_id = await self.get_user_id()
        if not user_id:
            return MultiArticlesResponse([], count=0)
        base_qs = Article.objects.filter(author__followers=user_id)
        count = await base_qs.acount()
        schema = ArticleSchema.get_runtime(user_id)
        return MultiArticlesResponse(
            result=await schema.aserialize(
                query.get_queryset(
                    base_qs
                )
            ),
            count=count
        )

    @api.get('/{slug}')
    async def get_article(self): pass

    @api.post('/{slug}/favorite')
    async def favorite(self, user: User = API.user_config):
        await Favorite.objects.aget_or_create(
            article=self.article,
            user=user
        )

    @api.delete('/{slug}/favorite')
    async def unfavorite(self, user: User = API.user_config):
        await Favorite.objects.filter(
            article=self.article,
            user=user
        ).adelete()

    @api.put('/{slug}')
    async def update_article(self, article: ArticleSchema[orm.WP] = request.BodyParam, user: User = API.user_config):
        if self.article.author_id != user.pk:
            raise exceptions.PermissionDenied('permission denied')
        article.id = self.article.pk
        await article.check_slug()
        await article.asave()

    @api.delete('/{slug}')
    async def delete_article(self, user: User = API.user_config):
        if self.article.author_id != user.pk:
            raise exceptions.PermissionDenied('permission denied')
        await self.article.adelete()

    @api.post
    async def post(self, article: ArticleSchema[orm.A] = request.BodyParam, user: User = API.user_config):
        article.author_id = user.pk
        await article.check_slug()
        await article.asave()
        self.article = article.get_instance()

    @api.before(get_article, favorite, unfavorite, update_article, delete_article)
    async def handle_slug(self, slug: str = request.SlugPathParam):
        article = await Article.objects.filter(slug=slug).afirst()
        if not article:
            raise exceptions.NotFound('article not found')
        self.article = article

    @api.before(post, update_article)
    async def gen_tags(self, article: ArticleSchema[orm.A] = request.BodyParam):
        for name in article.tag_list:
            slug = '-'.join([''.join(filter(str.isalnum, v)) for v in name.split()]).lower()
            tag, created = await Tag.objects.aupdate_or_create(slug=slug, defaults=dict(name=name))
            self.tags.append(tag)

    @api.after(get_article, favorite, unfavorite, update_article, post)
    async def handle_response(self) -> SingleArticleResponse:
        if not self.article:
            raise exceptions.NotFound('article not found')
        if self.tags:
            # create or set tags relation in creation / update
            await self.article.tags.aset(self.tags)
        schema = ArticleSchema.get_runtime(
            await self.get_user_id()
        )
        return SingleArticleResponse(
            await schema.ainit(self.article)
        )
