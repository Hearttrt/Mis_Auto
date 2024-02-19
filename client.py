# from main.const import URL_BASE, FIELD_MAPPING, HEADERS
from const import URL_BASE, FIELD_MAPPING, HEADERS, SHIP_ADD_MODEL
import logging
import math
import time
import json
import requests
import http.cookiejar as cj

defaultPath = "./data"
filePath = "../data/cookies.txt"


class MisAuto:
    def __init__(self, username, password, appointUser, appointPeople, saleNameList):
        self.username = username
        self.password = password
        self.appointUser = appointUser
        self.appointPeople = appointPeople
        self.saleNameList = saleNameList
        self.login()
        self.saleName = None
        self.landID = None

    def login(self):
        """
            登录
        """
        url = URL_BASE + '/login'
        playload = {
            "userName": self.username,
            "passWord": self.password
        }
        self.session = requests.session()
        self.session.cookies = cj.LWPCookieJar()
        response = self.post_something(url, playload)
        self.session.cookies.save(filename=filePath, ignore_discard=True, ignore_expires=True)
            
    def get_something(self, url, params=None):
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            logging.info(f'<GET {url} successed.>')
        except requests.exceptions.RequestException as exc:
            logging.error(f'<GET {url} failed>: {exc}')
            response = None
            
        return response
    
    def post_something(self, url, data):
        try:
            response = self.session.post(url, headers=HEADERS, json=data)
            response.raise_for_status()
            logging.info(f'<POST {url} successed.>')
        except requests.exceptions.RequestException as exc:
            logging.error(f'<POST {url} failed>: {exc}')
            response = None
            
        return response
    
    def get_business_list(self, params={"CHANNELID": ""}):
        """
            GET(params):
            params:
                - CHANNELID=
                - currentPage=1
                - totalResult= 6744 这个总数怎么来的
            response(模板见: ../data/business.json):
        """
        url = URL_BASE + '/business/projectList'
        return self.get_something(url, params).json() # response --> dict

    def get_business_list_more(self, search=None, params={"CHANNELID": ""}, showCount=10):
        """
            获取更多的列表
        """
        if search:
            params = {
                "search": search, 
                "CHANNELID": ""
                }
        totalList = []
        totalResult = self.get_business_list(params).get("obj",{}).get("page",{}).get("totalResult")

        count = math.ceil(totalResult / showCount) + 1 # math.ceil 向上取整
        for i in range(1, count): # range取不到num本身
            # params ={
            #     "search": search, 
            #     "CHANNELID": "",
            #     "currentPage": i,
            #     "showCount": showCount,
            #     "totalResult": totalResult
            # }
            params["currentPage"] = i
            params["showCount"] = showCount
            params["totalResult"] = totalResult
            data = self.get_business_list(params).get("obj",{}).get("list", [])
            totalList = totalList + data # 列表相加
            time.sleep(1)
            # print(f'正在获取第{i}页')
        currentTime = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{defaultPath}/misauto_all_{currentTime}_{totalResult}.json"
        with open(filename, 'w') as outfile:
            # ensure_ascii 
            json.dump(totalList, outfile, ensure_ascii=False)
            
    def get_business_list_update(self):
        pass
 
    def get_latest_projects(self, showCount=20):
        """
            GET(params): 
            获取项目落地的列表最近的20条, status == 0
        """
        # if self.session is None:
        #     self.login()
        url = URL_BASE + '/operation/dispatch'
        params = {
            "status" : 0,
            "currentPage": 1,
            "showCount": {showCount}
        } # TODO: check pls
        response = self.get_something(url, params)
        # get status=0 list
        project_list = response.json().get("obj", {}).get("list", []) 
        # extract to tuple_list(landId, projectNumber, status, saleName)
        extracted_list = [
            (d["landId"], d["projectNumber"], d["status"], d["saleName"]) 
            for d in project_list if d["saleName"] in self.saleNameList
            ]
        
        return extracted_list
       
    def get_project_info_detail(self, landID):
        """
            GET(params): 
            landid --> 获取落地明细信息:
             - msg --> str:success
             - obj --> {}
                - land --> {...} 落地明细信息都在这
                - projectTypeList --> [...] 没啥用
                - page --> {...} 这里面有个token不知道干啥的
                - write --> bool: true
             - status --> bool: true
             - error --> num: 0
                
        """ 
        url = URL_BASE + '/details/install'
        params = {
            "landId": landID,
            "type": 1
        } # TODO: check pls
        response = self.get_something(url, params).json()

        return response

    def get_project_ship_detial(self, landID):
        """
            GET(params): 
            获取landid详细信息shipSearchPro, 返回的信息(模板见: ../data/get_ship_magicball.json)包括:
             - error --> num: 0
             - msg --> str: success
             - obj --> {}
                - accessories --> {}
                    - accessoriesId --> str
                    - accessoriesName --> str
                    - createTime --> str: yy-mm-dd hh:mm:ss
                    - datailsList --> []
                        - {}
                            - accessoriesDetailsId --> str
                            - combinationName --> str
                            - description --> str
                            - materialId --> str
                            - materialName --> str
                            - number --> num
                            - remark --> str
                            - sortNumber --> num
                            - srcAccessoriesId --> str
                            - srcCombinationId --> str
                        - founder --> str
                        - srcMisBoomId --> str
                        - srcProductTypeId --> str
                        - status --> num
                - boom --> {...}
                - land --> {...}
                - materialList --> [{...}]
                - write --> bool: true
             - status --> bool: true
        """
        url = URL_BASE + '/operation/shipSearchPro'
        params = {
            "landId": landID
        }
        response = self.get_something(url, params).json()
        
        return response
    
    def get_execute_info(self, projectNumber=None):
        """
            GET: 查询信息
            projectNumber --> response(模板见: ../data/get_execute.json)
        """
        url = URL_BASE + '/operation/execute'
        params = {
            "PRONUMBER": projectNumber,

        }
        response = self.get_something(url, params)
        return response.json()
        
    def get_terminel_info(self):
        # TODO：終端信息
        pass

    def post_project_pm(self, landID):
        """
            POST(json/data): 
            landid --> 指派：
             - error --> num: 0
             - msg --> str: success 
             - obj --> null
             - status --> bool: true
        """
        url = URL_BASE + '/operation/manager'
        formData = {
            "landId":{landID},
            "appointUser":{self.appointUser},
            "appointPeople": {self.appointPeople},
            "status":1
        }
        response = self.post_something(url, formData)
        
        return response
  
    def post_ship(self, data):
        """
            POST(json/data): 出库单
        """
        url = URL_BASE + '/operation/ship'
        # data = self.concat_json() 
        response = self.post_something(url, data)
        
        return response





            