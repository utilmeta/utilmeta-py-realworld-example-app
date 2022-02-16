from utilmeta import conf
conf.BACKGROUND = True

from config.conf import config
from utilmeta.service import UtilMeta

service = UtilMeta(config=config)
service.resolve()
# YOU MUST IMPORT UTILS AFTER SERVICE RESOLVE

# config your alert settings here
from utilmeta.utils import Alert
config.alert.add(
    Alert(
        Alert.cpu_percent,
        threshold=80, level=Alert.Level.CRITICAL
    ),
    Alert(
        Alert.memory_percent,
        threshold=80, level=Alert.Level.CRITICAL
    ),
    Alert(
        Alert.disk_percent,
        threshold=80, level=Alert.Level.WARNING
    ),
    Alert(
        Alert.db_server_connections_percent('default'),
        threshold=60, level=Alert.Level.CRITICAL
    ),
    Alert(
        Alert.error_percent_in_requests(100),
        threshold=50, level=Alert.Level.CRITICAL
    ),
    interval=120    # seconds
)

if __name__ == '__main__':
    service.run()
