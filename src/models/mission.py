class Mission:
	id: int
	day: int
	start_time: float  # in hours
	end_time: float
	skill: str
	speciality: str

	def __init__(self, id: int, day: int, start_time: float, end_time: float, skill: str, speciality: str):
		self.id = id
		self.day = day
		self.start_time = start_time
		self.end_time = end_time
		self.skill = skill
		self.speciality = speciality
