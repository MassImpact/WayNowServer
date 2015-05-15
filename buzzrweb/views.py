from django.views.generic import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.conf import settings
from django.contrib import messages
import requests
import json


class HomeView(TemplateView):
    template_name = 'admin/index.html'
    
class MapsView(TemplateView):
    template_name = 'admin/super_map.html'

class profile():
    def __init__(self, user_id, username, phone, fullname, city, state, active, friends, total_time):
        if active:
            self.icon_status = '/static/admin/img/icon-yes.gif'
        else:
            self.icon_status = '/static/admin/img/icon-no.gif'

        self.username = username
        self.phone = phone
        self.fullname = fullname
        self.city = city
        self.state = state
        self.friends = friends
        self.time = total_time
        self.detail = '/user/%s/' % user_id

from buzzrweb.forms import SetPasswordForm


class ResetPasswordRequestView(TemplateView):
    template_name = "registration/password_reset.html"

    def post(self, request):
        context = RequestContext(request)
        return render_to_response('registration/password_reset.html', {}, context)


class PasswordResetConfirmView(TemplateView):
    template_name = "registration/password_reset_confirm.html"
    success_url = '/account/login'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
            """
            View that checks the hash in a password reset link and presents a
            form for entering a new password.
            """
            context = RequestContext(request)
            context_message = None

            form = self.form_class(request.POST)
            assert uidb64 is not None and token is not None  # checked by URLconf


            if form.is_valid():
                #form.save(commit=True)
                new_password=form.cleaned_data['new_password2']
                url = settings.API_SERVER_IP_ADDRESS + '/account/reset_password_confirm/'+str(uidb64)+'-'+str(token)+'/'
                headers = {'content-type': 'application/json'}

                data = {
                    'new_password': new_password
                }
                #r = requests.post(url, data=data)
                r = requests.post(url, data=json.dumps(data), headers=headers)
                #print r.text
                #print "status code"
                #print r.status_code

                context_message = r.json()['detail']
                if r.status_code == 200:
                    message_type = 'alert-success'
                else:
                    message_type = 'alert-danger'
                #print r.json()

                #user.set_password(new_password)
                #user.save()
                #messages.success(request, 'Password has been reset.')

                return render_to_response('registration/password_reset_confirm.html',
                            {'form': form, 'context_message': context_message,'message_type': message_type}, context)
            else:
                #print form.errors
                context_message = 'Password reset has not been unsuccessful.'
                return render_to_response('registration/password_reset_confirm.html',
                                          {'form': form}, context)
