from utilmeta.conf import Env


class ServiceEnvironment(Env):
    PRODUCTION: bool = False
    JWT_SECRET_KEY: str = ''
    DJANGO_SECRET_KEY: str = ''
    BASE_URL: str = ''


env = ServiceEnvironment(sys_env='CONDUIT_')
