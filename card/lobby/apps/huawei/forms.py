import hashlib

import logging
logger = logging.getLogger(__package__)

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.conf import settings

class HuaweiForm(forms.Form):
    uid = forms.CharField(max_length=50, required=True)
    access_token = forms.CharField(max_length=150, required=True)
    user_type = forms.CharField(max_length=50, required=True)
    device_name = forms.CharField(max_length=100, required=True)
    device_id = forms.CharField(max_length=32, required=True)
    device_model = forms.CharField(max_length=50, required=True)
    os_version = forms.CharField(max_length=50, required=True)
    os_platform = forms.CharField(max_length=50, required=True) 
    app_version = forms.CharField(max_length=20, required=True)
    channel = forms.CharField(max_length=50, required=False)
    package_type = forms.CharField(max_length=50, required=False)
    vender = forms.CharField(max_length=50, required=False)
    networking = forms.CharField(max_length=50, required=False)
    resolution = forms.CharField(max_length=50, required=False)
    memory_size = forms.CharField(max_length=50, required=False)
    imei_number = forms.CharField(max_length=50, required=False)
    sign = forms.CharField(max_length=50, required=False)

    error_messages = {
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'wrong_login_info': _("Your Information for Login is Wrong or incomplete "),
        }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.login_ip = kwargs.pop('login_ip', None)
        self.data = kwargs.get('data', None)
        self.user_cache = None
        self.service_repositories = kwargs.pop('service_repositories', None)
        self.activity_repository = kwargs.pop('activity_repository', None)
        self.counter_repository = kwargs.pop('counter_repository', None)
        self.need_creation = kwargs.pop('need_creation', False)
        super(HuaweiForm, self).__init__(*args, **kwargs)
    def _form_validate(self):
        if self.cleaned_data['app_version'] == '0.9':
            return
        data = u'{0}{1}{2}{3}{4}{5}{6}{7}{8}'.format(self.cleaned_data['access_token'],
                    self.cleaned_data['user_type'], self.cleaned_data['device_id'],
                    self.cleaned_data['device_model'], self.cleaned_data['os_version'],
                    self.cleaned_data['os_platform'], self.cleaned_data['app_version'],
                    self.cleaned_data['channel'], self.cleaned_data['vender'],)
        digest = hashlib.md5(data.encode("utf-8"))
        if digest.hexdigest() !=  self.cleaned_data['sign']:
            raise forms.ValidationError(self.error_messages['wrong_login_info'])

    def clean(self):
        logger.debug('authenticate args:%s', self.cleaned_data)
        if not self.is_valid():
            raise forms.ValidationError(self.error_messages['wrong_login_info'])
        if settings.HOLYTREE.need_validate_form:
            self._form_validate()
        cleaned_data = dict(self.cleaned_data.iteritems())
        cleaned_data['service_repositories'] = self.service_repositories
        cleaned_data['activity_repository'] = self.activity_repository
        cleaned_data['login_ip'] = self.login_ip
        cleaned_data['counter_repository'] = self.counter_repository
        cleaned_data['need_creation'] = self.need_creation
        self.user_cache = authenticate(**cleaned_data)
        if self.user_cache is None or not self.user_cache.is_active:
            raise PermissionDenied()

        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache