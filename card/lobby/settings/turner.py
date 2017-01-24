from go.util import DotDict

TURNER = DotDict({
    'cost':10000, 
    'max_round':4,
    'session_expire':300, #seconds
    'award_currencys':[0, 5000, 20000, 100000, 1000000],
    'statistic_id':1,
    'profit_margin':DotDict({
        'low_criteria':1.8,
        'high_criteria':2.5
        }),
    'probabilitys':DotDict({
        'player_win':[[0.6,0.6,0.27,0.1], [0.5,0.5,0.3,0.1], [0.5,0.5,0.3,0.1]],
        'player_lose':[[0.6,0.5,0.27,0.07], [0.5,0.5,0.3,0.06], [0.5,0.6,0.3,0.07]],
        'lucky_probs':[[0.6,0.6,0.27,0.1], [0.5,0.5,0.3,0.1], [0.5,0.5,0.3,0.1]],
        }),
    'newbie_rounds_criteria':30,
    'charge_interval':3600,
    'large':'LARGE',
    'small':'SMALL',
    'status':DotDict({
        'pending':'PENDING',
        'win':'WIN',
        'lose':'LOSE',
        'updating':"UPDATE"
        }),
})