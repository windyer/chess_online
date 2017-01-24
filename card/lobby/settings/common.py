from go.util import DotDict

CACHE_REDIS = DotDict({
    'host': 'localhost',
    'port': 13379,
    'db': 2,
})

PERSIST_REDIS = DotDict({
    'host': 'localhost',
    'port': 13380,
    'db': 2,
})

DATA = DotDict({
    'host': 'localhost',
    'port': 10089,
})

CHAT_SERVER = DotDict({
    'host': 'localhost',
    'port': 10010,
})

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

SHORT_DATE_FORMAT = 'Y.m.d'
SHORT_DATETIME_FORMAT = 'Y.m.d H:i'

TIME_FORMAT = 'H:i'
YEAR_MONTH_FORMAT = 'Y.m'
MONTH_DAY_FORMAT = 'm.d'

FIRST_DAY_OF_WEEK = 1

SECONDS_ONE_DAY = 60 * 60 * 24
UTC_OFFSET = 60 * 60 * 8

LOGGER_DB = "card.logger"
GEOIP_FILE = 'conf/GeoLite2-City.mmdb'
SENSITIVE_WORDS_FILE = 'conf/sensitive_words.conf'

TIMEOUT = DotDict({
    'lock_timeout': 5, #seconds           
})