from utilmeta import UtilMeta
from config.env import env
import os


def configure(service: UtilMeta):
    from utilmeta.core.server.backends.django import DjangoSettings
    from utilmeta.core.orm import DatabaseConnections, Database
    from utilmeta.conf.time import Time
    from utilmeta.ops.config import Operations
    from utilmeta.utils import DEFAULT_SECRET_NAMES

    service.use(Operations(
        route='ops',
        database=Database(
            name='realworld_ops',
            engine='sqlite3',
        ),
        secure_only=env.PRODUCTION,
        max_backlog=10,
        trusted_hosts=[] if env.PRODUCTION else ['127.0.0.1'],
        secret_names=[*DEFAULT_SECRET_NAMES, 'token'],
        base_url=env.BASE_URL
    ))

    service.use(DjangoSettings(
        apps_package='domain',
        secret_key=env.DJANGO_SECRET_KEY
    ))
    service.use(DatabaseConnections({
        'default': Database(
            engine='postgresql',
            name=env.DATABASE_NAME,
            user=env.DATABASE_USER,
            password=env.DATABASE_PASSWORD,
        ) if env.PRODUCTION else Database(
            name=str(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conduit')),
            engine='sqlite3',
        )
    }))
    service.use(Time(
        time_zone='UTC',
        use_tz=True,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ"
    ))
