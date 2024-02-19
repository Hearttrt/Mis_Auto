
from client import MisAuto
import time

list = []
username = ""
password = ""
appointUser = ""
appointPeople = ""
saleNameList = []

c = MisAuto(username,password,appointUser,appointPeople,saleNameList)
done_list = []
not_done_list = []
for item in list:
    resp = c.get_execute_info(item)
    # print(resp)
    result = resp.get('obj', {}).get('varList', [])
    if not result:
        not_done_list.append(item)
    else:
        done_list.append(item)
        print(item)
    time.sleep(1)
    # break
        
print(len(done_list), done_list)
print(len(not_done_list), not_done_list)



