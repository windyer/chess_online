from django.conf.urls import patterns, url

from card.lobby.apps.holytree import views as holytree_view
from card.lobby.apps.holytree.forms import HolyTreeForm, GuestForm, RobotForm

guest_template_name = {
    'template_name': 'guest_login.html', 
    'authentication_form': GuestForm
}
robot_template_name = {
    'template_name': 'robot_login.html', 
    'authentication_form': RobotForm
}
holytree_login_template_name = {
    'template_name': 'holytree_login.html',
    'authentication_form': HolyTreeForm,
    'extra_context':{'need_creation': False},
}
holytree_register_template_name = {
    'template_name': 'holytree_login.html',
    'authentication_form': HolyTreeForm,
    'extra_context':{'need_creation': True},
}

urlpatterns = patterns('',
    url(r'^$', holytree_view.api_view, name='holytree'),
    url(r'^login/$', holytree_view.login, holytree_login_template_name, name='holytree-login'),
    url(r'^guest/$', holytree_view.login, guest_template_name, name='guest-login'),
    url(r'^robot/$', holytree_view.login, robot_template_name, name='robot-login'),
    url(r'^register/$', holytree_view.login, holytree_register_template_name, name='holytree-register'),
    url(r'^password/change/$', holytree_view.ChangePassword.as_view(), name='change-password'),
    url(r'^bind/$', holytree_view.BindAccount.as_view(), name='bind'),
    url(r'^password/forget/$', holytree_view.ForgetPassword.as_view(), name='forget-password'),
    url(r'^password/reset/$', holytree_view.ResetPassword.as_view(), name='reset-password'),
    url(r'^check_email/$', holytree_view.check_email, name='check-email'),
    url(r'^check_user/$', holytree_view.CheckUser.as_view(), name='check-user'),


)
