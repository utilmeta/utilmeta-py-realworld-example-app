from utilmeta.core import cli, request, api, orm, response
import utype
import asyncio
from utype.types import *
import httpx
import aiohttp


class UserSchema(utype.Schema):
    username: str
    email: str
    # password: str = orm.Field(mode='wa')
    token: str = orm.Field(mode='r')
    bio: str
    image: Optional[str] = None


class ProfileSchema(utype.Schema):
    username: str
    bio: str
    following: bool = False
    image: Optional[str] = None


class ArticleSchema(utype.Schema):
    body: str
    created_at: datetime = utype.Field(alias='createdAt')
    updated_at: datetime = utype.Field(alias='updatedAt')
    author: ProfileSchema = orm.Field(mode='r')
    slug: str = orm.Field(no_input='aw', default=None, defer_default=True)
    title: str = orm.Field(default='', defer_default=True)
    description: str = orm.Field(default='', defer_default=True)
    tag_list: List[str] = orm.Field('tags.name', mode='rwa', no_output='aw', default_factory=list)
    favorites_count: int = utype.Field(alias='favoritesCount')
    favorited: bool = False
    # to be inherited


class ArticleCreation(utype.Schema):
    body: str
    title: str
    description: str
    tag_list: List[str] = utype.Field(alias='tagList')


class UserResponse(response.Response):
    result: UserSchema
    result_key = 'user'


class ArticleResponse(response.Response):
    result: ArticleSchema
    result_key = 'article'


class LoginSchema(utype.Schema):
    email: str
    password: str

    def __init__(self, email: str, password: str):
        super().__init__(locals())


class RealworldClient(cli.Client):
    @api.get('tags')
    async def async_get_tags(self): pass

    @api.get('articles/{slug}')
    async def async_get_article(self, slug: str) -> ArticleResponse: pass

    @api.get('articles/{slug}')
    def get_article(self, slug: str) -> ArticleResponse: pass

    @api.post('articles')
    async def async_post_article(self, article: ArticleCreation = request.BodyParam) -> ArticleResponse: pass

    @api.post('articles')
    def post_article(self, article: ArticleCreation = request.BodyParam) -> ArticleResponse: pass

    @api.post('users/login')
    async def async_login(self, user: LoginSchema = request.BodyParam) -> UserResponse: pass

    @api.post('users/login')
    def login(self, user: LoginSchema = request.BodyParam) -> UserResponse: pass


def client_test():
    with RealworldClient(
        base_url='http://127.0.0.1:8000/api',
        backend=httpx
    ) as client:
        user = client.login(
            user=LoginSchema(
                email='test@mail.com',
                password='password'
            )
        )
        print('USER:', user)
        client.update_base_headers({
            'authorization': f'token {user.result.token}'
        })
        new_article = client.post_article(
            article=ArticleCreation({
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["reactjs", "angularjs", "dragons"]
          })
        )
        print('NEW ARTICLE:', new_article)
        article = client.get_article(slug=new_article.result.slug)
        print('ARTICLE:', article)


async def atest():
    with RealworldClient(
        base_url='http://127.0.0.1:8000/api',
        backend=httpx
    ) as client:
        user = await client.async_login(
            user=LoginSchema(
                email='test@mail.com',
                password='password'
            )
        )
        print('USER:', user)
        client.update_base_headers({
            'authorization': f'token {user.result.token}'
        })
        new_article = await client.async_post_article(
            article=ArticleCreation({
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["reactjs", "angularjs", "dragons"]
          })
        )
        print('NEW ARTICLE:', new_article)
        article = await client.async_get_article(slug=new_article.result.slug)
        print('ARTICLE:', article)


if __name__ == '__main__':
    # client_test()
    asyncio.run(atest())
