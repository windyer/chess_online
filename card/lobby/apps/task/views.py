from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby import permissions

from card.lobby.apps.task import serializers
from card.lobby.apps.task.service import TaskService
from card.lobby.apps.task.redis import TaskStatus

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'detail-tasks': reverse('detail-tasks', request=request, format=format),
        'task-config': reverse('task-config', request=request, format=format),
        })

@go.logging.class_wrapper
class Task(generics.RetrieveAPIView, generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.DrawAwardRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = TaskService(request.service_repositories, 
                                request.activity_repository, 
                                request.counter_repository)
        user_id = self.request.user.id

        response = service.get_task_details(user_id)
        response_serializer = serializers.TaskInfo(response)

        return Response(response_serializer.data)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = TaskService(request.service_repositories, 
                                    request.activity_repository, 
                                    request.counter_repository)
            user_id = request.user.id
            response = service.draw_award(user_id, **serializer.data)
            response_serializer = serializers.DrawAwardResponse(response)
            return Response(response_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class TaskConfig(generics.RetrieveAPIView, generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.DrawAwardRequest
    #permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = TaskService(request.service_repositories, 
                                request.activity_repository, 
                                request.counter_repository)
        user_id = self.request.user.id

        response = service.get_task_config()
        response_serializer = Response(response)

        return Response(response_serializer.data)