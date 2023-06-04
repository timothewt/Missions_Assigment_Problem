from src.models.schedule import Schedule


class Employee:
	"""
	Represents a SESSAD employee, that visits missions 
	"""

	id: int  			# id of the employee
	center_id: str  	# id of the center the employee works at
	skill: str  		# skill of the employee (LPC, LSF)
	speciality: str  	# speciality of the employee (Musique, Mecanique, ect.)
	schedule: Schedule  # schedule of the employee's missions


	def __init__(self, id: int, center_id: str, skill: str, speciality: str, schedule: Schedule = None) -> None:
		self.id = id
		self.center_id = center_id
		self.skill = skill
		self.speciality = speciality
		if schedule is None:
			schedule = Schedule()
		self.schedule = schedule
	

	def reset_schedule(self) -> None:
		"""
		Resets the schedule of the employee
		"""
		self.schedule.reset_schedule()


	def __str__(self) -> str:
		return f"{self.id}: {self.skill}, {self.speciality}"


	def __repr__(self) -> str:
		return self.__str__()
