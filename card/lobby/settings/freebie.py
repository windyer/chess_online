from datetime import datetime
from go.util import DotDict

FREEBIE = DotDict({
    'salvage_currency':10000, 
    'salvage_currency_criteria':10000,
    'salvage_interval':120,
    'max_salvage_time':3,
    'score_wall':DotDict({
        'domob':DotDict({
            'publisher_id':'96ZJ0EAAzeN2TwTAee',
            }),
        'youmi':DotDict({
            'dev_server_secret':'fb559b21cb6f1780',
            }),
        'limei':DotDict({
            'adid':'a7171ffb67e3ea0496a2bd0f152b27dd',
            }),
        }),
    'money_tree':DotDict({
        "available_time":86400,
        "award_currency":5000,
        "fetch_interval_time":3600,
        "noon_fetch_time":(datetime(2014, 4, 30, 12, 30, 0, 0), datetime(2014, 4, 30, 13, 30, 0, 0),),
        "evening_fetch_time":(datetime(2014, 4, 30, 18, 30, 0, 0), datetime(2014, 4, 30, 19, 30, 0, 0),),
        }),
})