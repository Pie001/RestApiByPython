# -*- coding: utf-8 -*-
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ApiLibraries.serializers import ZipcodeSerializer, Ip2locationSerializer, CreditCardIinSerializer, TaskSerializer
from ApiLibraries.models import mt_zipcode, mt_ip2location_db11, mt_ip2location_db11_ipv6, mt_credit_card_iin, Item
from rest_framework import filters
from rest_framework import generics
from RestApiProject.pagination import StandardResultsSetPagination
import ipaddress
from ApiLibraries.mappers import ItemMapper
from ApiLibraries import Task
import re, unicodedata
from django.db.models import Q
import IP2Location
import os

# ============================= サンプル =============================
#"""
#サンプル
#郵便番号検索API
#(querysetの検索にはREST Frameworkのfilterを利用)
#URL/Zipcode/?zipcode=zip_val
#ex) localhost:60492/Zipcode/?zipcode=0640941&city=&street=
#"""
#class ZipcodeSampleViewSet(viewsets.ModelViewSet):
#    queryset = mt_zipcode.objects.all()
#    serializer_class = ZipcodeSerializer
#    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
#    filter_fields = ('zipcode', 'city', 'street',)
#    search_fields = ('^zipcode', '^pref', '^city', '^street',)
#    ordering_fields = ('zipcode', 'pref', 'city', 'street')
#    pagination_class = StandardResultsSetPagination

#"""
#サンプル
#/ZipcodeSample2/3330851
#"""
#class ZipcodeSampleList(generics.ListAPIView):
#    serializer_class = ZipcodeSerializer

#    def get_queryset(self):
#        """
#        This view should return a list of all the purchases for
#        the user as determined by the username portion of the URL.
#        """
#        zipcode_param = self.kwargs['zipcode']
#        return mt_zipcode.objects.filter(zipcode=zipcode_param)

#"""
#サンプル
#QuerySet整形
#"""
#class ZipcodeOldViewSet(viewsets.ModelViewSet):
#    queryset = mt_zipcode.objects.all()
#    serializer_class = ZipcodeSerializer
#    filter_backends = (filters.OrderingFilter,)
#    ordering_fields = ('zipcode', 'pref', 'city', 'street')
#    pagination_class = StandardResultsSetPagination

#    def get_queryset(self):
#        type_val = self.request.query_params.get('type')
#        key_val = self.request.query_params.get('key')
#        if type_val is not None and key_val is not None:
#            if type_val == "zipcode":
#                #数字かチェック
#                if key_val.isdigit() is True:
#                    # fieldname__startswith = like '%keyword'
#                    self.queryset = mt_zipcode.objects.filter(zipcode__startswith=key_val)

#            if type_val == "zipcode_old":
#                #数字かチェック
#                if key_val.isdigit() is True:
#                    self.queryset = mt_zipcode.objects.filter(zipcode_old__startswith=key_val)

#            if type_val == "address":
#                self.queryset = mt_zipcode.objects.filter(Q(pref__startswith=key_val) | Q(city__startswith=key_val) | Q(street__startswith=key_val))

#            if type_val == "address_katakana":
#                self.queryset = mt_zipcode.objects.filter(Q(pref_kana__startswith=key_val) | Q(city_kana__startswith=key_val) | Q(street_kana__startswith=key_val))

#        return self.queryset
# =========================== QuerySet End ===========================

