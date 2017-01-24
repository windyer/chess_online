# -*- coding:utf-8 -*-

__all__ = ['TaskManager', 'Task']

from collections import defaultdict
from card.core.statistics.models import StatisticItem, DailyStatisticItem

class Origin(object):
    '''
        origin definition class.
    '''

    def __init__(self, val):
        self._val = val
        self._origin_name = None

    @property
    def val(self):
        '''
            @return origin value.
        '''
        return self._val

    @property
    def name(self):
        '''
            @return origin name.
        '''
        return self._origin_name

    @name.setter
    def name(self, val):
        '''
            Set origin name in metaclass. 
        '''
        self._origin_name = val

    def __eq__(self, other):
        '''
            Only check origin value. 
        '''
        if type(other) == int:
            return self._val == other
        else:
            assert isinstance(other, Origin)
            return self._val == other.val

    def __unicode__(self):
        return self._origin_name

    def __str__(self):
        return self._origin_name

    __repr__ = __str__


class OriginBase(type):
    '''
        Metaclass of Achieve and Task.
    '''

    def __init__(cls, name, bases, attrs):
        super(OriginBase, cls).__init__(name, bases, attrs)
        cls._origins = []
        cls._initialize_origins(attrs)


    def _initialize_origins(cls, attrs):
        '''
            Initialize origin.
        '''
        for (origin_name, origin) in attrs.iteritems():
            if isinstance(origin, Origin):
                origin.name = origin_name
                cls._origins.append(origin)
        cls._origins.sort(key=lambda origin: origin.val)
        cls._origins = tuple(cls._origins)

class TaskBase(type):

    def __init__(cls, name, bases, attrs):
        super(TaskBase, cls).__init__(name, bases, attrs)
        cls._tasks = {}
        cls._task_map = defaultdict(dict)
        cls._initialize_tasks(attrs)

    def _initialize_tasks(cls, attrs):
        '''
            Initialize task.
        '''
        for task in attrs.itervalues():
            if isinstance(task, Task):
                cls._tasks[task.id] = task
                dependency = task.dependency.val
                threshold = task.threshold
                cls._task_map[dependency][threshold] = task


class Task(object):

    TOTAL_ROUNDS = Origin(val=1)
    WIN_TEN_THOUSAND_ROUNDS = Origin(val=3)
    STRUGGLE_WIN_ROUNDS = Origin(val=4)
    REPLACED_CARD_WIN_ROUNDS = Origin(val=5)
    CHARGE_MONEY = Origin(val=6)
    TURNER_ROUNDS = Origin(val=7)
    RECEIVE_GIFT_COUNT = Origin(val=8)
    SEND_GIFT_COUNT = Origin(val=9)
    TEXT_SPEAKER_TIME = Origin(val=10)
    UPDATE_AVATAR_TIME = Origin(val=11)
    FRIEND_COUNT = Origin(val=12)
    WIN_ROUNDS = Origin(val=13)
    INTEGRAL_PROFILE = Origin(val=14)
    BIND_ACCOUNT = Origin(val=15)
    THREE_WIN_TEN_THOUSAND_ROUNDS = Origin(val=16)

    __metaclass__ = OriginBase
    
    def __init__(self, id, name, dependency, threshold, award_currency, dependency_stat, is_daily, desc):
        assert isinstance(dependency, Origin)
        self._id = id
        self._name = name
        self._dependency = dependency
        self._threshold = threshold
        self._award_currency = award_currency
        self._dependency_stat = dependency_stat
        self._is_daily = is_daily
        self._desc = desc

    @property
    def name(self):
        return self._name

    @property
    def dependency_stat(self):
        return self._dependency_stat

    @property
    def desc(self):
        return self._desc
        
    @property
    def id(self):
        return self._id

    @property
    def is_daily(self):
        return self._is_daily

    @property
    def threshold(self):
        return self._threshold

    @property
    def dependency(self):
        return self._dependency

    @property
    def award_currency(self):
        return self._award_currency

    @classmethod
    def dependencys(cls):
        '''
        @return all the dependencys in order.
        '''
        return cls._origins

    def can_award(self, value):
        return value >= self.threshold

    def __str__(self):
        return '[id:{0}|name:{1}|dependency:{2}|threshold:{3}|award_currency:{4}]'.format(
                self.id, self.name, self.dependency.name, self.threshold, self.award_currency)

    def __repr__(self):
        return str(self)


class TaskManager(object):

    NO_USE1 = Task(1, '对战5局', Task.WIN_ROUNDS, 5, 2000, DailyStatisticItem, True, "在任意场中赢取5场游戏")
    NO_USE2 = Task(2, '对战20局', Task.WIN_ROUNDS, 20, 10000, DailyStatisticItem, True, "在任意场中赢取20场游戏")
    NO_USE4 = Task(4, '高级对决', Task.STRUGGLE_WIN_ROUNDS, 1, 2000, DailyStatisticItem, True, "在高级场以上赢得一场游戏")
    NO_USE5 = Task(5, '赌王在线', Task.REPLACED_CARD_WIN_ROUNDS, 1, 5000, DailyStatisticItem, True, "通过换牌赢取一场游戏")
    NO_USE6 = Task(6, '淘金达人', Task.CHARGE_MONEY, 6, 6000, DailyStatisticItem, True, "在商城中充值超过6元")
    NO_USE8 = Task(7, '一翻万金', Task.TURNER_ROUNDS, 1, 1000, DailyStatisticItem, True, "累计玩1次翻牌比大小")
    NO_USE102 = Task(102, '百人大战', Task.THREE_WIN_TEN_THOUSAND_ROUNDS, 1, 10000, DailyStatisticItem, True, "百人大战中赢得1万金币")

    NO_USE10 = Task(10, '初来炸到', Task.WIN_ROUNDS, 5, 2500, StatisticItem, False, "在任意场中赢取5场游戏")
    NO_USE11 = Task(11, '秀出真我', Task.INTEGRAL_PROFILE, 1, 1000, StatisticItem, False, "将个人信息填写完整")
    NO_USE12 = Task(12, '小喇叭', Task.TEXT_SPEAKER_TIME, 3, 10000, StatisticItem, False, "使用小喇叭发送三次消息")
    NO_USE13 = Task(13, '以礼相待', Task.SEND_GIFT_COUNT, 1, 2000, StatisticItem, False, "送给其他玩家一个礼物")
    NO_USE14 = Task(14, '礼尚往来', Task.RECEIVE_GIFT_COUNT, 1, 2500, StatisticItem, False, "收到一个礼物")
    NO_USE15 = Task(15, '金花秀场', Task.UPDATE_AVATAR_TIME, 1, 1000, StatisticItem, False, "成功上传个人图片")
    NO_USE16 = Task(16, '广交牌友', Task.FRIEND_COUNT, 3, 5000, StatisticItem, False, "加满3个好友")

    __metaclass__ = TaskBase

    @classmethod
    def tasks(cls):
        '''
        @return all the tasks.
        '''
        return cls._tasks

    @classmethod
    def dependencys(cls, dependency_val):
        '''
        @return all the tasks for one dependency.
        '''
        if dependency_val not in cls._task_map:
            return
        return cls._task_map[dependency_val]

    @classmethod
    def dependency_threshold(cls, dependency_val, threshold):
        '''
        @return  the typical task.
        '''
        if (dependency_val not in cls._task_map or 
            threshold not in cls._task_map[dependency_val]):
            return None
        return cls._task_map[dependency_val][threshold]
