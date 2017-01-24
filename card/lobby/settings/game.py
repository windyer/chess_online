from go.util import DotDict

GAME = DotDict({
    'concurrency_times':6.2831852, 
    'display_concurrency':False,
    'game_min_cash':[
        {'mode':1, 'level':1, 'min_cash':0, 'max_cash':120000, 'capped_cash':100000},#Mode.CLASSIC, Level.JUNIOR
        {'mode':2, 'level':2, 'min_cash':100000, 'max_cash':-1, 'capped_cash':1000000},#Mode.JOKER, Level.SENIOR
        {'mode':3, 'level':2, 'min_cash':500000, 'max_cash':-1, 'capped_cash':2000000},#Mode.CHEAT, Level.SENIOR
        {'mode':4, 'level':1, 'min_cash':30000, 'max_cash':-1, 'capped_cash':1000000},#Mode.STRUGGLE, Level.JUNIOR
        {'mode':4, 'level':3, 'min_cash':2000000, 'max_cash':-1, 'capped_cash':20000000},#Mode.STRUGGLE, Level.SUPER
        ],
})