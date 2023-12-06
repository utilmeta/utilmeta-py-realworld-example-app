from utilmeta import UtilMeta
from config.conf import configure
from config.env import env
import fastapi
# import django
import sys

__all__ = ['service']

service = UtilMeta(
    __name__,
    name='conduit',
    description='Realworld DEMO - conduit',
    backend=fastapi,
    production=env.PRODUCTION,
    version=(0, 1, 0),
    host='0.0.0.0' if env.PRODUCTION else '127.0.0.1',
    port=80 if env.PRODUCTION else 8000,
    background='-b' in sys.argv,
    asynchronous=True
)
configure(service)
