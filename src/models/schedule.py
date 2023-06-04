from models.mission import Mission
from config import *


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


	def can_fit_in_schedule(self, mission: Mission, distance_matrix: list[list[bool]], centers_nb: int) -> bool:
		"""
		Checks if the mission can fit in the schedule
		:param mission: the mission to check
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the mission can fit in the schedule, False otherwise
		"""
		for i in range(len(self.missions) - 1, -1, -1):

			if self.missions[i].day < mission.day:
				break

			if self.missions[i].day == mission.day:
				# considering the travel time between missions

				if self.missions[i].start_time < mission.start_time:
					# if the mission i starts before the mission we are checking
					distance_from_mission = distance_matrix[centers_nb + self.missions[i].id - 1][centers_nb + mission.id - 1]

					if self.missions[i].end_time + distance_from_mission / TRAVEL_SPEED > mission.start_time:
						return False
				else:
					# if the mission i ends before the mission we are checking
					distance_from_mission = distance_matrix[centers_nb + mission.id - 1][centers_nb + self.missions[i].id - 1]
					
					if mission.end_time + distance_from_mission / TRAVEL_SPEED > self.missions[i].start_time:
						return False

		return True


	def add_mission(self, mission: Mission) -> None:
		"""
		Adds a mission to the schedule while keeping it sorted by day and start_hour
		We consider that the mission had been checked with can_fit_in_schedule() before
		:param mission: the mission to add
		"""
		if len(self.missions) == 0:
			self.missions.append(mission)
			return
		
		if self.missions[-1].day < mission.day or (self.missions[-1].day == mission.day and self.missions[-1].end_time <= mission.start_time):
			self.missions.append(mission)
			return

		for i in range(len(self.missions) - 2, -1, -1):
			if (self.missions[i + 1].day > mission.day and self.missions[i].day < mission.day) or (self.missions[i + 1].day == mission.day and self.missions[i + 1].start_time >= mission.end_time and self.missions[i].day < mission.day) or (self.missions[i + 1].day > mission.day and self.missions[i].day == mission.day and self.missions[i].end_time <= mission.start_time) or (self.missions[i + 1].day == mission.day and self.missions[i + 1].start_time >= mission.end_time and self.missions[i].day == mission.day and self.missions[i].end_time <= mission.start_time):
				self.missions.insert(i + 1, mission)
				return

		self.missions.insert(0, mission)
		return


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


	def is_valid(self, distance_matrix: list[list[float]], centers_nb: int) -> bool:
		"""
		Checks if the schedule is valid, i.e. if no mission overlaps another mission
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the schedule is valid, False otherwise
		"""
		for i in range(1, len(self.missions)):

			if self.missions[i - 1].day == self.missions[i].day:
				distance_from_last_mission = distance_matrix[centers_nb + self.missions[i - 1].id - 1][centers_nb + self.missions[i].id - 1]
				time_from_last_mission = distance_from_last_mission / TRAVEL_SPEED

				if self.missions[i - 1].end_time + time_from_last_mission > self.missions[i].start_time:
					return False
		
		return True


	def __str__(self) -> str:
		return f"{self.missions}"


	def __repr__(self) -> str:
		return self.__str__()
