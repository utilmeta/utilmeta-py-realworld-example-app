from utilmeta.core import orm
import utype
from utype.utils.style import AliasGenerator


class BaseORMSchema(orm.Schema):
    __options__ = utype.Options(alias_generator=AliasGenerator.camel)
