from go.util import DotDict

BULL_URL = DotDict({
    'base_url':'http://oss.holytree.com.cn/hlnn/',
    'second_base_url':'http://oss.holytree.com.cn/hlnn/',
    'download_count_key':'BullDownloadCount',
    'download_count_pro':10.1,
    'channels':DotDict({
        #'default':DotDict({'url':'SS_HLNN_bzw_v140_20160612.apk','packType':'com.game.bullfight','url_front':'SS_AMUSEGAME_v1.2.0_20160817_bzw.apk','packType_front':'com.game.amusegame'}),
        'default':DotDict({'url_front':'SS_HLNN_bzw_v140_20160612.apk','packType_front':'com.game.bullfight','url':'SS_AMUSEGAME_v1.4.0_20161128_bzw.apk','packType':'com.game.amusegame'}),
        }),
    })
