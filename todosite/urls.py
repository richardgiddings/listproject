from . import views
from django.conf.urls import include, url
from .views import RegistrationView

app_name = 'todosite'
urlpatterns = [

    # Registration
    url(r'^register/$', RegistrationView.as_view(), name='register'),

    # User auth urls
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    url(r'^invalid/$', views.invalid_login, name='invalid'),

    # changing tasks
    url(r'^add_task/$', views.edit_task, name='add_task'),
    url(r'^(?P<task_id>\d+)/edit_task/$', views.edit_task, name='edit_task'),
    url(r'^delete/(?P<pk>\d+)/$', views.TaskDelete.as_view(), 
                                  name='delete_task'),
]