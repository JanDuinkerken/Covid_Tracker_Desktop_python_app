import pytz
import time
from datetime import datetime
import qrcode
from stoppablethread import StoppableThread
from model import Model
from page import Page
from view import View
import requests
import threading
import gi
from gi.repository import GLib

NUM = 25
utc=pytz.UTC

class Controller:
	def __init__(self):
		self.view = View(self)
		self.page = Page()
		page = self.page
		self.thread = StoppableThread()
		try:
			self.model = Model()
			self.view.generateTrees()
			self.view.update_page_num(page,0)
			self.view.update_page_num(page,1)
		except Exception as e:
			self.view.show_infobar(str(e),True)
			return None

	def start(self):
		self.view.main()

	def stop(self):
		return 0

	def on_cancel_clicked(self):
		self.thread.stop()
		self.view.stop_spinner()

	def on_home_s_clicked(self):
		self.page.res()
		self.view.set_next_sensitive()
		self.updatetree_home_s_clicked(0)
		self.view.update_page_num(self.page,0)

	def on_home_d_clicked(self):
		self.page.res()
		self.view.update_page_num(self.page,1)
		self.view.clear_db()
		self.view.show_home()

	def find_us_clicked(self):
		t=StoppableThread(target=self.find_us_clicked_next,daemon=True)
		t.start()
		t.join()


	def find_us_clicked_next(self):
		time.sleep(1)
		if self.thread.stopped():
			self.thread.rese()
		else:
			n, s, i, f = self.view.getData()
			self.view.clear_user()
			self.view.show_db()
			self.view.setData(n, s, i, f)
			entries=[n,s,i,f]
			GLib.idle_add(lambda: self.find_person(entries))

	def on_usr_clicked(self):
		self.view.hide_prin()
		self.view.show_search()

	def on_db_clicked(self):
		t=StoppableThread(target=self.on_db_clicked_next,daemon=True)
		t.start()
		t.join()

	def on_db_clicked_next(self):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			self.page.res()
			self.view.hide_prin()
			self.view.show_db()
			GLib.idle_add(lambda: self.getModel(False))

	def create_model_users(self,off, first):
		error = None
		try:
			data = self.model.users(off)
		except requests.exceptions.HTTPError as errh:
			error=errh
		except requests.exceptions.ConnectionError as errc:
			error=errc
		except requests.exceptions.Timeout as errt:
			error=errt
		except requests.exceptions.RequestException as err:
			error=err
		if(error==None):
			l=[]
			i=0
			if data["users"]:
				for i in range(NUM):
					l.append([data["users"][i]["name"], data["users"][i]["surname"]])
			if (first==True):
				self.view.stop_spinner()
				return l
			else:
				GLib.idle_add(lambda: self.process_create_model_users(error, l))
		else:
			l=[]
			GLib.idle_add(lambda: self.process_create_model_users(error,l))

	def process_create_model_users(self, error, l):
			if (error==None):
				self.after_cr_mod_us(l)
			else:
				self.view.stop_spinner()
				if isinstance(error,requests.exceptions.RequestException):
					self.view.show_infobar("Error en la petición.",True)
				elif isinstance(error,requests.exceptions.Timeout):
					self.view.show_infobar("Tiempo de espera finalizado.",True)
				elif isinstance(error,requests.exceptions.ConnectionError):
					self.view.show_infobar("Error de conexión con la base de datos.",True)
				elif isinstance(error,requests.exceptions.HTTPError):
					self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)

	def after_cr_mod_us(self,l):
			self.view.stop_spinner()
			self.view.change_page(l)

	def updatetree(self,num):
			self.view.start_spinner("usr")
			t=StoppableThread(target=self.updatetree_next, args=((num - 1)*25,),daemon=True)
			t.start()


	def updatetree_next(self, num):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			GLib.idle_add(lambda: self.create_model_users(num, False))

	def updatetree_home_s_clicked(self,num):
		self.view.start_spinner("usr")
		t=StoppableThread(target=self.updatetree_home_s_clicked_next, args=(num,),daemon=True)
		t.start()


	def updatetree_home_s_clicked_next(self, num):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			self.view.hide_search_page()
			self.view.show_home()
			GLib.idle_add(lambda: self.create_model_users(num, False))

	def se_next_thread(self):
			self.view.start_spinner("usr")
			t=StoppableThread(target=self.se_next_clicked, args=(),daemon=True)
			t.start()


	def se_next_clicked(self):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			error=None
			try:
				data = self.model.users(((self.page.num)*25))
			except requests.exceptions.HTTPError as errh:
					error=errh
			except requests.exceptions.ConnectionError as errc:
				error=errc
			except requests.exceptions.Timeout as errt:
				error=errt
			except requests.exceptions.RequestException as err:
				error=err

			GLib.idle_add(lambda: self.process_se_next_clicked(error, data))

	def process_se_next_clicked(self, error, data):
			if (error==None):
				self.after_se_next(data)
			else:
				self.view.stop_spinner()
				if isinstance(error,requests.exceptions.RequestException):
					self.view.show_infobar("Error en la petición.",True)
				elif isinstance(error,requests.exceptions.Timeout):
					self.view.show_infobar("Tiempo de espera finalizado.",True)
				elif isinstance(error,requests.exceptions.ConnectionError):
					self.view.show_infobar("Error de conexión con la base de datos.",True)
				elif isinstance(error,requests.exceptions.HTTPError):
					self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)

	def after_se_next(self, data):
			self.view.stop_spinner()
			if len(data["users"]) > 0:
					self.page.next()
					self.updatetree(self.page.num)
					self.view.update_page_num(self.page,0)
					self.view.set_prev_sensitive()
			else:
				self.view.block_next()

	def se_prev_clicked(self):
			if self.page.num > 1:
				self.page.prev()
				self.view.update_page_num(self.page,0)
				self.updatetree(self.page.num)
				self.view.set_next_sensitive()
			else:
				self.view.block_prev()

	def search_thread(self):
			self.view.start_spinner("usr")
			t=StoppableThread(target=self.search, args=(),daemon=True)
			t.start()


	def search(self):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			t = self.view.getSearch()
			s = t.split(" ")
			error = None
			if len(s)!=2:
				error = 400
			if(error == None):
				try:
					result = self.model.get_user_info(s[0], s[1])
				except requests.exceptions.HTTPError as errh:
					error=errh
				except requests.exceptions.ConnectionError as errc:
					error=errc
				except requests.exceptions.Timeout as errt:
					error=errt
				except requests.exceptions.RequestException as err:
					error=err

				if(error==None):
					if len(result["users"]) == 0:
						error = 401
					if(error==None):
						GLib.idle_add(lambda: self.process_search(error, result, s))
					else:
						GLib.idle_add(lambda: self.process_search(error, result, s))
				else:
					GLib.idle_add(lambda: self.process_search(error,result, s))
			else:
				GLib.idle_add(lambda: self.process_search(error, None, None))

	def process_search(self, error, result, s):
			if (error==None):
				self.after_search(result, s)
			else:
				self.view.stop_spinner()
				if isinstance(error,requests.exceptions.RequestException):
					self.view.show_infobar("Error en la petición.",True)
				elif isinstance(error,requests.exceptions.Timeout):
					self.view.show_infobar("Tiempo de espera finalizado.",True)
				elif isinstance(error,requests.exceptions.ConnectionError):
					self.view.show_infobar("Error de conexión con la base de datos.",True)
				elif isinstance(error,requests.exceptions.HTTPError):
					self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)
				elif (error==400):
					self.view.show_infobar("You must enter a name and a surname", False)
				elif (error==401):
					self.view.show_infobar("User not found", False)

	def after_search(self, result, s):
			self.view.hide_search_page()
			self.page.res()
			self.create_user_page(result["users"][0]["uuid"], s)

	def create_user_page(self, id, s):
			self.set_labels(s)
			self.update_qr(s)
			t=StoppableThread(target=self.update_access, args=(id,),daemon=True)
			t.start()
			t.join()
			self.view.show_user()

	def on_tree_selected_thread(self, data1, data2):
			self.view.start_spinner("usr")
			t=StoppableThread(target=self.on_tree_selected, args=(data1,data2,),daemon=True)
			t.start()


	def on_tree_selected(self, data1, data2):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			error = None
			try:
				res = self.model.get_user_info(data1[data2][0], data1[data2][1])
			except requests.exceptions.HTTPError as errh:
				error=errh
			except requests.exceptions.ConnectionError as errc:
				error=errc
			except requests.exceptions.Timeout as errt:
				error=errt
			except requests.exceptions.RequestException as err:
				error=err

			if (error == None):
				GLib.idle_add(lambda: self.process_tree_selected(error, res, data1, data2))

			else:
				GLib.idle_add(lambda: self.process_tree_selected(error))


	def process_tree_selected(self, error, res, data1, data2):
			if (error==None):
				self.after_tree_selected(res, data1, data2)
			else:
				self.view.stop_spinner()
				if isinstance(error,requests.exceptions.RequestException):
					self.view.show_infobar("Error en la petición.",True)
				elif isinstance(error,requests.exceptions.Timeout):
					self.view.show_infobar("Tiempo de espera finalizado.",True)
				elif isinstance(error,requests.exceptions.ConnectionError):
					self.view.show_infobar("Error de conexión con la base de datos.",True)
				elif isinstance(requests.exceptions.HTTPError):
					self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)

	def after_tree_selected(self, res, data1, data2):
			self.view.hide_search_page()
			self.create_user_page(res["users"][0]["uuid"], data1[data2])

	def set_labels(self, s):
			self.view.update_name(s[0])
			self.view.update_surname(s[1])

	def update_qr(self, s):
			img = qrcode.make('Name: ' + s[0].capitalize() + ' Surname: ' + s[1].capitalize())
			type(img)  # qrcode.image.pil.PilImage
			img.save("qr.png")
			self.view.update_qr_view()

	def update_access(self, id):
			error=None
			try:
				data = self.model.get_access_data(id)
			except requests.exceptions.HTTPError as errh:
				error=errh
			except requests.exceptions.ConnectionError as errc:
				error=errc
			except requests.exceptions.Timeout as errt:
				error=errt
			except requests.exceptions.RequestException as err:
				error=err

			if error == None:
				l=[]
				i=0
				for i in data["access_log"]:
					l.append([i["temperature"], i["timestamp"], i["type"], i["facility"]["name"], i["facility"]["address"], i["facility"]["id"]])

				GLib.idle_add(lambda: self.process_update_access(l, error))
			else:
				GLib.idle_add(lambda: self.process_update_access(None, error))

	def process_update_access(self, l, error):
		if error==None:
			self.after_update_access(l)
		else:
			self.view.stop_spinner()
			if isinstance(error,requests.exceptions.RequestException):
				self.view.show_infobar("Error en la petición.",True)
			elif isinstance(error,requests.exceptions.Timeout):
				self.view.show_infobar("Tiempo de espera finalizado.",True)
			elif isinstance(error,requests.exceptions.ConnectionError):
				self.view.show_infobar("Error de conexión con la base de datos.",True)
			elif isinstance(requests.exceptions.HTTPError):
				self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)

	def after_update_access(self,l):
		self.view.update_access_tree(l)
		self.view.stop_spinner()

	def us_back_clicked(self):
		self.view.clear_user()
		self.view.show_search()

	def getModel(self,first):
		error=None
		try:
			data = self.model.get_access_log(self.page)
		except requests.exceptions.HTTPError as errh:
			error=errh
		except requests.exceptions.ConnectionError as errc:
			error=errc
		except requests.exceptions.Timeout as errt:
			error=errt
		except requests.exceptions.RequestException as err:
			error=err

		if error==None:
			l=[]
			for i in range(NUM):
				timestamp= datetime.fromisoformat(data["access_log"][i]["timestamp"])
				date = timestamp.strftime("%Y-%m-%d | %H:%M:%S")
				l.append([str(data["access_log"][i]["user"]["name"]),str(data["access_log"][i]["user"]["surname"]),date,str(data["access_log"][i]["facility_id"]),data["access_log"][i]["type"]])
			if first:
				self.view.stop_spinner()
				return l
			else:
				GLib.idle_add(lambda: self.process_getModel(l,error))
		else:
			GLib.idle_add(lambda: self.process_getModel(None,error))

	def process_getModel(self, l, error):
		if error==None:
			self.after_get_model(l)
		else:
			self.view.stop_spinner()
			if isinstance(error,requests.exceptions.RequestException):
				self.view.show_infobar("Error en la petición.",True)
			elif isinstance(error,requests.exceptions.Timeout):
				self.view.show_infobar("Tiempo de espera finalizado.",True)
			elif isinstance(error,requests.exceptions.ConnectionError):
				self.view.show_infobar("Error de conexión con la base de datos.",True)
			elif isinstance(requests.exceptions.HTTPError):
				self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)

	def after_get_model(self, l):
		self.view.stop_spinner()
		self.view.update_page_num(self.page,1)
		self.view.changeColumns(0)
		self.view.updateView(l)


	def next_clicked(self):
		check= self.page.num +1
		if check*10>2992:
			return
		else:
			self.view.start_spinner("db")
			t = StoppableThread(target=self.next_clicked_2,args=(False,), daemon=True)
			t.start()


	def next_clicked_2(self, bool):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			self.page.next()
			GLib.idle_add(lambda: self.getModel(bool))

	def prev_clicked(self):
		if self.page.num - 1 <= 0:
			return
		else:
			self.view.start_spinner("db")
			t = StoppableThread(target=self.prev_clicked_2, args=(False,),daemon=True)
			t.start()


	def prev_clicked_2(self, bool):
		time.sleep(0.75)
		if self.thread.stopped():
			self.thread.rese()
		else:
			self.page.prev()
			GLib.idle_add(lambda: self.getModel(bool))

	def thread_find_person(self):
		self.view.start_spinner("db")
		t=StoppableThread(target=self.thread_find_person_next,daemon=True)
		t.start()


	def thread_find_person_next(self):
		time.sleep(0.25)
		if self.thread.stopped():
			self.thread.rese()
		else:
			entries=self.view.getEntries()
			GLib.idle_add(lambda: self.find_person(entries))

	def find_person(self,entries):
		error=None
		name=entries[0]
		surname=entries[1]
		try:
			usercheck=self.model.get_user_info(name,surname)
		except requests.exceptions.HTTPError as errh:
			error=errh
		except requests.exceptions.ConnectionError as errc:
			error=errc
		except requests.exceptions.Timeout as errt:
			error=errt
		except requests.exceptions.RequestException as err:
			error=err
		if error==None:
			if(len(usercheck["users"])==0):
				error=401
			if error==None:
				try:
					start=datetime.strptime(entries[2],"%Y-%m-%d")
					end=datetime.strptime(entries[3],"%Y-%m-%d")
				except ValueError as e:
					error=400
				if error==None:
					start=utc.localize(start)
					end=utc.localize(end)
					try:
						data=self.model.get_find_person()
					except requests.exceptions.HTTPError as errh:
						error=errh
					except requests.exceptions.ConnectionError as errc:
						error=errc
					except requests.exceptions.Timeout as errt:
						error=errt
					except requests.exceptions.RequestException as err:
						error=err

					if error==None:
						entries=[]

						datalog = data["access_log"]

						for i in range(len(datalog)):
							date= datetime.fromisoformat(datalog[i]["timestamp"])
							if name==datalog[i]["user"]["name"] and surname==datalog[i]["user"]["surname"] and start<date and end>date:
								entries.append(datalog[i])

						entries=self.process_entries(entries)

						final_list=[]
						possibles=[]

						for i in range(len(entries)):
							try:
								list=self.model.getEntriesFac(entries[i][0])
							except requests.exceptions.HTTPError as errh:
								error=errh
								self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)
							except requests.exceptions.ConnectionError as errc:
								error=errc
								self.view.show_infobar("Error de conexión con la base de datos.",True)
							except requests.exceptions.Timeout as errt:
								error=errt
								self.view.show_infobar("Tiempo de espera finalizado.",True)
							except requests.exceptions.RequestException as err:
								error=err
								self.view.show_infobar("Error en la petición.",True)
							if error==None:
								for j in range(len(list)):
									timestamp= datetime.fromisoformat(list[j]["timestamp"])
									if(list[j]["type"]=="OUT"):
										if timestamp>entries[i][1] and timestamp<entries[i][2]:
											if not self.is_in_list(list[j],final_list):
												final_list.append(list[j])
									#	else:
									#		if timestamp>entries[i][2]:
									#			possibles.append(list[j])
									else:
										if timestamp>entries[i][1] and timestamp<entries[i][2]:
											if not self.is_in_list(list[j],final_list):
												final_list.append(list[j])
								#This check was for a very specific situation and it's giving too much problems, so we decided to take it out
								#		else:
									#		if timestamp<entries[i][1] and self.is_in_list(list[j],possibles):
										#		print("Patata.")
											#	if not self.is_in_list(list[j],final_list):
												#	final_list.append(list[j])
		if error==None:
			l=[]
			for i in range(len(final_list)):
				datauser=final_list[i]["user"]
				l.append([str(datauser["name"]),str(datauser["surname"]),str(datauser["is_vaccinated"]),str(datauser["phone"]),datauser["email"]])
			GLib.idle_add(lambda: self.process_find_person(l,error))
		else:
			GLib.idle_add(lambda: self.process_find_person(None,error))

	def after_find_person(self, l):
		self.view.stop_spinner()
		self.view.changeColumns(1)
		self.view.updateView(l)

	def process_find_person(self,l,error):
		if error==None:
			self.after_find_person(l)
		else:
			self.view.stop_spinner()
			if error==401:
				self.view.show_infobar("User not found. Try again.", False)
			elif error==400:
				self.view.show_infobar("Wrong date format. Try again.", False)
			elif isinstance(error,requests.exceptions.RequestException):
				self.view.show_infobar("Error en la petición.",True)
			elif isinstance(error,requests.exceptions.Timeout):
				self.view.show_infobar("Tiempo de espera finalizado.",True)
			elif isinstance(error,requests.exceptions.ConnectionError):
				self.view.show_infobar("Error de conexión con la base de datos.",True)
			elif isinstance(requests.exceptions.HTTPError):
				self.view.show_infobar("Error HTTP ocurrido durante la petición.",True)


	def is_in_list(self,el,list):
		for x in range(len(list)):
			if el["user"]["uuid"]==list[x]["user"]["uuid"]:
				return True
		return False

	def process_entries(self,entries):
		processed=[]
		for i in range(len(entries)):
			#Asumimos que siempre va a venir ordenada debido a cómo tratamos las listas, de manera
			# que entries siempre traerá de primer elemento su última salida, de segundo du última
			#entrada...
			if i%2==0 and i+1<len(entries):
				timestamp= datetime.fromisoformat(entries[i]["timestamp"])
				timestamp2= datetime.fromisoformat(entries[i+1]["timestamp"])
				aux=[entries[i]["facility_id"],timestamp2,timestamp]
				processed.append(aux)

		return processed
