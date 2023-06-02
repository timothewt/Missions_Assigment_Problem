class Mission:
	"""
	Represents a mission that will be assigned to an employee.
	"""

	id: int  			# id of the mission
	day: int  			# day at which the mission takes place
	start_time: float  	# start time of the mission in minutes
	end_time: float  	# end time of the mission in minutes
	skill: str  		# skill required for the mission (LPC, LSF)
	speciality: str  	# speciality required for the mission (Musique, Mecanique, ect.)


	def __init__(self, id: int, day: int, start_time: float, end_time: float, skill: str, speciality: str) -> None:
		self.id = id
		self.day = day
		self.start_time = start_time
		self.end_time = end_time
		self.skill = skill
		self.speciality = speciality


	def __str__(self) -> str:
		return f"{self.id}: Day {self.day} at {round(self.start_time / 60, 2)}h-{round(self.end_time / 60, 2)}h, {self.skill}, {self.speciality}"


	def __repr__(self) -> str:
		return self.__str__()
