from utilmeta.types import *
from utilmeta.utils import *
from utilmeta.core.sdk import BaseResponse


class ArticlesCommentsSDK(SDK):
	class GetMultiResponse(BaseResponse):
		class GetMultiResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			public: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'multi'
		result: List[GetMultiResultSchema]
		__params__ = Response(result_data_key='comments')

	class GetSoleResponse(BaseResponse):
		class GetSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			public: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: GetSoleResultSchema
		__params__ = Response(result_data_key='comment')

	class GetBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class PostBodySchema(Schema, isolate=True):
		def __init__(
			self,
			body: 'str',
			public: 'bool' = None
		): super().__init__(locals())

	class PostSoleResponse(BaseResponse):
		class PostSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			public: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: PostSoleResultSchema
		__params__ = Response(result_data_key='comment')

	class PostBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class DeleteBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.get('articles/{slug}/comments/{id}', idempotent=True)
	def get(
		self,
		id: 'int' = Rule(require=False, ge=1, le=2147483647),
		slug: 'str' = Rule(require=False, max_length=255)
	) -> Union[GetMultiResponse, GetSoleResponse, GetBadrequestResponse]: pass

	@api.post('articles/{slug}/comments', idempotent=False)
	def post(
		self,
		slug: 'str' = Rule(require=False, max_length=255),
		data: PostBodySchema = Request.Body
	) -> Union[PostSoleResponse, PostBadrequestResponse]: pass

	@api.delete('articles/{slug}/comments/{id}', idempotent=True)
	def delete(
		self,
		id: 'int' = Rule(require=False, ge=1, le=2147483647),
		slug: 'str' = Rule(require=False, max_length=255)
	) -> Union[BaseResponse, DeleteBadrequestResponse]: pass


class ArticlesFavoriteSDK(SDK):
	class PostSoleResponse(BaseResponse):
		class PostSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: PostSoleResultSchema
		__params__ = Response(result_data_key='article')

	class DeleteSoleResponse(BaseResponse):
		class DeleteSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: DeleteSoleResultSchema
		__params__ = Response(result_data_key='article')

	@api.post('articles/{slug}/favorite', idempotent=False)
	def post(
		self,
		slug: 'str' = Rule(require=False, max_length=255)
	) -> PostSoleResponse: pass

	@api.delete('articles/{slug}/favorite', idempotent=True)
	def delete(
		self,
		slug: 'str' = Rule(require=False, max_length=255)
	) -> DeleteSoleResponse: pass


class ArticlesSDK(SDK):
	favorite = ArticlesFavoriteSDK()
	comments = ArticlesCommentsSDK()

	class GetMultiResponse(BaseResponse):
		class GetMultiResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
		name = 'multi'
		result: List[GetMultiResultSchema]
		__params__ = Response(result_data_key='articles', total_count_key='articlesCount')

	class GetSoleResponse(BaseResponse):
		class GetSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: GetSoleResultSchema
		__params__ = Response(result_data_key='article')

	class GetBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class PutBodySchema(Schema, isolate=True):
		def __init__(
			self,
			body: 'str',
			description: 'str',
			title: 'str' = '',
			tag_list: List['str'] = None
		): super().__init__(locals())

	class PutSoleResponse(BaseResponse):
		class PutSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: PutSoleResultSchema
		__params__ = Response(result_data_key='article')

	class PutBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class PostBodySchema(Schema, isolate=True):
		def __init__(
			self,
			body: 'str',
			description: 'str',
			public: 'bool' = None,
			title: 'str' = '',
			tag_list: List['str'] = None
		): super().__init__(locals())

	class PostSoleResponse(BaseResponse):
		class PostSoleResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'sole'
		result: PostSoleResultSchema
		__params__ = Response(result_data_key='article')

	class PostBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class DeleteBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class FeedMultiResponse(BaseResponse):
		class FeedMultiResultSchema(Schema, isolate=True):
			class AuthorSchema(Schema):
				username: 'str'
				bio: 'str'
				image: 'str'
				following: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)

			class CommentsSchema(Schema, isolate=True):
				class AuthorSchema1(Schema):
					username: 'str'
					bio: 'str'
					image: 'str'
					following: 'bool' = Rule(require=False)
					id: 'int' = Rule(require=False)
				body: 'str'
				created_at: 'datetime'
				updated_at: 'datetime'
				author: AuthorSchema1
				public: 'bool' = Rule(require=False)
				id: 'int' = Rule(require=False)
			body: 'str'
			createdAt: 'datetime'
			updatedAt: 'datetime'
			author: AuthorSchema
			description: 'str'
			public: 'bool' = Rule(require=False)
			slug: 'str' = Rule(require=False)
			title: 'str' = Rule(require=False)
			tagList: List['str'] = Rule(require=False)
			favoritesCount: 'int' = Rule(require=False)
			favorited: 'bool' = Rule(require=False)
			comments: List[CommentsSchema] = Rule(require=False)
			id: 'int' = Rule(require=False)
		name = 'multi'
		result: List[FeedMultiResultSchema]
		__params__ = Response(result_data_key='articles', total_count_key='articlesCount')

	class FeedBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.get('articles/{slug}', idempotent=True)
	def get(
		self,
		slug: 'str' = Rule(require=False, max_length=255),
		tag: 'str' = Rule(require=False, max_length=255),
		author: 'str' = Rule(require=False, max_length=40),
		favorited: 'str' = Rule(require=False, max_length=40),
		offset: 'int' = Rule(require=False, ge=0),
		limit: 'int' = Rule(require=False, ge=0)
	) -> Union[GetMultiResponse, GetSoleResponse, GetBadrequestResponse]: pass

	@api.put('articles/{slug}', idempotent=True)
	def put(
		self,
		slug: 'str' = Rule(require=False, max_length=255),
		tag: 'str' = Rule(require=False, max_length=255),
		author: 'str' = Rule(require=False, max_length=40),
		favorited: 'str' = Rule(require=False, max_length=40),
		data: PutBodySchema = Request.Body
	) -> Union[PutSoleResponse, PutBadrequestResponse]: pass

	@api.post('articles', idempotent=False)
	def post(
		self,
		data: PostBodySchema = Request.Body
	) -> Union[PostSoleResponse, PostBadrequestResponse]: pass

	@api.delete('articles/{slug}', idempotent=True)
	def delete(
		self,
		slug: 'str' = Rule(require=False, max_length=255),
		tag: 'str' = Rule(require=False, max_length=255),
		author: 'str' = Rule(require=False, max_length=40),
		favorited: 'str' = Rule(require=False, max_length=40)
	) -> Union[BaseResponse, DeleteBadrequestResponse]: pass

	@api.get('articles/feed', idempotent=True)
	def feed(self) -> Union[FeedMultiResponse, FeedBadrequestResponse]: pass


