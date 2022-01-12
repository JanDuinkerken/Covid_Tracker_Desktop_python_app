class Page:
	def __init__(self):
		self.num = 1

	def next(self) -> None:
		self.num += 1

	def prev(self) -> None:
		self.num -= 1

	def res(self):
		self.num = 1
