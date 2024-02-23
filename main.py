from client import MisAuto



username = ""
password = ""
appointUser = ""
appointPeople = ""
salepeople_list = []

landid = ""

c = MisAuto(username,password,appointUser,appointPeople)
c.get_latest_projects(appointPeople)




