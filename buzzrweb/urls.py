from django.conf.urls import patterns, include, url
from buzzrweb import views
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.user_login', name='login'),
    url(r'^home/$', views.HomeView.as_view()),
    #url(r'^maps/$', views.MapsView.as_view()),
    url(r'^dashboard/', include('dashboard.urls')),
    #url(r'^reset_password', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(),name='reset_password_confirm'),

)
