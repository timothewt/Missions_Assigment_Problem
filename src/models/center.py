class Center:
	id: int
	name: str


	def __init__(self, id: int, name: str):
		self.id = id
		self.name = name
		

	def __str__(self):
		return f"{self.id}: {self.name}"


	def __repr__(self):
		return self.__str__()
