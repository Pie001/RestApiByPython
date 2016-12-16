# -*- coding: utf-8 -*-
import django_filters
from rest_framework import filters
from ApiLibraries.models import mt_zipcode, mt_ip2location_db11, mt_ip2location_db11_ipv6

#class ZipcodeFilter(django_filters.FilterSet):
#    class Meta:
#        model = mt_zipcode
#        fields = ['name', 'price', 'manufacturer']

#class IpFilter(django_filters.FilterSet):
#    ip = django_filters.NumberFilter(name="ip", lookup_type='in')

#    class Meta:
#        model = mt_ip2location_db11
#        fields = ("ip")

class IpInFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        ip = request.QUERY_PARAMS.get('ip')
        if ip:
            #ip = ids.split(",")
            #return mt_ip2location_db11.objects.filter(ip_to__gte=ip)[:10]
            return queryset.filter(ip_to__gte=ip)[:10]
        return queryset
