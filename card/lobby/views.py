from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.conf import settings

from card.lobby.aop import api_view_available

@api_view(('GET',))
@api_view_available()
def root_api(request, format=None):
    """
        This is the entry point for the API described in the
        Follow the hyperinks each resource offers to explore the API.
        Note that you can also explore the API from the command line,
        for instance using the `curl` command-line tool.
        For example: `curl -X GET http://restframework.herokuapp.com/
        -H "Accept: application/json; indent=4"`
    """
    api = {
        'friend': reverse('friend', request=request, format=format),
        'game': reverse('game', request=request, format=format),
        'player': reverse('player', request=request, format=format),
        'rank': reverse('rank', request=request, format=format),
        'store': reverse('store', request=request, format=format),
        'timeline' : reverse('timeline', request=request, format=format),
        'chat': reverse('chat', request=request, format=format),
        'task': reverse('task', request=request, format=format),
        'update': reverse('update', request=request, format=format),
        'freebie': reverse('freebie', request=request, format=format),
        'activity': reverse('activity', request=request, format=format),
        'daily': reverse('daily', request=request, format=format),
        'holytree': reverse('holytree', request=request, format=format),
        'skypay': reverse('skypay', request=request, format=format),
        'mobile': reverse('mobile', request=request, format=format),
        'iapppay': reverse('iapppay', request=request, format=format),
        'turner': reverse('turner', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'three': reverse('three', request=request, format=format),
        'fruit': reverse('fruit', request=request, format=format),
        'roulette': reverse('roulette', request=request, format=format),
        'lottery': reverse('lottery', request=request, format=format),
        'baidu': reverse('baidu', request=request, format=format),
        'zhuoyi': reverse('zhuoyi', request=request, format=format),
        'wiipay': reverse('wiipay', request=request, format=format),
        'youku': reverse('youku', request=request, format=format),
        'dianyou': reverse('dianyou', request=request, format=format),
        'yuyang': reverse('yuyang', request=request, format=format),
        'api': reverse('api', request=request, format=format),
        'chubao': reverse('chubao', request=request, format=format),
        'coolpad': reverse('coolpad', request=request, format=format),
        'luckbag': reverse('luckbag', request=request, format=format),
        'dianxin': reverse('dianxin', request=request, format=format),
        'cat2currency': reverse('cat2currency', request=request, format=format),
        'moguwan': reverse('moguwan', request=request, format=format),
        'appchina': reverse('appchina', request=request, format=format),
        'ysdk': reverse('ysdk', request=request, format=format),
        'huawei': reverse('huawei', request=request, format=format),
        'invite': reverse('invite', request=request, format=format),
        }
        
    return Response(api)