"""
郵便番号検索API

URL/Zipcode/?zipcode=zip_val
ex) localhost/Zipcode/?type=zipcode&key=606
"""
class ZipcodeViewSet(viewsets.ModelViewSet):
    queryset = mt_zipcode.objects.all()
    serializer_class = ZipcodeSerializer

    def list(self, request):
        page_size = 100
        type_val = request.query_params.get('type')
        key_val = request.query_params.get('key')
        orderby_val = request.query_params.get('orderby')
        size_val = request.query_params.get('size')
        search_success = False
        
        if size_val is not None and size_val.isdigit() is True and page_size >= int(size_val):
            page_size = int(size_val)

        if orderby_val is None:
            orderby_val = 'zipcode'

        if type_val is not None and key_val is not None:
            if type_val == "zipcode":
                #数字かチェック
                if key_val.isdigit() is True:
                    # fieldname__startswith = like '%keyword'
                    if 0 is not mt_zipcode.objects.filter(zipcode__startswith=key_val).count():
                        self.queryset = mt_zipcode.objects.filter(zipcode__startswith=key_val).order_by(orderby_val)[:page_size]
                        search_success = True
                    
            elif type_val == "zipcode_old":
                #数字かチェック
                if key_val.isdigit() is True and 0 is not mt_zipcode.objects.filter(zipcode_old__startswith=key_val).count():
                    self.queryset = mt_zipcode.objects.filter(zipcode_old__startswith=key_val).order_by(orderby_val)[:page_size]
                    search_success = True

            elif type_val == "address":
                if 0 is not mt_zipcode.objects.filter(Q(pref__startswith=key_val) | Q(city__startswith=key_val) | Q(street__startswith=key_val)).count():
                    self.queryset = mt_zipcode.objects.filter(Q(pref__startswith=key_val) | Q(city__startswith=key_val) | Q(street__startswith=key_val)).order_by(orderby_val)[:page_size]
                    search_success = True

            elif type_val == "address_kana":
                if 0 is not mt_zipcode.objects.filter(Q(pref_kana__startswith=key_val) | Q(city_kana__startswith=key_val) | Q(street_kana__startswith=key_val)).count():
                    self.queryset = mt_zipcode.objects.filter(Q(pref_kana__startswith=key_val) | Q(city_kana__startswith=key_val) | Q(street_kana__startswith=key_val)).order_by(orderby_val)[:page_size]
                    search_success = True

            if search_success is False:
                return Response({'message': '検索結果がありません。', 'type' : type_val, 'key' : key_val})

        else:
            return Response({'message': '検索条件を設定してください。'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ZipcodeSerializer(self.queryset, many=True)
        return Response(serializer.data)

"""
IPアドレスで検索(IPv4)

localhost/IpCountry/?ip=210.172.128.230
"""
class Ip2locationViewSet(viewsets.ModelViewSet):
    queryset = mt_ip2location_db11.objects.all()
    serializer_class = Ip2locationSerializer

    def list(self, request):
        param_ip = request.query_params.get('ip')
        if param_ip is not None:
            try:
                ipnet = ipaddress.ip_network(param_ip)
                if ipnet.version == 4:
                    param_ip_val = int(ipaddress.IPv4Address(param_ip))
                    #SELECT * FROM `restapi-local`.mt_ip2location_db11 where 3534520550 <= ip_to LIMIT 1;
                    ip_infos = mt_ip2location_db11.objects.filter(ip_to__gte=param_ip_val).order_by('ip_to')[:1]
                else:
                    ip_infos = mt_ip2location_db11.objects.all()[:1]
                    return Response(ip_infos, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'message': 'IP形式が正しくありません。', 'param': param_ip}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'IPアドレスの情報がありません。', 'param': param_ip}, status=status.HTTP_400_BAD_REQUEST)

        serializer = Ip2locationSerializer(ip_infos, many=True)
        return Response(serializer.data)

"""
バリデーションチェック
１、email：メールアドレス
２、tel：電話番号(電話番号/携帯番号のハイフンなし)
３、url：URL（ホームページアドレス）
４、zip:郵便番号(ハイフンあり/ハイフンなし)
５、ip：IP
６、ipv6：IPv6形式
"""
class ValidationCheckViewSet(viewsets.ViewSet):

    message_OK = 'The value is valid.'
    message_NG = 'The value is not valid.'
    message_required = 'The value is required.'
    pattern_email = r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'
    pattern_tel = r'^(\d{1,4})-(\d{1,4})-(\d{4})$'
    pattern_mobile_phone_no_hyphen = r'^(0[89]0\d{8})$'
    pattern_url = r'^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+$'
    pattern_zip = r'^(\d{3})-(\d{4})$'
    pattern_zip_no_hyphen = r'^(\d{7})$'

    def list(self, request):
        type_val = request.query_params.get('type')
        value_val = request.query_params.get('val')
        length_val = request.query_params.get('len')
        message = self.message_NG
        length = 0

        if type_val is not None and value_val is not None:
            length = len(value_val)
            # --------- 書式チェック -------------
            if type_val == 'email':
                if re.match(self.pattern_email, value_val):
                    message = self.message_OK

            elif type_val == 'tel':
                # 電話番号
                if re.match(self.pattern_tel, value_val):
                    message = self.message_OK
                # 携帯電話番号(ハイフンなし)
                if value_val.isdigit() is True and re.match(self.pattern_mobile_phone_no_hyphen, value_val):
                    message = self.message_OK

            elif type_val == 'url':
                if re.match(self.pattern_url, value_val):
                    message = self.message_OK

            elif type_val == 'zip':
                # 郵便番号
                if re.match(self.pattern_zip, value_val):
                    message = self.message_OK
                # 郵便番号(ハイフンなし)
                elif value_val.isdigit() is True and re.match(self.pattern_zip_no_hyphen, value_val):
                    message = self.message_OK

            elif type_val == 'ip':
                try:
                    ipnet = ipaddress.ip_network(value_val)
                    if ipnet.version == 4:
                        message = self.message_OK
                except ValueError:
                    pass

            elif type_val == 'ipv6':
                try:
                    ipnet = ipaddress.ip_network(value_val)
                    if ipnet.version == 6:
                        message = self.message_OK
                except ValueError:
                    pass

        else:
            message = self.message_required

        check_result = {'message': message, 'type': type_val, 'param' : value_val, 'length' : length}
        return Response(check_result)

