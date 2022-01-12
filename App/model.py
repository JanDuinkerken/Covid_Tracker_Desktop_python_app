import requests
NUM = 25

class Model:
	def __init__(self):
		try:
			requests.get("http://localhost:8080/api/rest/users",headers={"x-hasura-admin-secret":"myadminsecretkey"},timeout=5)
		except (requests.ConnectionError,requests.ConnectTimeout) as exception:
			raise IOError("No se pudo acceder al servidor")

	def users(self,offset):
		r = requests.get("http://localhost:8080/api/rest/users?offset=" + str(offset) + "&limit=" + str(NUM),
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		r.raise_for_status()
		return r.json()

	def get_user_info(self,name, surname):
		name=name.capitalize()
		surname=surname.capitalize()
		r = requests.get("http://localhost:8080/api/rest/user?name=" + name + "&surname=" + surname, headers={"x-hasura-admin-secret":"myadminsecretkey"})
		r.raise_for_status()
		return r.json()

	def get_access_data(self,id):
		r = requests.get( "http://localhost:8080/api/rest/user_access_log/" + id,
				headers={"x-hasura-admin-secret":"myadminsecretkey"})
		r.raise_for_status()
		return r.json()


	def get_access_log(self,page):
		r= requests.get("http://localhost:8080/api/rest/access_log?offset=" +str((page.num - 1)*NUM) +"&limit=" + str(NUM),
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		return r.json()

	def get_find_person(self):
		r= requests.get("http://localhost:8080/api/rest/access_log?offset=0",
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		return r.json()

	def getEntriesFac(self,id):
		r= requests.get("http://localhost:8080/api/rest/facility_access_log/" + str(id) + "/?offset=0",
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		data=r.json()
		return data["access_log"]
