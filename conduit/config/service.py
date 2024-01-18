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
    host='0.0.0.0' if env.PRODUCTION else '127.0.0.1',
    port=80 if env.PRODUCTION else 8000,
    asynchronous=True
)
configure(service)
