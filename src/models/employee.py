from models.schedule import Schedule


class Employee:
	id: int
	center_id: str
	skill: str
	speciality: str
	schedule: Schedule


	def __init__(self, id: int, center_id: str, skill: str, speciality: str, schedule: Schedule = Schedule()):
		self.id = id
		self.center_id = center_id
		self.skill = skill
		self.speciality = speciality
		self.schedule = schedule
	

	def reset_schedule(self):
		self.schedule = Schedule()


	def __str__(self):
		return f"{self.id}: {self.skill}, {self.speciality}"


	def __repr__(self):
		return self.__str__()
