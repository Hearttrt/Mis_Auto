
class JsonProcessor:
    #TODO: 
    def __init__(self, jsonData):
        self.jsonData = jsonData
        self.obj = self.jsonData.get('obj', {})
        self.page = self.obj.get('page', {})
        self.boom = self.obj.get('boom', {}) # 没有boom返回{}
        self.accessories = self.obj.get('accessories', {})
        self.land = self.obj.get('land', {})
        # 好像下面这个就没有必要了。。
        # if self.boom is None or self.accessories is None or self.land is None:
        #     raise ValueError('Invalid obj')

    def get_values(self, keyWord, data):
        if not isinstance(data, dict):
            return None

        if keyWord in data:
            return data[keyWord]

        for value in data.values():
            result = self.get_values(value, keyWord)
            if result is not None:
                return result

        return None
        
    def extract_details_list(self, detailsList, modelList):
        floorHight = self.get_values('floorHight', self.jsonData)
        projectNumber = self.get_values('projectNumber', self.jsonData)
        srcProductTypeId = self.get_values('srcProductTypeId', self.jsonData)

        for details in detailsList:
            details.update({
                "projectNumber": projectNumber,
                "srcProductTypeId": srcProductTypeId
            })
            for key in list(details.keys()):
                if key == 'materialId':
                    details['srcMaterialId'] = details[key]
                if key not in modelList:
                    del details[key]

        return detailsList
    
    def concat_Json(self, sourceKeys, targetKeys, response):
        """
            组合成post需要的表单json
        """
        result = {}
        
        for key in sourceKeys:
            field = targetKeys.get(key)
            if isinstance(field, str):
                result[key] = self.get_values(field, response)
            elif isinstance(field, list):
                result[key] = [self.concat_Json(field, response)]
            elif isinstance(field, tuple):
                field1, field2, field3 = field
                response = self.get_values(field3, response)
                result[key] = \
                    self.get_values(field1, response) + ' - ' + self.get_values(field2, response)
            else:
                result[key] = self.get_values(key, response)

        return result