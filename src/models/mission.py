class Mission:
	id: int
	day: int
	start_time: float  # in minutes
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


	def __str__(self):
		return f"{self.id}: Day {self.day} at {round(self.start_time / 60, 2)}h-{round(self.end_time / 60, 2)}h, {self.skill}, {self.speciality}"


	def __repr__(self):
		return self.__str__()
