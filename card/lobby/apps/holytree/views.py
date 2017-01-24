#coding=utf-8

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import card.lobby.apps.holytree.models as holytree_models
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import get_current_site
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render,HttpResponse
import go.logging
import base64
from card.core.error.lobby import HolyTreeError
from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import request_limit, api_view_available
from card.lobby.apps.holytree import serializers
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.holytree.service import HolyTreeService
from backends import HolyTreeBackend
import card.lobby.apps.player.models as player_models
import ujson


@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'login': reverse('holytree-login', request=request, format=format),
        'check_user': reverse('check-user', request=request, format=format),
        'guest': reverse('guest-login', request=request, format=format),
        'robot': reverse('robot-login', request=request, format=format),
        'register': reverse('holytree-register', request=request, format=format),
        'password/change': reverse('change-password', request=request, format=format),
        'password/forget/': reverse('forget-password', request=request, format=format),
        'password/reset/': reverse('reset-password', request=request, format=format),
        'bind': reverse('bind', request=request, format=format),
        })

@go.logging.class_wrapper
class ChangePassword(generics.CreateAPIView):

    serializer_class   = serializers.ChangePassword
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.ChangePassword)
    def post(self, request, format=None):
        holytree_service  = HolyTreeService(self.request.service_repositories, 
                                request.activity_repository, request.counter_repository)
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            user_id = request.user.id
            holytree_service.change_password(user_id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class BindAccount(generics.CreateAPIView):

    serializer_class   = serializers.BindAccount
    permission_classes = (permissions.IsIdentifiedPlayer,)
    user_id =''
    user_email=''
    password=''
    @trace_view
    @request_limit(serializers.BindAccount)
    def post(self, request, format=None):
        holytree_service  = HolyTreeService(self.request.service_repositories, 
                                request.activity_repository, request.counter_repository)
        serializer = self.get_serializer(data=request.DATA)
        player_extra = player_models.PlayerExtra.get_player_extra(request.user.id)
        if int(player_extra.app_version.replace('.','')) >= 200:
            if serializer.is_valid():
                self.user_id  = request.user.id
                self.user_email= request.DATA['user_name']
                self.password=request.DATA['password']

                holytree_service.send_email(int(self.user_id),self.user_email,self.password,type="bind")
            return Response({})
        else:
            if serializer.is_valid():
                user_id = request.user.id
                holytree_service.bind_account(user_id, **serializer.data)
                return Response({})
            else:
                from rest_framework import status
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class ForgetPassword(generics.CreateAPIView):

    serializer_class = serializers.ForgetPasswordRequest

    @trace_view
    @request_limit(serializers.ForgetPasswordRequest)
    def post(self, request, format=None):
        holytree_service = HolyTreeService(self.request.service_repositories, 
                                request.activity_repository, request.counter_repository)
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            holytree_service.forget_password(**serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class ResetPassword(generics.RetrieveAPIView, generics.CreateAPIView):

    serializer_class = serializers.ResetPasswordRequest
    template_name = 'reset-password.html'

    @trace_view
    def get(self, request, format=None):
        return TemplateResponse(
            request, self.template_name,
            {'title': '重置帐号密码', 'request': request}
        )

    @trace_view
    def post(self, request, format=None):
        token = request.QUERY_PARAMS.get('token', '')
        holytree_service  = HolyTreeService(self.request.service_repositories, 
                                request.activity_repository, request.counter_repository)
        serializer = self.get_serializer(data=request.DATA)
        context = {'title': '重置帐号密码', 'request': request}

        if serializer.is_valid():
            try:
                holytree_service.reset_password(
                    token.strip(), serializer.data['new_password']
                )
            except HolyTreeError.INVALID_TOKEN:
                messages.error(request, u'网页已过期')
            else:
                messages.success(request, u'密码重设成功')
            return TemplateResponse(request, self.template_name, context)
        else:
            for error in serializer.errors.values():
                if u'两次输入的密码不相同' in error:
                    messages.error(request, u'两次输入的密码不相同')
                    break
                if u'密码设置过于简单' in error:
                    messages.error(request, u'密码设置过于简单')
                    break
            else:
                messages.error(request, u'输入错误')
            return TemplateResponse(request, self.template_name, context)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          authentication_form=AuthenticationForm,
          redirect_field_name=REDIRECT_FIELD_NAME,
          current_app=None, extra_context=None):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        login_ip = request.META.get('REMOTE_ADDR', None)
        kwargs = {'data': request.POST,
                  'service_repositories': request.service_repositories,
                  'login_ip':login_ip,
                  'activity_repository':request.activity_repository,
                  'counter_repository':request.counter_repository}
        if extra_context is not None:
            kwargs.update(extra_context)
            
        form = authentication_form(**kwargs)
            
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        if not settings.HOLYTREE.api_view_available:
            return HttpResponseServerError("resourse can not find", 
                                status=403, content_type="text/plain")
        form = authentication_form(request)

    request.session.set_test_cookie()
    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
'''
@go.logging.class_wrapper
class CheckEmail(generics.CreateAPIView):

    #serializer_class   = serializers.ChangePassword
    #permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        holytree_service = HolyTreeService(request.service_repositories,
                                       request.activity_repository, request.counter_repository)
        holytreebackend=HolyTreeBackend()
        token=request.GET['token']
        type= request.GET['type']
        t=0
        if type == 'bind' :
            t=holytree_service.check_email(token)
        if type == 'regist':
            t=holytreebackend.check_email(token,request.service_repositories,
                                request.activity_repository, request.counter_repository)
        if t==1 :
            return HttpResponse("恭喜您,邮箱验证成功! ")
        if t==0 :
            return HttpResponse("对不起,验证失败!请重新验证!")
'''

@sensitive_post_parameters()
@csrf_protect
@never_cache
def check_email(request):
    holytree_service = HolyTreeService(request.service_repositories,
                                       request.activity_repository, request.counter_repository)
    holytreebackend=HolyTreeBackend()
    parameter = request.GET['parameter']
    data = base64.b64decode(parameter)
    data = ujson.loads(data)
    token = data['token']
    type = data['type']
    t=0
    if type == 'bind' :
        t=holytree_service.check_email(token)
    if type == 'regist':
        t=holytreebackend.check_email(token,request.service_repositories,
                                request.activity_repository, request.counter_repository)
    if t==1 :
        return HttpResponse("恭喜您,邮箱验证成功! ")
    if t==0 :
        return HttpResponse("对不起,验证失败!请重新验证!")


@go.logging.class_wrapper
class CheckUser(generics.CreateAPIView):

    serializer_class   = serializers.ChangePassword
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        user_id=request.POST['user_id']
        holytree = holytree_models.HolyTree()
        try:
            user=holytree.get_holytree_by_user_id(int(user_id))
            user_name=user.user_name
            bind=True
        except Exception as ex:
            bind=False
        return Response({'bind': bind})
