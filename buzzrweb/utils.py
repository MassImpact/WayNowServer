from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render_to_response
def is_logged_user(request):
    authenticated = request.session.get('logged_in', 0)
    return authenticated


def required_login(request, context):
    #context = RequestContext(request)
    context_dict = {'message': "You are not authenticated user, please login!"}
    if is_logged_user(request) == 0:
        return render_to_response('dashboard/login.html', context_dict, context)


