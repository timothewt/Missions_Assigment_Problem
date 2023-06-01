class Employee:
	id: int
	center_id: str
	skill: str
	speciality: str


	def __init__(self, id: int, center_id: str, skill: str, speciality: str):
		self.id = id
		self.center_id = center_id
		self.skill = skill
		self.speciality = speciality
	

	def __str__(self):
		return f"{self.id}: {self.skill}, {self.speciality}"


	def __repr__(self):
		return self.__str__()
