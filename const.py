
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

BRUSH_ID = [
    "8c9b3922aab9496f8ec243ab80a4e619", 
    "fa98de0576b7403181118f6725d04266", 
    "f89702a1cdaa4e16a9a68379eba44695"
    ]
PRODUCT_TYPE_LIST = [
    '14e63829657c4d2894555e1aebfa4bda', 
    'c2b443a667fe4535a5d9b9d1ada813a6', 
    '34616ea369c74b02845921e6d567f346',
    '8df6b569e8414b4790ba08c047f9f93d'  
    ]

# Playload for shipdetail 
SHIP_ADD_MODEL = [
    'contactPeople', 
    'deliveryList',
    'proNumber',
    'deliveryDate', # landid查询出来的时间对不上
    'developDate', # landid查询出来的时间对不上
    'fixAddress',
    'sceneDirector',
    'scenePhone', # scenePhone
    'contactPhone', 
    'remarks'
    ]

# DELIVERYLIST_MODEL = [
#     'boomId', 
#     'fnsName', 
#     'landNumber', 
#     'srcProductTypeId', 
#     'srcLandId' ,
#     'materialCache', 
#     'detailsList' 
#     ]

FIELD_MAPPING = {
    'srcLandId': 'landId',
    'fnsName': ('productTypeName', 'boomName'),
    'contactPhone': 'scenePhone',
    'contactPeople': 'sceneDirector',
    'materialCache': '',
    'proNumber': 'projectNumber',
    'deliveryList': [
        'boomId', 
        'fnsName', 
        'landNumber', 
        'srcProductTypeId', 
        'srcLandId' ,
        'materialCache', 
        'detailsList'
    ]
}

DETAILSLIST_MODEL = [
    'number', 
    'projectNumber', 
    'sortNumber', 
    'srcMaterialId', 
    'srcProductTypeId', 
    'materialName'
    ]

URL_BASE = ''