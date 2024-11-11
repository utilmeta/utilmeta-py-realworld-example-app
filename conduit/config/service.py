from utilmeta import UtilMeta
from config.conf import configure
from config.env import env
import starlette

__all__ = ['service']

service = UtilMeta(
    __name__,
    name='conduit',
    description='Realworld DEMO - conduit',
    backend=starlette,
    production=env.PRODUCTION,
    version=(1, 0, 0),
    port=8080,
    asynchronous=True,
    api='service.api.RootAPI',
    route='/api'
)
configure(service)
