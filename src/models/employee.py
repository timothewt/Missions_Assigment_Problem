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
	