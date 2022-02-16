from utilmeta.service import UtilMeta
from config.conf import config

if __name__ == '__main__':
    UtilMeta(config=config).serve()
