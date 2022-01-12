from typing import Protocol

class Handler(Protocol):
	def on_home_s_clicked(self) -> None:pass
	def on_home_d_clicked(self) -> None:pass
	def on_usr_clicked(self) -> None:pass
	def on_db_clicked(self) -> None:pass
	def create_model_users(self,off) -> None:pass
	def updatetree(self,num) -> None:pass
	def se_next_clicked(self) -> None:pass
	def se_prev_clicked(self) -> None:pass
	def search(self) -> None:pass
	def create_user_page(self, id, s) -> None:pass
	def on_tree_selected(self, data1, data2) -> None:pass
	def set_labels(self, s) -> None:pass
	def update_qr(self, s) -> None:pass
	def update_access(self, id) -> None:pass
	def us_back_clicked(self) -> None:pass
	def getModel(self) -> None:pass
	def next_clicked(self) -> None:pass
	def prev_clicked(self) -> None:pass
	def find_person(self) -> None:pass
	def is_in_list(self,el,list) -> None:pass
	def process_entries(self,entries) -> None:pass
	def on_cancel_clicked(self) -> None:pass
