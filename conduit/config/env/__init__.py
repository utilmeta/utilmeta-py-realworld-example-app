from utilmeta.conf import Env


class ServiceEnvironment(Env):
    PRODUCTION: bool = False
    OPS_TOKEN: str = ''
    JWT_SECRET_key: str = ''
    DATABASE_USER: str = ''
    DATABASE_PASSWORD: str = ''
    REDIS_PASSWORD: str = ''
    PUBLIC_ONLY: bool = True
    TEST_ENV_SUFFIX: str = ''       # be -test when it's test env


env = ServiceEnvironment(__file__)