class ProfilesFollowSDK(SDK):
	class PostResponse(BaseResponse):
		class PostResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			following: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		result: PostResultSchema
		__params__ = Response(result_data_key='profile')

	class DeleteResponse(BaseResponse):
		class DeleteResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			following: 'bool' = Rule(require=False)
			id: 'int' = Rule(require=False)
		result: DeleteResultSchema
		__params__ = Response(result_data_key='profile')

	@api.post('profiles/{username}/follow', idempotent=False)
	def post(
		self,
		username: 'str' = Rule(max_length=40)
	) -> PostResponse: pass

	@api.delete('profiles/{username}/follow', idempotent=True)
	def delete(
		self,
		username: 'str' = Rule(max_length=40)
	) -> DeleteResponse: pass


class ProfilesSDK(SDK):
	follow = ProfilesFollowSDK()

	class GetResponse(BaseResponse):
		class GetResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			following: 'bool' = Rule(require=False)
		result: GetResultSchema
		__params__ = Response(result_data_key='profile')

	class GetBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.get('profiles/{username}', idempotent=True)
	def get(
		self,
		username: 'str' = Rule(max_length=40)
	) -> Union[GetResponse, GetBadrequestResponse]: pass


class UsersSDK(SDK, response=Response(result_data_key='user')):
	class PostBodySchema(Schema, isolate=True):
		def __init__(
			self,
			email: 'str',
			password: 'str',
			username: 'str'
		): super().__init__(locals())

	class PostResponse(BaseResponse):
		class PostResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			email: 'str'
			token: 'str' = Rule(require=False)
			id: 'int' = Rule(require=False)
		result: PostResultSchema

	class PostBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class LoginBodySchema(Schema, isolate=True):
		def __init__(
			self,
			email: 'str',
			password: 'str'
		): super().__init__(locals())

	class LoginResponse(BaseResponse):
		class LoginResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			email: 'str'
			token: 'str' = Rule(require=False)
			id: 'int' = Rule(require=False)
		result: LoginResultSchema

	class LoginBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.post('users', idempotent=False)
	def post(
		self,
		data: PostBodySchema = Request.Body
	) -> Union[PostResponse, PostBadrequestResponse]: pass

	@api.post('users/login', idempotent=False)
	def login(
		self,
		data: LoginBodySchema = Request.Body
	) -> Union[LoginResponse, LoginBadrequestResponse]: pass


class UserSDK(SDK):
	class GetResponse(BaseResponse):
		class GetResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			email: 'str'
			token: 'str' = Rule(require=False)
		result: GetResultSchema
		__params__ = Response(result_data_key='user')

	class GetBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	class PutBodySchema(Schema, isolate=True):
		def __init__(
			self,
			username: 'str' = Rule(max_length=40),
			bio: Optional['str'] = None,
			image: Optional['str'] = None,
			email: 'str' = Rule(regex='^[a-z0-9A-Z]+[a-z0-9A-Z._-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+[a-z0-9A-Z]+$', max_length=60)
		): super().__init__(locals())

	class PutResponse(BaseResponse):
		class PutResultSchema(Schema, isolate=True):
			username: 'str'
			bio: 'str'
			image: 'str'
			email: 'str'
			token: 'str' = Rule(require=False)
			id: 'int' = Rule(require=False)
		result: PutResultSchema
		__params__ = Response(result_data_key='user')

	class PutBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.get('user', idempotent=True)
	def get(
		self,
		id: 'int' = Rule(require=False, ge=1, le=2147483647)
	) -> Union[GetResponse, GetBadrequestResponse]: pass

	@api.put('user', idempotent=True)
	def put(
		self,
		id: 'int' = Rule(require=False, ge=1, le=2147483647),
		data: PutBodySchema = Request.Body
	) -> Union[PutResponse, PutBadrequestResponse]: pass


class APIService(SDK):
	user = UserSDK()
	users = UsersSDK()
	profiles = ProfilesSDK()
	articles = ArticlesSDK()

	class TagsResponse(BaseResponse):
		result: List['str']
		__params__ = Response(result_data_key='tags')

	class TagsBadrequestResponse(BaseResponse):
		name = 'BadRequest'
		status = 422
		__params__ = Response(result_data_key='data', error_message_key='error')

	@api.get(idempotent=True)
	def tags(self) -> Union[TagsResponse, TagsBadrequestResponse]: pass


conduit = APIService(base_url='http://127.0.0.1:9090/api', version='0.1.0')
