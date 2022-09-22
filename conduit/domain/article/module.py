from utilmeta.types import *
from utilmeta.utils import *
from .models import Article, Comment, Tag
from .schema import ArticleSchema, CommentSchema
from config.env import env


class ArticleMain(Module):
    model = Article
    schema = ArticleSchema
    option = Option(
        filters={
            'tag': Filter(field='tags.name'),
            'author': Filter(field='author.username'),
            'favorited': Filter(field='favorited_bys.username'),
        },
        auto_user_field=model.author,
        path_param_field=model.slug,
        path_param_rule=Rule(regex='[a-z0-9-]+')
    )
    method = Method(
        get=Page(offset=True),
        put=(
            Auth(relate=model.author),
            Schema.Options(ignore_required=True)  # for PUT method, realworld spec treat every field optional
        ),
        post=Auth(login=True),
        delete=Auth(relate=model.author)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []

    @api.before(method.POST, method.PUT)
    def gen_slug_and_tags(self, data: schema):
        if data.title:
            data.slug = '-'.join([''.join(filter(str.isalnum, v)) for v in data.title.split()]).lower()
            while self.filter(slug=data.slug).exclude(id=self.pk).exists():
                data.slug += '1'    # use to avoid slug conflict
        for name in data.tag_list:
            slug = '-'.join([''.join(filter(str.isalnum, v)) for v in name.split()]).lower()
            tag, created = Tag.objects.update_or_create(slug=slug, defaults=dict(name=name))
            self.tags.append(tag)

    @api.get
    def feed(self, limit: int = None, offset: int = None) -> List[schema]:
        if not self.user_id:
            return []
        self.queryset = self.queryset.filter(author__followers=self.user)
        self.apply_slice(limit=limit, offset=offset)
        return self.serialize()

    @api.post('{slug}/favorite', request=Request(login=True))
    def favorite(self, article: model):
        article.favorited_bys.add(self.user)

    @api.delete('{slug}/favorite', request=Request(login=True))
    def unfavorite(self, article: model):
        article.favorited_bys.remove(self.user)

    @api.before(method.GET, feed)
    def filter_public(self):
        if env.PUBLIC_ONLY:
            # only display public content or self-created content
            self.queryset = self.queryset.filter(exp.Q(public=True) | exp.Q(author_id=self.user_id))

    @api.after(method.GET, feed)
    def multi_result(self) -> Response(
        result_data_key='articles',
        total_count_key='articlesCount',
        description='list of objects when path param [slug] is not provided',
        name='list'
    ): pass

    @api.after(method.GET, method.PUT, method.POST, favorite, unfavorite)
    def sole_result(self, article: model) -> Response(
        schema, name='object',
        result_data_key='article',
        description='single object when path param [slug] is provided or new object is created'
    ):
        if self.tags:
            article.tags.set(self.tags)
        return self.object  # should read (serialize()) after tags was add


class CommentMain(Module):
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
    def alter_result(self) -> Response(List[schema], result_data_key='comments'): pass

    @api.after(method.POST)
    def add_result(self, result: schema) -> Response(schema, result_data_key='comment'):
        return result
