from config.conf import config
from utilmeta.service import UtilMeta

service = UtilMeta(config=config)

wsgi = service.wsgi()
