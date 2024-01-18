from django.db import models
from utilmeta.core.orm.backends.django import models as amodels


class BaseContent(amodels.AwaitableModel):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # public = models.BooleanField(default=False)
    author_id: int

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Tag(amodels.AwaitableModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Article(BaseContent):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    author = models.ForeignKey('user.User', on_delete=amodels.ACASCADE, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles')


class Comment(BaseContent):
    article = models.ForeignKey(Article, related_name='comments', on_delete=amodels.ACASCADE)
    author = models.ForeignKey('user.User', on_delete=amodels.ACASCADE, related_name='comments')
