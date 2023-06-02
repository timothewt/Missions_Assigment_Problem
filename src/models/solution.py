from models.employee import Employee
from models.mission import Mission


class Solution:
	assignments: list[int]
	

	def __init__(self, size: int):
		self.assignments = [0] * size


	def get_fitness_1(self) -> float:
		return 0


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:
		return 0


	def get_fitness_3(self) -> float:
		return 0


	def mutate(self) -> None:
		pass


	def is_valid(self, employees: list[Employee], missions: list[Mission]) -> bool:
		"""
		Checks if the solution is valid, i.e. if no mission overlaps another mission for each employee
		:param employees: the employees
		:param missions: the missions
		:return: True if the solution is valid, False otherwise
		"""
		is_valid = True
		for i, mission in enumerate(missions):
			employees[self.assignments[i] - 1].schedule.add_mission(mission)
		for i, employee in enumerate(employees):
			if not employee.schedule.is_valid():
				is_valid = False
				break
		for employee in employees:
			employee.reset_schedule()
		return is_valid


	def __str__(self):
		return f"{self.assignments}"


	def __repr__(self):
		return self.__str__()

