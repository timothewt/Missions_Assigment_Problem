class Center:
	"""
	Represents a center
	"""

	id: int  	# id of the center 
	name: str  	# name of the center


	def __init__(self, id: int, name: str) -> None:
		self.id = id
		self.name = name
		

	def __str__(self) -> str:
		return f"{self.id}: {self.name}"


	def __repr__(self) -> str:
		return self.__str__()
