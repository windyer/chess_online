import os
from go.util import DotDict

LOBBY = os.path.realpath(os.path.join(__file__, os.path.pardir, os.path.pardir))


LOGGING = DotDict({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': DotDict({
        'standard': DotDict({
            'format': '[%(asctime)s.%(msecs).03d] [process|%(process)d] [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }),
    }),
    'filters': DotDict({
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    }),
    'handlers': DotDict({
        'console': DotDict({
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }),
        'file': DotDict({
            'level': 'DEBUG',
            'class': 'card.core.util.mlogging.TimedRotatingFileHandler_MP',
            'when' : 'midnight',
            'interval': 1,
            'filename': os.path.join(LOBBY, '../../log/lobby.log'),
            'backupCount': 7,
            'formatter':'standard',
        }),
        'mail_admins': DotDict({
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }),
        'transaction': DotDict({
            'level': 'INFO',
            'class': 'card.core.util.mlogging.TimedRotatingFileHandler_MP',
            'when' : 'midnight',
            'interval': 1,
            'filename': 'log/lobby_transaction.log',
            'backupCount': 7,
            'formatter':'standard',
        }),
    }),
    'loggers': DotDict({
        'django.request': DotDict({
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }),
        'django.db.backends': DotDict({
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }),
        'lobby': DotDict({
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }),
        'trans_log': DotDict({
            'handlers': ['transaction'],
            'level': 'INFO',
            'propagate': False, 
        }),
    })
})
