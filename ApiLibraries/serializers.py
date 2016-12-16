# -*- coding: utf-8 -*-
from rest_framework import serializers
from ApiLibraries.models import mt_zipcode, mt_ip2location_db11, mt_ip2location_db11_ipv6, mt_credit_card_iin, Item

class ZipcodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mt_zipcode
        fields = ('zipcode', 'zipcode_old', 'jiscode', 'pref_kana', 'city_kana', 'street_kana', 'pref', 'city', 'street', 'flag1', 'flag2', 'flag3', 'flag4', 'flag5', 'flag6')

class Ip2locationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mt_ip2location_db11
        fields = ('ip_from','ip_to','country_code','country_name','region_name','city_name','latitude','longitude','zip_code','time_zone')

#class Ip2locationIpv6Serializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = mt_ip2location_db11_ipv6
#        fields = ('ip_from','ip_to','country_code','country_name','region_name','city_name','latitude','longitude','zip_code','time_zone')

class CreditCardIinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mt_credit_card_iin
        fields = ('iin','card_brand','card_sub_brand','card_type','card_category','country_code','bank_name','bank_url','bank_phone','bank_city')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id','name','price')


STATUSES = (
    'New',
    'Ongoing',
    'Done',
)

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    owner = serializers.CharField(max_length=256)
    status = serializers.ChoiceField(choices=STATUSES, default='New')

    def create(self, validated_data):
        return Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance