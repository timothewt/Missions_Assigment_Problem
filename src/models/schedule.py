from models.mission import Mission


class Schedule:
	missions: list[Mission]  # we keep the list sorted by day and start_hour

	def __init__(self, missions: list[Mission] = []):
		self.missions = missions


	def is_empty_for_day(self, day: int) -> bool:
		for i in range(len(self.missions) - 1, -1, -1):
			if mission.day < day:
				return True
			if mission.day == day:
				return False
		return True


	def __str__(self):
		return f"{self.missions}"


	def __repr__(self):
		return self.__str__()
