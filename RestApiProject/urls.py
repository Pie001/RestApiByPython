"""
Definition of urls for RestApiProject.
"""
from django.conf.urls import url, include
from rest_framework import routers
from ApiLibraries import views as zipcodeViews

router = routers.DefaultRouter()
# sample
#router.register(r'ZipcodeSample', zipcodeViews.ZipcodeSampleViewSet, base_name='ZipcodeSample')
# api
router.register(r'Zipcode', zipcodeViews.ZipcodeViewSet, base_name='Zipcode')
#router.register(r'ZipcodeOld', zipcodeViews.ZipcodeOldViewSet, base_name='ZipcodeOld')

router.register(r'IpCountry', zipcodeViews.Ip2locationViewSet, base_name='IpCountry')
#router.register(r'IpCountry_IPv6', zipcodeViews.Ip2locationIpv6ViewSet, base_name='IpCountry_IPv6')

router.register(r'ValidationCheck', zipcodeViews.ValidationCheckViewSet, base_name='ValidationCheck')

router.register(r'CreditCardIin', zipcodeViews.CreditCardIinViewSet, base_name='CreditCardIin')

# non model test
router.register(r'tasks', zipcodeViews.TaskViewSet, base_name='tasks')
router.register(r'IpCountry_IPv6', zipcodeViews.Ip2locationIpv6ViewSet, base_name='IpCountry_IPv6')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # sample 
    #url(r'^ZipcodeSample2/(?P<zipcode>[.\d]+)/$', zipcodeViews.ZipcodeSampleList.as_view()),
    # response test
    #url(r'^IpCountry_IPv6/', 'zipcodeViews.Ip2locationIpv6ViewSet'),
    url(r'^items/', 'ApiLibraries.views.item_list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]