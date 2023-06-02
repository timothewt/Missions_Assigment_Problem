from models.mission import Mission


class Schedule:
	"""
	Represents the schedule of an employee (his assigned missions)
	"""
	
	missions: list[Mission]  # list of the employee's missions, we keep the list sorted by day and start_hour

	def __init__(self, missions: list[Mission] = None) -> None:
		if missions is None:
			missions = []
		self.missions = missions


	def reset_schedule(self) -> None:
		"""
		Resets the schedule
		"""
		self.missions = []


	def add_mission(self, mission: Mission) -> None:
		"""
		Adds a mission to the schedule
		:param mission: the mission to add
		"""
		self.missions.append(mission)
		self.missions.sort(key=lambda m: (m.day, m.start_time))


	def is_empty_for_day(self, day: int) -> bool:
		"""
		Checks if the employee has no mission for the given day
		:param day: the day to check
		:return: True if the employee has no mission for the given day, False otherwise
		"""
		for i in range(len(self.missions) - 1, -1, -1):
			if self.missions[i].day < day:
				return True
			if self.missions[i].day == day:
				return False
		return True


	def is_valid(self) -> bool:
		"""
		Checks if the schedule is valid, i.e. if no mission overlaps another mission
		:return: True if the schedule is valid, False otherwise
		"""
		# TODO : add travel time between missions (add distance matrix to the paramters)
		for i in range(len(self.missions) - 1):
			if self.missions[i].day == self.missions[i + 1].day:
				if self.missions[i].end_time > self.missions[i + 1].start_time:
					return False
		return True


	def __str__(self) -> str:
		return f"{self.missions}"


	def __repr__(self) -> str:
		return self.__str__()
