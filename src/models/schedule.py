from models.mission import Mission
from config import *


class Schedule:
	"""
	Represents the schedule of an employee (his assigned missions)
	"""
	
	missions: list[Mission]  # list of the employee's missions, we keep the list sorted by day and start_hour
	distance_traveled: float  # distance traveled by the employee to complete his missions

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


	def add_mission(self, mission: Mission, distance_matrix: list[list[float]], centers_nb: int, employee_center_id: int) -> None:
		"""
		Adds a mission to the schedule while keeping it sorted by day and start_hour
		We consider that the mission had been checked with can_fit_in_schedule() before
		:param mission: the mission to add
		"""
		if len(self.missions) == 0:
			self.missions.append(mission)
			self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
			return

		elif len(self.missions) == 1:
			if self.missions[0].day < mission.day:
				self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
				self.missions.append(mission)
				return
			elif self.mission[0].day > mission.day:
				self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
				self.missions.insert(0, mission)
				return
			elif self.missions[0].end_time <= mission.start_time:
				self.distance_traveled -= distance_matrix[centers_nb + self.missions[0].id - 1][employee_center_id - 1]
				self.distance_traveled += distance_matrix[centers_nb + self.missions[0].id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
				self.missions.append(mission)
				return
			else:
				self.distance_traveled -= distance_matrix[employee_center_id - 1][centers_nb + self.missions[0].id - 1]
				self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][centers_nb + self.missions[0].id - 1]
				self.missions.insert(0, mission)
				return

		if self.missions[-1].day < mission.day:
			self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
			self.missions.append(mission)
			return
		elif (self.missions[-1].day == mission.day and self.missions[-1].end_time <= mission.start_time):
			self.distance_traveled -= distance_matrix[centers_nb + self.missions[-1].id - 1][employee_center_id - 1]
			self.distance_traveled += distance_matrix[centers_nb + self.missions[-1].id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
			self.missions.append(mission)
			return

		for i in range(len(self.missions) - 2, -1, -1):
			if (self.missions[i + 1].day > mission.day and self.missions[i].day < mission.day):
				# no mission for mission.day
				self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
				self.missions.insert(i + 1, mission)
				return

			elif (self.missions[i + 1].day == mission.day and self.missions[i + 1].start_time >= mission.end_time and self.missions[i].day < mission.day):
				# the only mission for mission.day is after mission
				self.distance_traveled -= distance_matrix[employee_center_id - 1][centers_nb + self.missions[i + 1].id - 1]
				self.distance_traveled += distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][centers_nb + self.missions[i + 1].id - 1]
				self.missions.insert(i + 1, mission)
				return

			elif (self.missions[i + 1].day > mission.day and self.missions[i].day == mission.day and self.missions[i].end_time <= mission.start_time):
				# the only mission for mission.day is before mission
				self.distance_traveled -= distance_matrix[centers_nb + self.missions[i].id - 1][employee_center_id - 1]
				self.distance_traveled += distance_matrix[centers_nb + self.missions[i].id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
				self.missions.insert(i + 1, mission)
				return

			elif (self.missions[i + 1].day == mission.day and self.missions[i + 1].start_time >= mission.end_time and self.missions[i].day == mission.day and self.missions[i].end_time <= mission.start_time):
				# the mission fits between two missions
				self.distance_traveled -= distance_matrix[centers_nb + self.mission[i].id - 1][centers_nb + self.mission[i + 1].id - 1]
				self.distance_traveled += distance_matrix[centers_nb + self.mission[i].id - 1][centers_nb + mission.id - 1] + distance_matrix[centers_nb + mission.id - 1][centers_nb + self.mission[i + 1].id - 1]
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


	def is_valid(self, distance_matrix: list[list[float]], centers_nb: int, employee_center_id: int) -> bool:
		"""
		Checks if the schedule is valid, i.e. if no mission overlaps another mission
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the schedule is valid, False otherwise
		"""
		if len(self.missions) == 0:
			return True

		# TODO : add working time as attribute and computes it when adding mission

		weekly_work_time = self.missions[0].end_time - self.missions[0].start_time + (distance_matrix[employee_center_id - 1][centers_nb + self.missions[0].id - 1] / TRAVEL_SPEED)
		daily_work_time = weekly_work_time
		first_daily_mission_start_time = self.missions[0].start_time

		for i in range(1, len(self.missions)):

			if self.missions[i - 1].day == self.missions[i].day:
				# if they are the same day, computes the travel time between the two missions
				distance_from_last_mission = distance_matrix[centers_nb + self.missions[i - 1].id - 1][centers_nb + self.missions[i].id - 1]
				time_from_last_mission = distance_from_last_mission / TRAVEL_SPEED

				if self.missions[i - 1].end_time + time_from_last_mission > self.missions[i].start_time:
					return False
				else:
					total_mission_time = self.missions[i].end_time - self.missions[i].start_time + time_from_last_mission
					daily_work_time += total_mission_time
					weekly_work_time += total_mission_time

			else:
				# if not the same day, mission[i-1] is the last mission of a day mission[i-1].day, so the employee has to go back to his center
				last_mission_to_center_travel_time = (distance_matrix[centers_nb + self.missions[i - 1].id - 1][employee_center_id - 1] / TRAVEL_SPEED)
				daily_work_time += last_mission_to_center_travel_time
				weekly_work_time += last_mission_to_center_travel_time

				if daily_work_time > MAX_MINUTEES_PER_DAY or self.missions[i - 1].end_time - first_daily_mission_start_time > MAX_DAILY_MINUTES_RANGE:
					return False

				# then we compute the travel time from the center to the first mission of the day mission[i].day
				daily_work_time = self.missions[i].end_time - self.missions[i].start_time + (distance_matrix[employee_center_id - 1][centers_nb + self.missions[i].id - 1] / TRAVEL_SPEED)
				weekly_work_time += daily_work_time
				first_daily_mission_start_time = self.missions[i].start_time

		last_mission_to_center_travel_time = (distance_matrix[centers_nb + self.missions[-1].id - 1][employee_center_id - 1] / TRAVEL_SPEED)
		daily_work_time += last_mission_to_center_travel_time
		weekly_work_time += last_mission_to_center_travel_time
		
		if weekly_work_time > MAX_MINUTEES_PER_WEEK or daily_work_time > MAX_MINUTEES_PER_DAY or self.missions[-1].end_time - first_daily_mission_start_time > MAX_DAILY_MINUTES_RANGE:
			return False
		
		return True


	def get_travel_distance(self, distance_matrix: list[list[float]]):
		pass


	def __str__(self) -> str:
		return f"{self.missions}"


	def __repr__(self) -> str:
		return self.__str__()
