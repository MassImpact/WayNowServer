from django.conf.urls import patterns, url

from dashboard import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^all-users/$', views.all_users, name='all_users'),
        #url(r'^about/$', views.about, name='about'),
        #url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
        url(r'^login/$', views.user_login, name='login'),
        url(r'^reset/$', views.user_reset_pwd, name='reset_pwd'),
        url(r'^stats/$', views.stats, name='stats'),
        url(r'^technical/$', views.technical, name='technical'),
        url(r'^maps/$', views.maps, name='maps'),
        url(r'^maps_cu/(?P<pk>(.)+)/$', views.maps_cu, name='maps_cu'),
        #url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^user/(?P<pk>(.)+)/$', views.profile, name='profile'),
        url(r'^delete-user/(?P<pk>(.)+)/$', views.deleteProfile, name='deleteProfile'),
        url(r'^community/(?P<pk>(.)+)/$', views.community, name='community'),
    )
