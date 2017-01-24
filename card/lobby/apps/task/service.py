from collections import defaultdict

from card.core.conf import settings

import go.logging

from card.core.enum import Gender
from card.core.statistics.models import StatisticItem, DailyStatisticItem
from card.lobby.service.view_service import ViewService

from card.lobby.apps.task.redis import TaskStatus
from card.lobby.apps.task.tasks import TaskManager
from card.lobby.apps.player.service import PlayerService
from card.core.error.lobby.task_error import TaskError
from card.lobby.apps.timeline.service import TimeLineService

@go.logging.class_wrapper
class TaskService(ViewService):

    def __init__(self, service_repositories, activity_repository, counter_repository):
        super(TaskService, self).__init__(service_repositories, activity_repository)
        self.counter_repository = counter_repository

    def _friend_count(self, user_id):
        social_service = self.service_repositories.db.social_service
        return social_service.get_friend_count(user_id).friend_count

    def _integral_profile(self, user_id):
        player_service = self.service_repositories.db.player_service
        profile = player_service.get_profile(user_id)
        if (profile.nick_name is not None and 
            profile.gender != Gender.UNKNOWN and
            profile.signature != "" and
            profile.contact != ""):
            return True
        else:
            return False


    def get_statistics(self, user_id, dependency_stat):
        statistics = dependency_stat()
        statistics.set_id(user_id)
        resp = defaultdict(int, statistics.counters_value)
        if issubclass(dependency_stat, StatisticItem):
            resp['friend_count'] = self._friend_count(user_id)
            integral_profile = resp['integral_profile']
            if ((integral_profile is None or integral_profile == 0) and
                self._integral_profile(user_id)):
                resp['integral_profile'] = 1
                for counter in self.counter_repository.counters:
                    counter.incr(user_id, **{'integral_profile':1})
        return resp

    def get_task_details(self, user_id):
        resp = {}
        task_status = TaskStatus()
        resp['newbie'] = self.get_statistics(user_id, StatisticItem)
        resp['daily'] = self.get_statistics(user_id, DailyStatisticItem)
        resp['awarded_tasks'] = [{'task_id':task_id} for task_id, awarded in 
                        task_status.award_status(user_id).iteritems() if awarded]
        return resp

    def can_draw_task(self, user_id):
        task_status = TaskStatus()
        awarded_tasks = [task_id for task_id, awarded in 
                        task_status.award_status(user_id).iteritems() if awarded]
        if len(awarded_tasks) == len(TaskManager.tasks()):
            return False

        stat = {}
        stat['StatisticItem'] = self.get_statistics(user_id, StatisticItem)
        stat['DailyStatisticItem'] = self.get_statistics(user_id, DailyStatisticItem)
        for task_id, task in TaskManager.tasks().iteritems():
            if task_id in awarded_tasks:
                continue
            statistics = stat[task.dependency_stat.__name__]
            stat_value = statistics[task.dependency.name.lower()]
            if task.can_award(stat_value):
                return True

        return False

    def update_award_status(self, user_id, task_id, awarded=True):
        if task_id not in TaskManager.tasks():
            raise TaskError.TASK_NOT_EXISTS(user_id=user_id, task_id=task_id)
        task_status = TaskStatus()
        task_status.draw_award(user_id, task_id)
        
    def draw_award(self, user_id, task_id):
        if task_id not in TaskManager.tasks():
            raise TaskError.TASK_NOT_EXISTS(user_id=user_id, task_id=task_id)

        task_status = TaskStatus()
        if task_status.has_awarded(user_id, task_id):
            raise TaskError.HAS_AWARDED(user_id=user_id, task_id=task_id)

        task = TaskManager.tasks()[task_id]
        statistics = self.get_statistics(user_id, task.dependency_stat)
        stat_value = statistics[task.dependency.name.lower()]

        if task.can_award(stat_value):
            award_currency = task.award_currency
            player_service = PlayerService(self.service_repositories, self.activity_repository)
            player_currency = player_service.increment_currency(user_id, award_currency, 'Task_Award')
            task_status.draw_award(user_id, task_id)

            task_award = settings.TIME_LINE.personal_messages.task_award
            task_award = task_award.format(task.name.decode('utf-8'), award_currency)
            timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
            timeline_service.send_personal_message(user_id, task_award)

            return player_currency._asdict()
        else:
            raise TaskError.NOT_REACH_LIMITATION(user_id=user_id, task_id=task_id)

    def get_task_config(self):
        response = {}
        tasks = TaskManager.tasks()
        for task_id, task in tasks.iteritems():
            response[task_id] = task.award_currency
        return response
