from const import DETAILSLIST_MODEL, SHIP_ADD_MODEL, FIELD_MAPPING

class JsonProcessor:
    # def __init__(self, json_object):
    #     self.json_object = json_object
        
    def get_json_value(self, json_object, key: str):
        if not isinstance(json_object, dict):
            return None

        if key in json_object:
            return json_object[key]

        for value in json_object.values():
            result = self.get_json_value(value, key)
            if result is not None:
                return result

        return None

    def update_json_data(self, json_object, update_json):
        json_object.update(update_json)
    
    def del_json_key_value(self, json_object, key):
        return json_object.pop(key)
    
    def get_value_old(self, json_object, key: str):
        if isinstance(json_object, dict):
            for k,v in json_object.items():
                if k == key:
                    return json_object.get(k)
                if isinstance(v, (dict,list)):
                    self.get_value(v, key)
                elif isinstance(json_object, list):
                    for item in json_object:
                        if isinstance(k, (dict,list)):
                            self.get_value(item, key)

# result = j.get_json_value(json_data.get('obj').get('accessories'), 'detailsList')

def concat_json(j, json_object, source_keys, target_keys=None, update_data=None):
    result = {}
    for key in source_keys:
        if target_keys is None:
            field = key
        else:
            field = target_keys.get(key)
        
        if isinstance(field, str):
            result[key] = j.get_json_value(json_object, field)
        elif isinstance(field, list):
            tmp = j.get_json_value(json_object, field)
            for item in tmp:
                j.update_json_data(item, update_data)
            
        elif isinstance(field, dict):
            keys = field.keys()
            result[key] = [concat_json(j, json_object, keys, field, update_data=update_data)]
        elif isinstance(field, tuple):
            field1, field2, field3 = field
            response = j.get_json_value(json_object, field3)
            result[key] = \
                j.get_json_value(response, field1) + ' - ' + j.get_json_value(response, field2)
        else:
            result[key] = j.get_json_value(json_object, key)

    return result
json_data = {}
j = JsonProcessor()
obj = json_data.get('obj')
update_data = {
    "projectNumber": "",
    "srcProductTypeId": ""
}
result = concat_json(j, obj, SHIP_ADD_MODEL, FIELD_MAPPING, update_data)
