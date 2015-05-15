# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from buzzrweb.utils import is_logged_user, required_login
from django.template import RequestContext
import datetime
import phonenumbers

# import simplejson as json
import urllib
from django.conf import settings
import requests
import json
import pprint

def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    context_dict = {'message': "Welcome to Dashboard"}
    # Render the response and send it back!
    # Required login
    if is_logged_user(request) == 1:

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        if start_date:
            date_st = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            date_st = datetime.date.today() + datetime.timedelta(-29)

        if end_date:
            date_ed = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            date_ed = datetime.date.today()

        #search_url = 'http://113.160.224.183:8281/rest/get_chart_info/'
        search_url = settings.API_SERVER_IP_ADDRESS + '/rest/get_chart_info/'

        raw = urllib.urlopen(search_url)
        js = raw.readlines()

        jsdata = json.loads(js[0])
        user_total = 0
        total_miles = 0
        total_msg_voice = 0
        total_msg_text = 0
        total_msg_other = 0
        total_new_user = 0
        overall_avg_va = 0.0
        total_days = (date_ed - date_st)
        overall_usage_com = 0

        for item in jsdata:
            date_cr = datetime.datetime.strptime(item['cur_date'], '%Y-%m-%d').date()
            if date_ed >= date_cr and date_st <= date_cr:
                user_total = int(item['total_user'])
                total_miles += float(item['total_miles'])
                total_msg_voice += int(item['total_msg_voice'])
                total_msg_text += int(item['total_msg_text'])
                total_msg_other += int(item['total_msg_other'])
                total_new_user += int(item['total_new_user'])
                overall_usage_com += int(item['total_communities'])

        overall_avg_va = round(float(float(total_new_user)/float(total_days.days+1)),2)

        context_dict = {"overall_total": user_total, "overall_avg_va": overall_avg_va, "overall_new": total_new_user,
                        "overall_usage_text": total_msg_text, "overall_usage_voice": total_msg_voice,
                        "overall_usage_other": total_msg_other, "overall_usage_com": overall_usage_com,
                        "overall_usage_miles": total_miles, "overall_usage_avg_speed": 0,
                        "serer_uptime": '00.00%', "total_aws": 0, "data": json.dumps(jsdata)}
        #return HttpResponseRedirect('/dashboard')
        return render_to_response('dashboard/index.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)



#@login_required
def profile(request, pk):
    context = RequestContext(request)
    context_dict = {}
    plural_mile = 'Mile'
    # Required login
    if is_logged_user(request) == 1:

        url = settings.API_SERVER_IP_ADDRESS + '/rest/admin/user/' + pk + '/'

        headers = {'content-type': 'application/json'}

        if request.method == 'POST':
            #print request
            post = request.POST
            if post:
                # Validate POST
                if len(post['phone'].strip()) <= 15 and len(post['phone'].strip()) >= 10:
                    data = {
                        'first_name': post['first_name'].strip(), 'last_name': post['last_name'].strip(),
                        'phone': post['phone'].strip(), 'email': post['email'].strip(),
                        'status': post['status'].strip(),
                    }
                    r = requests.post(url, data=json.dumps(data), headers=headers)
                    #            message = r.text
                    #            print message
                    #            print r.json()['detail']
                    context_dict['message'] = r.json()['detail']
                    if r.status_code == 200:
                        context_dict['message_type'] = 'alert-success'
                    else:
                        context_dict['message_type'] = 'alert-danger'

                else:
                    context_dict['message'] = 'Invalid Phone Number'
                    context_dict['message_type'] = 'alert-danger'
        try:
            profile = requests.get(url, headers={'content-type': 'application/json'}).json()
            try:
                if float(profile['stats']['miles']) > 1:
                    plural_mile = 'Miles'
                profile['stats']['miles'] = str(profile['stats']['miles']) + ' ' + plural_mile
            except:
                profile['stats']['miles'] = '0 ' + plural_mile
                pass

        except:
            profile = None

        context_dict['user'] = profile
        context_dict['url_community'] = '/dashboard/community/' + pk
        context_dict['pk']= pk
        return render_to_response('dashboard/profile.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

def deleteProfile(request, pk):
    context = RequestContext(request)
    context_dict = {}
    if is_logged_user(request) == 1:
        url = settings.API_SERVER_IP_ADDRESS + '/rest/admin/user/' + pk + '/'
        headers = {'content-type': 'application/json'}
        if request.method == 'POST':
            r = requests.delete(url, headers=headers)
            #print r.status_code
            #print r.text
            return HttpResponseRedirect('/dashboard/all-users')
        else:
            return HttpResponseRedirect('/dashboard/user/'+pk)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

def user_reset_pwd(request):
        context = RequestContext(request)
        context_dict = {}
        return render_to_response('dashboard/resetpassword.html', {}, context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    context_dict = {}

    #url = settings.API_SERVER_IP_ADDRESS + '/oauth2/access_token/'
    url = settings.API_SERVER_IP_ADDRESS + '/rest/access_token/'

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        data = {'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET,
                'grant_type': 'password', 'username': username, 'password': password}

        #r = requests.post(url, data=json.dumps(data), headers=headers)
        r = requests.post(url, data=data)
        #context_dict['message'] = r.json()['detail']
        #print r.text

        #print r.json()
        if r.status_code == 200:
            account = r.json()['account']
            #print account
            if account['is_staff'] == True:
                #request.session['authenticated'] = 1
                request.session['logged_in'] = 1
                request.session['access_token'] = r.json()['access_token']
                request.session['account'] = account
                return HttpResponseRedirect('/dashboard')
            else:
                context_dict['message'] = 'You don\'t have permission to access administrator'
                context_dict['msgtype'] = "danger"
                return render_to_response('dashboard/login.html', context_dict, context)

        else:
            #context_dict['message'] = r.json()['error']
            context_dict['message'] = r.json()['detail']
            context_dict['msgtype'] = "danger"
            return render_to_response('dashboard/login.html', context_dict, context)

    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('dashboard/login.html', {}, context)

#@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    #logout(request)
    context = RequestContext(request)
    if is_logged_user(request) == 1:
        request.session['logged_in'] = 0
        request.session['access_token'] = ''
        request.session['account'] = ''
        # Take the user back to the homepage.
        #return HttpResponseRedirect('/')
        context_dict = {'message': "Logout successful!", 'msgtype': "success"}
        return render_to_response('dashboard/login.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

class basic_profile():
    def __init__(self, user_id, username, phone, fullname, city, state, active, friends, total_time):
        if active:
            self.icon_status = '/static/admin/img/icon-yes.gif'
            self.icon_title = 'Yes'
        else:
            self.icon_status = '/static/admin/img/icon-no.gif'
            self.icon_title = 'No'

        self.username = username
        self.phone = phone
        self.fullname = fullname
        self.city = city
        self.state = state
        self.friends = friends
        self.time = total_time
        self.detail = '/dashboard/user/%s/' % user_id


def all_users(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    if is_logged_user(request) == 1:
        #search_url = 'http://113.160.224.183:8280/rest/users/'
        search_url = settings.API_SERVER_IP_ADDRESS + '/rest/users/'

        raw = urllib.urlopen(search_url)
        js = raw.readlines()
        js_object = json.loads(js[0])

        #filter it all
        users = []
        context_dict = {'users': users}
        for item in js_object:

            username = item['username']
            fullname = ("%s %s" % (item['first_name'], item['last_name']))
            user_id = item['user_id']
            active = item['is_active']
            friends = item['friends']
            total_time = item['total_time']
            city = item['city']
            state = item['state']
            parsed_number = phonenumbers.parse(item['phone'], 'US')
            phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

            user = basic_profile(user_id, username, phone, fullname, city, state, active, friends, total_time)
            users.append(user)

        return render_to_response('dashboard/users.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)


def stats(request):

    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    if is_logged_user(request) == 1:
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        if start_date:
            date_st = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            date_st = datetime.date.today() + datetime.timedelta(-29)

        if end_date:
            date_ed = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            date_ed = datetime.date.today()

        #search_url = 'http://113.160.224.183:8281/rest/get_chart_info/'
        search_url = settings.API_SERVER_IP_ADDRESS + '/rest/get_chart_info/'

        raw = urllib.urlopen(search_url)
        js = raw.readlines()
        jsdata = json.loads(js[0])

        # Calc
        user_total = 0
        total_miles = 0
        total_msg_voice = 0
        total_msg_text = 0
        total_msg_other = 0
        total_new_user = 0
        overall_avg_va = 0.0
        total_days = ((date_ed - date_st))
        overall_usage_com = 0

        sc_data=[]
        lc_data=[]
        for item in jsdata:
            date_cr = datetime.datetime.strptime(item['cur_date'], '%Y-%m-%d').date()
            if date_ed >= date_cr and date_st <= date_cr:
                user_total = int(item['total_user'])
                total_msg_voice += int(item['total_msg_voice'])
                total_msg_text += int(item['total_msg_text'])
                total_msg_other += int(item['total_msg_other'])
                total_new_user += int(item['total_new_user'])
                overall_usage_com += int(item['total_communities'])
            #for chart
            if start_date and end_date:
                if date_ed >= date_cr and date_st <= date_cr:
                    sc_data+=[{'cur_date': item['cur_date'],
                       "total_msg_voice": item['total_msg_voice'],
                       "total_msg_text": item['total_msg_text'],
                       "total_msg_other": item['total_msg_other']}]
                    lc_data+=[{'cur_date': item['cur_date'],
                               'total_active_user': item['total_active_user'],
                               'total_user': item['total_user'],}]
            else:
                sc_data=jsdata
                lc_data=jsdata

        overall_avg_va = round(float(float(total_new_user)/float(total_days.days+1)),2)

        context_dict = {"overall_total": user_total, "overall_avg_va": overall_avg_va, "overall_new": total_new_user,
                        "overall_usage_text": total_msg_text, "overall_usage_voice": total_msg_voice,
                        "overall_usage_other": total_msg_other, "overall_usage_com": overall_usage_com,
                        "overall_usage_avg_speed": 0, "data": json.dumps(jsdata),
                        "sc_data": json.dumps(sc_data),
                        "lc_data": json.dumps(lc_data)}


        # For User Heat Map
        try:
            url_heat_map = settings.API_SERVER_IP_ADDRESS + '/rest/admin/heat-map'
            url_get_miles = settings.API_SERVER_IP_ADDRESS + '/rest/admin/statistic-miles'

            if start_date and end_date:
                payload = {'start_date': start_date, 'end_date': end_date}
                heatMapData = requests.get(url_heat_map, headers={'content-type': 'application/json'}, params=payload).json()
                total_miles = requests.get(url_get_miles, headers={'content-type': 'application/json'}, params=payload).json()
            else:
                heatMapData = requests.get(url_heat_map, headers={'content-type': 'application/json'}).json()
                total_miles = requests.get(url_get_miles, headers={'content-type': 'application/json'}).json()
        except:
            heatMapData = None

        context_dict['heat_map_data'] = json.dumps(heatMapData)
        context_dict['overall_usage_miles'] = total_miles


        return render_to_response('dashboard/stats.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

def technical(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    if is_logged_user(request) == 1:

        context_dict = {}
        return render_to_response('dashboard/technical.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)


def community(request, pk):
    context = RequestContext(request)
    context_dict = {}
    if is_logged_user(request) == 1:
        url = settings.API_SERVER_IP_ADDRESS + '/rest/admin/community/' + pk + '/'
        try:
            community = requests.get(url, headers={'content-type': 'application/json'}).json()
        except:
            community = None

        context_dict['communities'] = community

        return render_to_response('dashboard/community.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

def maps(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    import requests
    if is_logged_user(request) == 1:
        url = settings.API_SERVER_IP_ADDRESS + '/rest/get_info_for_maps/'
        # headers = {'content-type': 'application/json', 'Authorization': 'Bearer fb8ad0a788a3790f3a77d074a4d7011a49911854'}
        r = requests.get(url).json()
        print json.dumps(r['users_with_loc'])
        context_dict = {'enabled_users': r['enabled_users'],
                        'enabled_coms': r['enabled_coms'],
                        'locations': json.dumps(r['users_with_loc'])}
        return render_to_response('dashboard/super_map.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)

def maps_cu(request, pk):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    context_dict = {}

    if is_logged_user(request) == 1:

        url = settings.API_SERVER_IP_ADDRESS + '/rest/get_current_user_location/'+pk+'/'
        r = requests.get(url.replace("favicon.ico/",'')).json()
        print r
        context_dict['locations']= json.dumps(r['detail'])
        context_dict['pk']= pk
        res=r['responsecode']
        print res
        if res==200:
            return render_to_response('dashboard/user_map.html', context_dict, context)
        else:
            return render_to_response('dashboard/user_map_not_found.html', context_dict, context)
    else:
        context_dict = {'message': "You are not authenticated user, please login!", 'msgtype': "danger"}
        return render_to_response('dashboard/login.html', context_dict, context)
