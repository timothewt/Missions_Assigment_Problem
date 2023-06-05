from models.mission import Mission
from config import *


class Schedule:
	"""
	Represents the schedule of an employee (his assigned missions)
	"""
	
	missions: list[Mission]  			# list of the employee's missions, we keep the list sorted by day and start_hour
	distance_traveled: float  			# distance traveled by the employee to complete his missions
	weekly_work_time: float  			# hours worked during the week
	daily_work_time: dict[int, float]  	# hours worked during each day, the key is the day and the value the time worked
	daily_start_time: dict[int, float]  # start time of the employee's day, the key is the day and the value the time he leaves the center
	daily_end_time: dict[int, float]  	# end time of the employee's day, the key is the day and the value the time he goes back at the center

	def __init__(self) -> None:
		self.missions = []
		self.distance_traveled = 0
		self.weekly_work_time = 0
		self.daily_work_time = dict()
		self.daily_start_time = dict()
		self.daily_end_time = dict()


	def reset_schedule(self) -> None:
		"""
		Resets the schedule
		"""
		self.__init__()


	def can_fit_in_schedule(self, mission: Mission, distance_matrix: list[list[bool]], centers_nb: int, employee_center_id: int) -> bool:
		"""
		Checks if the mission can fit in the schedule
		:param mission: the mission to check
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the mission can fit in the schedule, False otherwise
		"""
		mission_duration = mission.end_time - mission.start_time
		missions_of_day = [m for m in self.missions if m.day == mission.day]
		added_travel_distance = 0
		travel_time = 0
		travel_time_bis = 0

		if len(missions_of_day) == 0:
			added_travel_distance = distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
			
			return mission_duration + (added_travel_distance / TRAVEL_SPEED) <= MAX_DAILY_WORK_TIME \
					and self.weekly_work_time + mission_duration + (added_travel_distance / TRAVEL_SPEED) <= MAX_WEEKLY_WORK_TIME \
					and mission.end_time + (distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] / TRAVEL_SPEED) - (mission.start_time - (distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1])) <= MAX_DAILY_TIME_RANGE

		elif mission.end_time < missions_of_day[0].start_time:
			# if the mission checked is before the first mission of the day
			added_travel_distance = distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][centers_nb + missions_of_day[0].id - 1] \
									- distance_matrix[employee_center_id - 1][centers_nb + missions_of_day[0].id - 1]
			travel_time = distance_matrix[centers_nb + mission.id - 1][centers_nb + missions_of_day[0].id - 1] / TRAVEL_SPEED
			
			return mission.end_time + travel_time <= missions_of_day[0].start_time \
					and mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.daily_work_time[mission.day] <= MAX_DAILY_WORK_TIME \
					and mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.weekly_work_time <= MAX_WEEKLY_WORK_TIME \
					and missions_of_day[-1].end_time + (distance_matrix[centers_nb + missions_of_day[-1].id - 1][employee_center_id - 1] / TRAVEL_SPEED) - (mission.start_time - (distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1])) <= MAX_DAILY_TIME_RANGE

		elif mission.start_time > missions_of_day[-1].end_time:
			# if the mission checked is after the last mission of the day
			added_travel_distance = distance_matrix[centers_nb + missions_of_day[-1].id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] \
									- distance_matrix[centers_nb + missions_of_day[-1].id - 1][employee_center_id - 1]
			travel_time = distance_matrix[centers_nb + missions_of_day[-1].id - 1][centers_nb + mission.id - 1] / TRAVEL_SPEED
			return missions_of_day[-1].end_time + travel_time <= mission.start_time \
					and mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.daily_work_time[mission.day] <= MAX_DAILY_WORK_TIME \
					and mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.weekly_work_time <= MAX_WEEKLY_WORK_TIME \
					and mission.end_time + (distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] / TRAVEL_SPEED) - (missions_of_day[0].start_time - (distance_matrix[employee_center_id - 1][centers_nb + missions_of_day[0].id - 1])) <= MAX_DAILY_TIME_RANGE

		else:
			# else, it may fit between two missions during the day
			prev_mission = missions_of_day[0]

			for i in range(len(missions_of_day) - 1):
				next_mission = missions_of_day[i + 1]

				if mission.start_time > prev_mission.end_time and mission.end_time < next_mission.start_time:
					# checks if employee has the time to travel from mission i to the checked mission, and from the checked mission to the mission i + 1
					added_travel_distance = distance_matrix[centers_nb + prev_mission.id - 1][centers_nb + mission.id - 1] \
											+ distance_matrix[centers_nb + mission.id - 1][centers_nb + next_mission.id - 1] \
											- distance_matrix[centers_nb + prev_mission.id - 1][centers_nb + next_mission.id - 1]

					travel_time = distance_matrix[centers_nb + prev_mission.id - 1][centers_nb + mission.id - 1] / TRAVEL_SPEED
					travel_time_bis = distance_matrix[centers_nb + mission.id - 1][centers_nb + next_mission.id - 1] / TRAVEL_SPEED
					
					return mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.daily_work_time[mission.day] <= MAX_DAILY_WORK_TIME \
							and prev_mission.end_time + travel_time <= mission.start_time \
							and mission.end_time + travel_time_bis <= next_mission.start_time \
							and mission_duration + (added_travel_distance / TRAVEL_SPEED) + self.weekly_work_time <= MAX_WEEKLY_WORK_TIME

				prev_mission = next_mission

		return False  # no time frame found where the mission can fit


	def add_mission(self, mission: Mission, distance_matrix: list[list[float]], centers_nb: int, employee_center_id: int) -> None:
		"""
		Adds a mission to the schedule while keeping it sorted
		We consider that the mission had been checked with can_fit_in_schedule() before
		When adding a mission, updates the total distance traveled by the employee and the time worked during the week and the day
		Replaces the travel time took into account when inserting previous missions
		:param mission: the mission to add
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:param employee_center_id: the id of the center where the employee is based
		"""
		day = mission.day
		missions_of_day = [m for m in self.missions if m.day == day]

		added_travel_distance = 0
		mission_insert_index = 0  # index where the mission will be inserted in the schedule

		if len(missions_of_day) == 0:
			added_travel_distance = distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1]
									# distance center->mission->center
			self.daily_start_time[day] = mission.start_time - (distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] / TRAVEL_SPEED)
			self.daily_end_time[day] = mission.end_time + (distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] / TRAVEL_SPEED)
			for i, m in enumerate(self.missions):
				if m.day > day:
					mission_insert_index = i
					break
			else:
				mission_insert_index = len(self.missions)


		elif mission.end_time < missions_of_day[0].start_time:
			# if the new mission is before the first mission of the day
			added_travel_distance = distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][centers_nb + missions_of_day[0].id - 1] \
									- distance_matrix[employee_center_id - 1][centers_nb + missions_of_day[0].id - 1]
									# distance center->mission->first_mission_of_day, minus center->first_mission_of_day
			self.daily_start_time = mission.start_time - (distance_matrix[employee_center_id - 1][centers_nb + mission.id - 1] / TRAVEL_SPEED)
			mission_insert_index = self.missions.index(missions_of_day[0])

		elif mission.start_time > missions_of_day[-1].end_time:
			# if the new mission is after the last mission of the day
			added_travel_distance = distance_matrix[centers_nb + missions_of_day[-1].id - 1][centers_nb + mission.id - 1] \
									+ distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] \
									- distance_matrix[centers_nb + missions_of_day[-1].id - 1][employee_center_id - 1]
									# distance last_mission_of_day->mission->center, minus last_mission_of_day->center
			self.daily_end_time = mission.end_time + (distance_matrix[centers_nb + mission.id - 1][employee_center_id - 1] / TRAVEL_SPEED)
			mission_insert_index = self.missions.index(missions_of_day[-1]) + 1

		else:
			# else, it fits between two missions during the day
			for i in range(len(missions_of_day) - 1):

				if mission.start_time > missions_of_day[i].end_time and mission.end_time < missions_of_day[i + 1].start_time:
					added_travel_distance = distance_matrix[centers_nb + missions_of_day[i].id - 1][centers_nb + mission.id - 1] \
											+ distance_matrix[centers_nb + mission.id - 1][centers_nb + missions_of_day[i + 1].id - 1] \
											- distance_matrix[centers_nb + missions_of_day[i].id - 1][centers_nb + missions_of_day[i + 1].id - 1]  
											# distance mission i->mission->mission i+1, minus distance mission i->mission i+1
					mission_insert_index = self.missions.index(missions_of_day[i + 1])
					break

		added_work_time = mission.end_time - mission.start_time + added_travel_distance / TRAVEL_SPEED  # time taken to travel
		if day not in self.daily_work_time:
			self.daily_work_time[day] = added_work_time

		else:
			self.daily_work_time[day] += added_work_time

		self.weekly_work_time += added_work_time
		self.distance_traveled += added_travel_distance
		self.missions.insert(mission_insert_index, mission)


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


	def get_travel_distance(self, distance_matrix: list[list[float]]):
		pass


	def __str__(self) -> str:
		return f"{self.missions}"


	def __repr__(self) -> str:
		return self.__str__()
