from utilmeta import UtilMeta
from config.env import env


def configure(service: UtilMeta):
    from utilmeta.core.server.backends.django import DjangoSettings
    from utilmeta.core.orm import DatabaseConnections, Database
    from utilmeta.conf.time import Time
    from utilmeta.ops.config import Operations

    service.use(Operations(
        route='ops',
        database=Database(
            name='realworld_ops',
            engine='sqlite3',
        ),
        secure_only=env.PRODUCTION,
        max_backlog=50 if env.PRODUCTION else 50,
        trusted_hosts=[] if env.PRODUCTION else ['127.0.0.1']
    ))

    service.use(DjangoSettings(
        apps_package='domain',
        secret_key=env.DJANGO_SECRET_KEY
    ))
    service.use(DatabaseConnections({
        'default': Database(
            name='conduit',
            engine='sqlite3',
        )
    }))
    service.use(Time(
        time_zone='UTC',
        use_tz=True,
        datetime_format="%Y-%m-%dT%H:%M:%S.%fZ"
    ))
