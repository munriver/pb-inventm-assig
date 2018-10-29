from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'inventm'
urlpatterns = [
    url(r'^$', auth_views.login, name='login'),
    url(r'^login/$', views.r_login, name='rlogin'),
    url(r'^list/$', views.r_enumerate, name='list'),
    url(r'^add/$', views.add_items, name='add'),
    url(r'^delete/$', views.delete_items, name='delete'),
    url(r'^unauthorized/$', views.r_unauthorized, name='unauthorized'),
    url(r'^approve/$', views.approve_changes, name='approve'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url('^', include('django.contrib.auth.urls')),
]
