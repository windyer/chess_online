# -*- coding:utf-8 -*-
from go.util import DotDict
from card.core.property.three import Property

HOLYTREE = DotDict({
    'deactived_device_set_key':"DEACTIVED_DEVICE_SET",
    'incompatible_versions':DotDict({
        'mmZFT':['0.8'],
        'qmBZW':['0.8'],
        }),
    'create_ip_limition':DotDict({
        'ip_count':DotDict({
            'active':True,
            'start_hour':0,
            'end_hour':6,
            "prefix_count":2,
            'ip_hash_key':"PLAYER_CREATE_IP_HASH:{0}",
            'ip_hash_key_expire':60*60,
            'max_ip_create_count':10,
            }),
        'ip_frequency':DotDict({
            'active':True,
            'create_ip_prefix':'HOLYTREE:CREATE:ACCOUNT:IP:{0}', 
            'interval':100,
            }),
        'black_ip':DotDict({
            'active':True,
            'black_ip_set_key':'HOLYTREE:BLACK:IP:SET',
            }),
        }),
    'login_ip_limitation':DotDict({
        'black_ip': DotDict({
            "active":True,
            'black_ip_set_key': 'HOLYTREE:LOGON:BLACK:IP:SET',
            }),
        "ip_net":DotDict({
            "active":True,
            "ttl": 60*60,
            "max_count":30,
            "prefix_count":2,
            'hash_key':"PLAYER_LOGON_IP_NET_HASH:{0}",
            }),
        "ip_adress":DotDict({
            "active":True,
            "ttl": 60*60*24,
            "max_count":10,
            'hash_key':"PLAYER_LOGON_IP_ADDRESS_HASH:{0}",
            }),
        }),
    'create_device_limition':DotDict({
        'device_count':DotDict({
            'active':True,
            'device_create_count':7,
            'create_device_key':'HOLYTREE:CREATE:ACCOUNT:DEVICE', 
            }),
        'white_device':DotDict({
            'active':True,
            'device_set_key':'HOLYTREE:WHITE:CREATE:DEVICE:SET',
            }),
        }),
    'version_limition':DotDict({
        'active':True,
        'disable_versions':[u"1.0.0", u"1.0.1", u"1.0.2", u"1.1.0", u"1.2.0",]
        }),
    'api_view_available':False,
    'need_validate_form':True,
    'exclude_suffixs':[u"'s iPhone", u"'s iPad", u"'s iPod", 
                        u"’s iPhone", u"’s iPad", u"’s iPod",
                        u"的 iPhone", u"的 iPad", u"的 iPod"],
    'silent_user_interval': {'minutes': 30},
    'reset_password': DotDict({
        "token_expire_time": 86400,
        "forget_password_interval":60,
        "last_forget_password_key": "HOLYTREETECH:FORGET:PASSWORD:HASH",
        "url_prefix": "http://120.27.103.99/three/holytree/password/reset/?token={0}",
        "token_key_prefix": "HOLYTREETECH:FORGET:PASSWORD:{0}:{1}",
        'subject': u'全民豹子王密码重置! ',
        'context': u'''您好, 感谢您对全民豹子王的热爱, 请尽快点击如下链接重置密码!\n 重置密码链接地址:{0}''',
        }),
    'aes_keys':DotDict({
        "default":"E29A77E9900B0ECDB162DF4E1FEEFF9D",
        '1.0.0':"E29A77DF900B0ECDB162DF4E1FEEFF9D",
        '1.0.1':"E29A77DF900B0ECDB162DF4E1FEEFF9D",
        '1.0.2':"E29A77DF900B0ECDB162DF4E1FEEFF9D",
        }),
    'check_email':DotDict({
        "token_expire_time": 3600,
        "url_prefix": "http://120.27.103.99/three/holytree/check_email/?parameter={0}",
        "token_key_prefix": "HOLYTREETECH:CHECK:EMAIL:{0}:{1}",
        'subject': u'全民豹子王邮箱绑定! ',
        'context': u'''亲爱的用户您好:\n     感谢您对全民豹子王的热爱, 请尽快点击如下链接邮箱绑定!(为保证您的账户安全请在1个小时内完成)
        \n 邮箱绑定链接地址:{0}''',
        }),
  })
