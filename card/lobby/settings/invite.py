#coding=utf-8
from go.util import DotDict
INVITE=DotDict({
    'off_invite_channel':['zx001','zx002','zx003','zx004','zx005_phone',
                'zx005_91','zx006','zx007','zx010','zx011','zx014','zx016','zx017',
                'zx020', 'zx009', 'zx018', 'zx021', 'zx022', 'zx023',
                'zx025', 'zx027', 'zx012'],
    'enable_invite':True,
    'redis_hash_key':'INVITER:INFO:{0}',
    'redis_list_key':'INVITER:LIST:{0}',
    'redis_bull_key':'INVITER:BULL',
    'first_award_ratio':10000*0.16,
    'second_award_ratio': 10000 * 0.08,
    'QR_code':'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/qr_code.png',
    'down_url':'https://at.umeng.com/0LvOLz',
    'reason':'invite_award',
    'award_info':u'{0}通过邀请好友加入已获得{1}万金币奖励',
})