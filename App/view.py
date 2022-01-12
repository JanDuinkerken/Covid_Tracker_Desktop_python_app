import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from datetime import datetime
from handler import Handler

class View:
	def __init__(self, handler:Handler):
		self.handler=handler
		w = Gtk.Window(title="admin")
		self.w = w
		w.connect("delete-event", Gtk.main_quit)

		w.set_default_size(width=1280,height=720)
		w.set_border_width(10)

		usr_button = Gtk.Button(label = "Search User", hexpand=True, vexpand=True)
		usr_button.connect("clicked", self.button_switch)
		self.usr_button = usr_button

		db_button = Gtk.Button(label="Database", hexpand=True, vexpand=True)
		db_button.connect("clicked", self.button_switch)
		self.db_button = db_button

		back_home_search = Gtk.Button(label = "Home")
		back_home_search.connect('clicked', self.button_switch)
		self.back_home_search = back_home_search

		back_home_db = Gtk.Button(label = "Go Back")
		back_home_db.connect('clicked', self.button_switch)
		self.back_home_db = back_home_db

		self.searchbar = Gtk.Entry()
		self.searchbar.set_text("Search")
		searchbar_accessible=self.searchbar.get_accessible()
		searchbar_accessible.set_name("Search")

		button1 = Gtk.Button(label="<")
		button1.connect("clicked", self.button_switch)
		button1.set_sensitive(False)
		self.button1 = button1

		button2 = Gtk.Button(label=">")
		button2.connect("clicked", self.button_switch)
		self.button2 = button2

		number = Gtk.Label(label = f"")
		self.number=number

		tree = Gtk.TreeView(hexpand=True, vexpand=True)
		tree.columns_autosize()
		tree.set_enable_search(True)
		select = tree.get_selection()
		select.connect('changed', self.on_tree_selected_v)
		self.select = select
		self.tree = tree

		us_name = Gtk.Label()
		self.us_name = us_name

		us_surname = Gtk.Label()
		self.us_surname = us_surname

		qr = Gtk.Image()
		self.qr = qr

		us_back = Gtk.Button(label = "Go Back")
		us_back.connect("clicked", self.button_switch)
		self.us_back = us_back

		in_us = Gtk.Entry(hexpand=True)
		self.in_us = in_us
		self.in_us.set_text("Inicio: YY-MM-DD")
		in_us_accessible=self.in_us.get_accessible()
		in_us_accessible.set_name("Inicio_us")

		fin_us = Gtk.Entry(hexpand=True)
		self.fin_us = fin_us
		self.fin_us.set_text("Fin: YY-MM-DD")
		fin_us_accessible=self.fin_us.get_accessible()
		fin_us_accessible.set_name("Fin_us")

		find_us=Gtk.Button.new_with_label("Find Contacts")
		self.find_us = find_us
		self.find_us.connect("clicked",self.button_switch)

		scrl = Gtk.ScrolledWindow(expand = True)
		scrl.set_size_request(475, 1)
		self.scrl=scrl

		label1=Gtk.Label(label="Nombre:")
		label1.set_justify(Gtk.Justification.LEFT)
		label1.set_max_width_chars(15)
		self.label1 = label1

		label2=Gtk.Label(label="Apellido:")
		label2.set_justify(Gtk.Justification.LEFT)
		self.label2 = label2

		label3=Gtk.Label(label="Fecha Inicio:")
		label3.set_justify(Gtk.Justification.LEFT)
		self.label3 = label3

		label4=Gtk.Label(label="Fecha Fin:")
		label4.set_justify(Gtk.Justification.LEFT)
		self.label4 = label4

		self.name = Gtk.Entry()
		self.name.set_text("Nombre")
		name_accessible=self.name.get_accessible()
		name_accessible.set_name("Nombre")

		self.sur = Gtk.Entry()
		self.sur.set_text("Apellido")
		sur_accessible=self.sur.get_accessible()
		sur_accessible.set_name("Apellido")

		self.start = Gtk.Entry()
		self.start.set_text("Inicio: YYYY-MM-DD")
		start_accessible=self.start.get_accessible()
		start_accessible.set_name("Inicio")

		self.end = Gtk.Entry()
		self.end.set_text("Fin: YYYY-MM-DD")
		end_accessible=self.end.get_accessible()
		end_accessible.set_name("Fin")

		self.find=Gtk.Button.new_with_label("Find")
		self.find.connect("clicked",self.button_switch)

		self.find2=Gtk.Button.new_with_label("Find ->")
		self.find2.connect("clicked",self.button_switch)

		db_prev = Gtk.Button.new_with_label("<<")
		db_prev.connect("clicked", self.button_switch)
		self.db_prev = db_prev

		db_next = Gtk.Button.new_with_label(">>")
		db_next.connect("clicked", self.button_switch)
		self.db_next = db_next

		db_page = Gtk.Label(label="Patata")
		db_page.set_justify(Gtk.Justification.LEFT)
		self.db_page=db_page

		spinner = Gtk.Spinner()
		self.spinner = spinner

		cancel = Gtk.Button.new_with_label("X")
		cancel.connect("clicked", self.button_switch)
		self.cancel = cancel

		grid = Gtk.Grid()
		self.grid=grid

		grid.attach(usr_button, 0,1,10,2)
		grid.attach(db_button, 0,3,10,2)
		grid.attach(back_home_db,0,1,1,2)
		grid.attach(label1,1,1,2,1)
		grid.attach(label2,3,1,2,1)
		grid.attach(label3,5,1,2,1)
		grid.attach(label4,7,1,2,1)
		grid.attach(self.find,9,2,1,1)
		grid.attach_next_to(self.name, label1, Gtk.PositionType.BOTTOM,2,1)
		grid.attach_next_to(self.sur, label2,Gtk.PositionType.BOTTOM,2,1)
		grid.attach_next_to(self.start,label3,Gtk.PositionType.BOTTOM,2,1)
		grid.attach_next_to(self.end, label4,Gtk.PositionType.BOTTOM,2,1)
		grid.attach(db_prev,2,9,2,1)
		grid.attach(db_next,6,9,2,1)
		grid.attach(db_page,4,9,2,1)

		grid.attach(back_home_search,0,1,1,1)
		grid.attach(self.searchbar,1,1,8,1)
		grid.attach(self.tree, 0, 2, 10, 1)
		grid.attach_next_to(self.find2,self.searchbar,Gtk.PositionType.RIGHT,1,1)
		grid.attach(number, 4, 3, 1, 1)
		grid.attach_next_to(button2, number, Gtk.PositionType.RIGHT, 1, 1)
		grid.attach_next_to(button1, number, Gtk.PositionType.LEFT, 1, 1)

		grid.attach(us_name,1,2,1,1)
		grid.attach(us_surname,1,3,1,1)
		grid.attach(qr,0,2,1,2)
		grid.attach(us_back,0,1,3,1)
		grid.attach(in_us, 0,6,1,1)
		grid.attach(fin_us, 1,6,1,1)
		grid.attach(find_us,2,6,1,1)
		grid.attach(scrl, 0,7,3,3)

		w.add(grid)
		w.show_all()

		self.in_us.hide()
		self.fin_us.hide()
		self.find_us.hide()
		self.tree.hide()
		self.us_name.hide()
		self.us_surname.hide()
		self.qr.hide()
		self.scrl.hide()
		self.us_back.hide()
		self.searchbar.hide()
		self.find2.hide()
		self.button1.hide()
		self.button2.hide()
		self.number.hide()
		self.label1.hide()
		self.label2.hide()
		self.label3.hide()
		self.label4.hide()
		self.name.hide()
		self.sur.hide()
		self.start.hide()
		self.end.hide()
		self.find.hide()
		self.db_prev.hide()
		self.db_next.hide()
		self.db_page.hide()
		self.back_home_search.hide()
		self.back_home_db.hide()
		self.spinner.hide()
		self.cancel.hide()

	def on_tree_selected_v(self, selection):
			model,treeiter=selection.get_selected()
			if treeiter == None: return

			data1 = model
			data2 = treeiter
			self.handler.on_tree_selected_thread(data1, data2)

	def main(self):
		Gtk.main()

	def set_next_sensitive(self):
		self.button2.set_sensitive(True)

	def set_prev_sensitive(self):
		self.button1.set_sensitive(True)

	def block_next(self):
		self.button2.set_sensitive(False)

	def block_prev(self):
		self.button1.set_sensitive(False)

	def getSearch(self):
		return self.searchbar.get_text().lower()

	def getData(self):
		n = self.us_name.get_text().split(" ")[1]
		s = self.us_surname.get_text().split(" ")[1]
		i = self.in_us.get_text()
		f = self.fin_us.get_text()

		return n, s, i, f

	def setData(self,n, s, i, f):
		self.name.set_text(n)
		self.sur.set_text(s)
		self.start.set_text(i)
		self.end.set_text(f)

	def process_model(self,list,which):
		store=self.getListStore(which)
		for i in range(len(list)):
			store.append(list[i])
		return store

	def generateTrees(self):
		model= self.handler.create_model_users(0, True)
		model = self.process_model(model,0)
		self.tree.set_model(model)
		self.add_column(self.tree, "Users", 0, 1)


		user_access = Gtk.TreeView()
		renderer = Gtk.CellRendererText()
		columns=["temperature","timestamp","type","name","address","id"]
		for el in columns:
			column1=Gtk.TreeViewColumn(el,renderer,text=columns.index(el))
			user_access.append_column(column1)

		user_access.columns_autosize()

		self.user_access = user_access
		model=self.handler.getModel(True)
		model=self.process_model(model,2)
		self.db=Gtk.TreeView(model=model, hexpand=True, vexpand=True)
		db_accessible=self.db.get_accessible()
		db_accessible.set_name("Lista")
		columns=["Nombre","Apellido","Fecha","Edificio","IN/OUT"]
		for el in columns:
			renderer=Gtk.CellRendererText()
			column=Gtk.TreeViewColumn(el,renderer,text=columns.index(el))
			self.db.append_column(column)

		self.scrl.add(self.user_access)
		self.grid.attach(self.db,0,3,10,6)
		self.db.hide()
		self.user_access.hide()




	def update_page_num(self,page,which):
		n = page.num
		text = f"{n}"
		if which==0:
			self.number.set_label(text)
		elif which==1:
			self.db_page.set_label(text)

	def get_search(self):
		n = self.us_name.get_text().split(" ")[1]
		s = self.us_surname.get_text().split(" ")[1]
		i = self.in_us.get_text()
		f = self.fin_us.get_text()
		return n, s, i, f

	def set_search(self, n, s, i, f):
		self.name.set_text(n)
		self.sur.set_text(s)
		self.start.set_text(i)
		self.end.set_text(f)


	def update_name(self, name):
		self.us_name.set_markup("<big>Name: " + name.capitalize() + "</big>")

	def update_surname(self, surname):
		self.us_surname.set_markup("<big>Surname: " + surname.capitalize() + "</big>")

	def change_page(self,model):
		model=self.process_model(model,0)
		self.tree.set_model(model)

	def update_qr_view(self):
		self.qr.set_from_file("qr.png")

	def show_home(self):
		self.usr_button.show()
		self.db_button.show()

	def hide_prin(self):
		self.usr_button.hide()
		self.db_button.hide()

	def hide_search_page(self):
		self.tree.hide()
		self.searchbar.hide()
		self.find2.hide()
		self.button1.hide()
		self.button2.hide()
		self.number.hide()
		self.back_home_search.hide()

	def show_user(self):
		self.us_name.show()
		self.us_surname.show()
		self.qr.show()
		self.user_access.show()
		self.scrl.show()
		self.us_back.show()
		self.in_us.show()
		self.fin_us.show()
		self.find_us.show()

	def clear_user(self):
		self.us_name.hide()
		self.us_surname.hide()
		self.qr.hide()
		self.user_access.hide()
		self.scrl.hide()
		self.us_back.hide()
		self.in_us.hide()
		self.fin_us.hide()
		self.find_us.hide()

	def show_search(self):
		self.tree.show()
		self.select.unselect_all()
		self.searchbar.show()
		self.find2.show()
		self.button1.show()
		self.button2.show()
		self.number.show()
		self.back_home_search.show()

	def show_db(self):
		self.back_home_db.show()
		self.label1.show()
		self.label2.show()
		self.label3.show()
		self.label4.show()
		self.name.show()
		self.sur.show()
		self.start.show()
		self.end.show()
		self.find.show()
		self.db.show()
		self.db_prev.show()
		self.db_next.show()
		self.db_page.show()

	def clear_db(self):
		self.label1.hide()
		self.label2.hide()
		self.label3.hide()
		self.label4.hide()
		self.name.hide()
		self.sur.hide()
		self.start.hide()
		self.end.hide()
		self.find.hide()
		self.db.hide()
		self.db_prev.hide()
		self.db_next.hide()
		self.back_home_db.hide()
		self.db_page.hide()

	def update_access_tree(self, l):
		store=self.process_model(l,1)
		self.user_access.set_model(store)

	def updateView(self,model):
		model=self.process_model(model,2)
		self.db.set_model(model)

	def createModel(self,data):
		l=[]
		for i in range(len(data)):
			timestamp= datetime.fromisoformat(data[i]["timestamp"])
			date = timestamp.strftime("%Y-%m-%d | %H:%M:%S")
			l.append([str(data[i]["user"]["name"]),str(data[i]["user"]["surname"]),date,str(data[i]["facility_id"]),data[i]["type"]])
		self.updateView(l)

	def getEntries(self):
		l=[]
		l.append(self.name.get_text())
		l.append(self.sur.get_text())
		l.append(self.start.get_text())
		l.append(self.end.get_text())
		return l

	def changeColumns(self,which):
		cols=self.db.get_columns()
		for el in cols:
			self.db.remove_column(el)
		if which==0:
			columns=["Nombre","Apellido","Fecha","Edificio","IN/OUT"]
		else:
			columns=["Nombre","Apellido","Vacuna?","Teléfono","Email"]
		for el in columns:
			renderer=Gtk.CellRendererText()
			column=Gtk.TreeViewColumn(el,renderer,text=columns.index(el))
			self.db.append_column(column)

	def show_infobar(self,output_text, close):
		self.infobar=Gtk.InfoBar(hexpand=True)
		if(close):
			self.infobar.connect("response",self.close_program)
		else:
			self.infobar.connect("response",self.close_info_bar)

		self.grid.attach(self.infobar,0,100,10,1)
		infobar_accessible = self.infobar.get_accessible()
		infobar_accessible.set_name("information")
		self.infobar.show()
		self.infobar.set_message_type(Gtk.MessageType.INFO)
		self.infobar.add_button("OK",0)
		message = Gtk.Label(label=output_text)
		content=self.infobar.get_content_area()
		content.add(message)
		message.show()

	def close_program(self, a, b):
		Gtk.main_quit()

	def close_info_bar(self, a, b):
		self.infobar.destroy()

	def getListStore(self, which) :
		if which==0:
			return Gtk.ListStore(str,str)
		if which==1:
			return Gtk.ListStore(str, str, str, str, str, int)
		if which==2:
			return Gtk.ListStore(str,str,str,str,str)

	def add_column(self,tree,title, id1, id2):
		column = Gtk.TreeViewColumn(title)

		name = Gtk.CellRendererText()
		surname = Gtk.CellRendererText()

		column.pack_start(name, True)
		column.pack_start(surname, True)

		column.add_attribute(name, "text", id1)
		column.add_attribute(surname, "text", id2)

		tree.append_column(column)

	def start_spinner(self, which):
		if which == "home":
			self.grid.attach_next_to(self.cancel, self.usr_button, Gtk.PositionType.RIGHT, 1, 9)
			self.grid.attach_next_to(self.spinner, self.cancel, Gtk.PositionType.RIGHT, 1, 9)
		elif which == "usr":
			self.grid.attach_next_to(self.cancel, self.find2, Gtk.PositionType.RIGHT, 2, 1)
			self.grid.attach_next_to(self.spinner, self.cancel, Gtk.PositionType.RIGHT, 2, 1)
		elif which == "db":
			self.grid.attach_next_to(self.cancel, self.find, Gtk.PositionType.RIGHT, 2, 1)
			self.grid.attach_next_to(self.spinner, self.cancel, Gtk.PositionType.RIGHT, 2, 1)

		self.cancel.show()
		self.spinner.start()
		self.spinner.show()

	def stop_spinner(self):
		self.cancel.hide()
		self.spinner.hide()
		self.spinner.stop()
		self.grid.remove(self.spinner)
		self.grid.remove(self.cancel)

	def button_switch(self, widget:Gtk.Widget):
		if widget==self.usr_button:
			self.handler.on_usr_clicked()
		if widget==self.db_button:
			self.handler.on_db_clicked()
		if widget==self.back_home_search:
			self.handler.on_home_s_clicked()
		if widget==self.back_home_db:
			self.handler.on_home_d_clicked()
		if widget==self.button1:
			self.handler.se_prev_clicked()
		if widget==self.button2:
			self.handler.se_next_thread()
		if widget==self.us_back:
			self.handler.us_back_clicked()
		if widget==self.find:
			self.handler.thread_find_person()
		if widget==self.find2:
			self.handler.search_thread()
		if widget==self.db_prev:
			self.handler.prev_clicked()
		if widget==self.db_next:
			self.handler.next_clicked()
		if widget == self.find_us:
			self.handler.find_us_clicked()
		if widget == self.cancel:
			self.handler.on_cancel_clicked()
