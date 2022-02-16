from utilmeta.fields import *


class BaseContent(Model):
    body = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    public = BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Tag(Model):
    name = CharField(max_length=255)
    slug = SlugField(db_index=True, unique=True)
    created_at = DateTimeField(auto_now_add=True)


class Article(BaseContent):
    slug = SlugField(db_index=True, max_length=255, unique=True)
    title = CharField(db_index=True, max_length=255)
    description = TextField()
    author = ForeignKey('user.User', on_delete=CASCADE, related_name='articles')
    tags = ManyToManyField(Tag, related_name='articles')


class Comment(BaseContent):
    article = ForeignKey(Article, related_name='comments', on_delete=CASCADE)
    author = ForeignKey('user.User', on_delete=CASCADE, related_name='comments')
