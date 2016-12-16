# -*- coding: utf-8 -*-
from django.db import models
from model_utils.fields import StatusField

"""
郵便番号用テーブル
"""
class mt_zipcode(models.Model):
    id = models.IntegerField
    jiscode         = models.CharField(max_length=5)
    zipcode_old     = models.CharField(max_length=5)
    zipcode         = models.CharField(max_length=7)
    pref_kana       = models.CharField(max_length=20)
    city_kana       = models.CharField(max_length=100)
    street_kana     = models.CharField(max_length=200)
    pref            = models.CharField(max_length=20)
    city            = models.CharField(max_length=100)
    street          = models.CharField(max_length=200)
    flag1           = models.BooleanField(default=1)
    flag2           = models.BooleanField(default=1)
    flag3           = models.BooleanField(default=1)
    flag4           = models.BooleanField(default=1)
    flag5           = models.BooleanField(default=1)
    flag6           = models.BooleanField(default=1)

    def __unicode__(self):
        return self.name

    #モデルの Meta オプション
    class Meta:
        #モデルの使うデータベーステーブルの名前。ない場合はappname_modelname(ex) postcode_tasttb)
        db_table = 'mt_zipcode'

"""
IPv4用テーブル
"""
class mt_ip2location_db11(models.Model):
    id              = models.IntegerField
    ip_from         = models.IntegerField(db_index=True)
    ip_to           = models.IntegerField(db_index=True)
    country_code    = models.CharField(max_length=2)
    country_name    = models.CharField(max_length=64)
    region_name     = models.CharField(max_length=128)
    city_name       = models.CharField(max_length=128)
    latitude        = models.CharField(max_length=64)
    longitude       = models.CharField(max_length=64)
    zip_code        = models.CharField(max_length=30)
    time_zone       = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mt_ip2location_db11'
        #INDEX `idx_ip_from_to` (`ip_from`, `ip_to`)
        index_together = ["ip_from", "ip_to"]

"""
IPv6用テーブル
"""
class mt_ip2location_db11_ipv6(models.Model):
    id              = models.IntegerField
    ip_from         = models.IntegerField(db_index=True)
    ip_to           = models.IntegerField(db_index=True)
    country_code    = models.CharField(max_length=2)
    country_name    = models.CharField(max_length=64)
    region_name     = models.CharField(max_length=128)
    city_name       = models.CharField(max_length=128)
    latitude        = models.CharField(max_length=64)
    longitude       = models.CharField(max_length=64)
    zip_code        = models.CharField(max_length=30)
    time_zone       = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mt_ip2location_db11_ipv6'
        #INDEX `idx_ip_from_to` (`ip_from`, `ip_to`)
        index_together = ["ip_from", "ip_to"]


"""
クレジットカードの発行者識別番号(IIN)テーブル
"""
class mt_credit_card_iin(models.Model):
    id = models.IntegerField
    iin             = models.CharField(max_length=6)
    card_brand      = models.TextField(max_length=64)
    card_sub_brand  = models.TextField(max_length=64)
    card_type       = models.TextField(max_length=64)
    card_category   = models.TextField(max_length=64)
    country_code    = models.TextField(max_length=128)
    bank_name       = models.TextField(max_length=128)
    bank_url        = models.TextField(max_length=200)
    bank_phone      = models.TextField(max_length=128)
    bank_city       = models.TextField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mt_credit_card_iin'

"""
テスト用テーブル
"""
class Item(models.Model):
    id              = models.IntegerField
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'item'
