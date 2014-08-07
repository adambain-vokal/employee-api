from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import viewsets, routers

from employeeapi_app.models import Employee

admin.autodiscover()

class EmployeeViewSet(viewsets.ModelViewSet):
    model = Employee
    
router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'employeeapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^api/v1/', include(router.urls)),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
)
