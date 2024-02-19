from client import MisAuto



username = ""
password = ""
appointUser = ""
appointPeople = ""
saleNameList = []

landid = ""

c = MisAuto(username,password,appointUser,appointPeople,saleNameList)
c.get_project_ship_detial(landid)




