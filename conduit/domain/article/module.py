from utilmeta.types import *
from utilmeta.utils import *
from .models import Article, Comment, Tag
from .schema import ArticleSchema, CommentSchema
from config.env import env


class ArticleMain(Module):
    model = Article
    schema = ArticleSchema
    option = Option(
        path_param_field=model.slug,
        filters={
            'tag': Filter(field='tags.name'),
            'author': Filter(field='author.username'),
            'favorited': Filter(field='favorited_bys.username'),
        },
        auto_user_field=model.author
    )
    method = Method(
        get=Page(offset=True, all=True),
        put=Auth(relate=model.author),
        post=Auth(login=True),
        delete=Auth(relate=model.author)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []

    @api.before(method.POST, method.PUT)
    def gen_slug_and_tags(self, data: schema):
        if data.title:
            data.slug = '-'.join([v for v in data.title.split()]).lower()
        for name in data.tag_list:
            slug = '-'.join([v for v in name.split()]).lower()
            tag, created = Tag.objects.update_or_create(slug=slug, defaults=dict(name=name))
            self.tags.append(tag)

    @api.get(request=Request(login=True), option=Option(path_param_field=None))
    def feed(self) -> List[schema]:
        self.queryset = self.queryset.filter(author__followers=self.user)
        self.query_count = self.count
        return self.serialize()

    @api.before(feed, method.GET)
    def filter_public(self):
        if env.PUBLIC_ONLY:
            # only display public content or self-created content
            self.q = self.q.filter(exp.Q(public=True) | exp.Q(author_id=self.user_id))

    @api.post(request=Request(login=True))
    def favorite(self, article: model):
        article.favorited_bys.add(self.user)

    @api.delete(favorite, request=Request(login=True))
    def unfavorite(self, article: model):
        article.favorited_bys.remove(self.user)

    @api.after(method.GET, feed)
    def alter_result(self, result) -> Response(
        result_data_key='articles',
        total_count_key='articlesCount',
        name='multi'
    ): pass

    @api.after(method.GET, method.PUT, method.POST, favorite, unfavorite)
    def add_result(self, article: model) -> Response(schema, result_data_key='article', name='sole'):
        if self.tags:
            article.tags.set(self.tags)
        return self.object


class CommentMain(Module, register=True):
    model = Comment
    schema = CommentSchema
    option = Option(
        path_param_field='id',
        auto_user_field=model.author
    )
    method = Method(
        get=Auth(),
        post=Auth(login=True),
        delete=Auth(relate=model.author)
    )

    @api.before(method.GET)
    def filter_public(self):
        if env.PUBLIC_ONLY:
            # only display public content or self-created content
            self.q = self.q.filter(exp.Q(public=True) | exp.Q(author_id=self.user_id))

    @api.after(method.GET)
    def alter_result(self) -> Response(List[schema], result_data_key='comments', name='multi'): pass

    @api.after('*', excludes=method.DELETE)     # mark as one=True
    def add_result(self, target: model) -> Response(schema, result_data_key='comment', name='sole'):
        return self.object if target else None
