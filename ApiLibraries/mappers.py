from bpmappers import Mapper, RawField

"""
テスト用マップ
"""
class ItemMapper(Mapper):
    item_id = RawField('id')
    item_name = RawField('name')
    item_price = RawField('price')