"""
クレジットカードの発行者識別番号(IIN)
"""
class CreditCardIinViewSet(viewsets.ModelViewSet):
    queryset = mt_credit_card_iin.objects.all()
    serializer_class = CreditCardIinSerializer

    def list(self, request):
        param_iin = request.query_params.get('iin')
        if param_iin is not None and param_iin.isdigit() is True and 6 == len(param_iin) :
            if 0 is not mt_credit_card_iin.objects.filter(iin=param_iin).count():
                iin_infos = mt_credit_card_iin.objects.filter(iin=param_iin)[:1]
            elif 0 is not mt_credit_card_iin.objects.filter(iin__startswith=param_iin[:4]).count():
                iin_infos = mt_credit_card_iin.objects.filter(iin__startswith=param_iin[:4])[:1]
            else:
                return Response({'message': 'No results for {0}. Make sure you enter a valid BIN/IIN number.'.format(param_iin)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No results for {0}. Make sure you enter a valid BIN/IIN number.'.format(param_iin)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreditCardIinSerializer(iin_infos, many=True)
        serializer.data[0]['iin'] = param_iin
        return Response(serializer.data)


"""
IPアドレスで検索(IPv6)
No Model & use BIN file
localhost/IpCountry/?ip=fd07:a47c:3742:823e:3b02:76:982b:463
"""
class Ip2locationIpv6ViewSet(viewsets.ViewSet):

    def list(self, request):
        param_ip = self.request.query_params.get('ip')
        if param_ip is not None:
            try:
                ipnet = ipaddress.ip_network(param_ip)
                if ipnet.version == 6:

                    IP2LocObj = IP2Location.IP2Location();
                    IP2LocObj.open(os.path.join("data","IP2LOCATION-LITE-DB11.IPV6.BIN"));
                    ip_infos = IP2LocObj.get_all(param_ip);

                else:
                    return Response({'message': 'IP形式が正しくありません。', 'param': param_ip}, status=status.HTTP_400_BAD_REQUEST)

            # address が正しい IPv4, IPv6 アドレスを表現していない場合や、ネットワークの host bit がセットされていた場合
            except ValueError:
                return Response({'message': 'IP形式が正しくありません。', 'param': param_ip}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'IPアドレスの情報がありません。', 'param': param_ip})

        return Response({'zipcode': ip_infos.zipcode, 'city': ip_infos.city, 'ip': param_ip, 'longitude': ip_infos.longitude, 'country_long': ip_infos.country_long, 
                            'country_short': ip_infos.country_short, 'latitude': ip_infos.latitude, 'timezone': ip_infos.timezone, 'region': ip_infos.region})



# ============================= TEST =============================
"""
テスト
http://d.hatena.ne.jp/nullpobug/20131021/1382281371
ex) localhost:55840/items/
"""
@api_view(['GET'])
def item_list(request):
    items = Item.objects.all()
    serializer_class = Ip2locationSerializer
    return Response(ItemMapper(item).as_dict() for item in items)


"""
テスト
localhost/tasks/
ex) 
[
    {
        "id": 1,
        "name": "Demo",
        "owner": "xordoquy",
        "status": "Done"
    },
    {
        "id": 2,
        "name": "Model less demo",
        "owner": "xordoquy",
        "status": "Ongoing"
    },
    {
        "id": 3,
        "name": "Sleep more",
        "owner": "xordoquy",
        "status": "New"
    }
]
"""
class TaskViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer

    def list(self, request):
        # get requestで受け取ったパラメーター
        # ex) url/tasks/?name=testname&owner=testowner&status=teststatus
        name_val = request.query_params.get('name')
        owner_val = request.query_params.get('owner')
        status_val = request.query_params.get('status')
        param_pass = self.kwargs.get('uid')
        tasks = {
            1: Task(id=1, name=name_val, owner=owner_val, status=status_val),
            #1: Task(id=1, name='Demo', owner='xordoquy', status='Done'),
            2: Task(id=2, name='Model less demo', owner='xordoquy', status='Ongoing'),
            3: Task(id=3, name='Sleep more', owner='xordoquy', status='New'),
        }
        serializer = TaskSerializer(instance=tasks.values(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

