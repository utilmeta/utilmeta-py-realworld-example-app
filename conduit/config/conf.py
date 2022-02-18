from utilmeta import conf
from config.env import env
from utilmeta.util.common import Format
from utilmeta.util.parser.base import Options
from datetime import timedelta

config = conf.Config(
    __name__,
    name='conduit',
    description='Realworld example app service',
    host=conf.Host(
        product=f'realworld{env.TEST_ENV_SUFFIX}.utilmeta.com',
        develop='127.0.0.1:9090'
    ),
    root_api='service.api.RootAPI',
    root_url='api',
    apps_dir='domain',
    production=env.PRODUCTION,
    middlewares=conf.DEFAULT_MIDDLEWARES,
    preference=conf.Preference(
        base_parser_options=Options(alias_from_case_styles='camelCase'),
        param_offset_name='offset',
        param_limit_name='limit',
    ),
    auth=conf.Auth(
        user_model='user.User',
        login_fields='email',
        jwt_token_field='token',
        auth_strategy=conf.Auth.JWT,
        jwt_secret_key=env.JWT_SECRET_key
    ),
    task=conf.Task(
        main_cycle_interval=30,
        worker_cycle_interval=15,
        console_log_execution=not env.PRODUCTION,
        max_instance_memory=0.3,
        max_worker_memory=200 * 1024 ** 2,
        min_interval=3,
        max_workers=conf.Task.MAX_WORKERS,
        max_worker_tasks=10,
        min_worker_tasks=3,
        concurrent_cls=conf.Task.THREAD_POOL      # or conf.Task.GEVENT_POOL for gevent backend
    ),
    ops=conf.Operations(
        db='ops',
        cache='default',
        route='ops',
        token=env.OPS_TOKEN,
        supervisor_secure=env.PRODUCTION,
        supervisor_authorized=env.PRODUCTION
    ),
    monitor=conf.Monitor(
        server_monitor_interval=60,
        worker_monitor_interval=20,
    ),
    alert=conf.Alert(
        default_interval=60,
    ),
    log=conf.Log(
        data_store_level=conf.Log.WARN,
        result_store_level=conf.Log.WARN,
        query_store_time_limit=timedelta(milliseconds=600),
        maintain=timedelta(days=7),
        parse_user_agent=True,
    ),
    databases={
        'default': conf.Database(
            engine=conf.Database.POSTGRESQL,
            name='realworld',
            user=env.DATABASE_USER,
            password=env.DATABASE_PASSWORD
        ) if env.PRODUCTION else conf.Database(
            engine=conf.Database.SQLITE,
            name='realworld_demo',
        ),
        'ops': conf.Database(
            engine=conf.Database.POSTGRESQL,
            name='realworld_ops',
            user=env.DATABASE_USER,
            password=env.DATABASE_PASSWORD
        ) if env.PRODUCTION else conf.Database(
            engine=conf.Database.SQLITE,
            name='realworld_demo_ops',
        ),
    },
    caches={
        'default': conf.Cache(
            backend=conf.Cache.REDIS,
            password=env.REDIS_PASSWORD,
            redis_config=conf.Cache.Redis(
                '/etc/redis/redis.conf',
                daemonize=True,
            )
        ) if env.PRODUCTION else conf.Cache(
            backend=conf.Cache.FILE
        )
    },
    time=conf.Time(
        datetime_format=Format.DATETIME_TFZ,
        date_format=conf.Time.DATE_DEFAULT,
        time_zone=conf.Time.TimeZone.UTC,
        use_tz=False
    ),
    deploy=conf.Deploy(
        socket=conf.Deploy.AUTO_FILE,
        # worker_class=conf.UWSGI.GEVENT,
        # worker_connections=1000,
        https=True,
        wsgi_server=conf.UWSGI('uwsgi.ini'),
        web_server=conf.Nginx('conf.nginx', link='/etc/nginx/sites-enabled/realworld-example-app.conf',
                              main='/etc/nginx/nginx.conf'),
        auto_reload=False,
        index_file='index.html',
        static_url='/',
    )
)
