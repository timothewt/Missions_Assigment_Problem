from models.employee import Employee
from models.mission import Mission


class Solution:
	assignments: list[int]
	

	def __init__(self, size: int):
		self.assignments = [0] * size


	def get_fitness_1(self) -> float:
		count = len(self.assignments)
		for assigned_employee_id in self.assignments:
			if assigned_employee_id == 0:
				count -= 1
		return count


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:


		return 0

	def compute_E(self, nb_employee: int, nb_mission : int) -> list[list[int]]:
		E = [[0] * nb_mission for _ in range(nb_employee)]  # Matrice vide pour stocker les assignations des intervenants
		for employee in range(1, nb_employee+1):
			for n in self.assignments:
				if n == employee:
					check_schedule
					insertion
		return E

	# def check_schedule(self, E: list[list[int]], M: ):
	# 	for

	def get_fitness_3(self, employees: list[Employee], missions: list[Mission]) -> float:
		"""
		Computes the specialities fitness, i.e. the number of corresponding speciality between missions and employees
		:param employees: the employees
		:param missions: the missions
		:return: the specialities fitness
		"""
		count = len(self.assignments)
		for mission_index, assigned_employee_id in enumerate(self.assignments):
			if assigned_employee_id == 0:
				count -= 1
				continue
			if employees[assigned_employee_id - 1].speciality != next((mission for mission in missions if mission.id == mission_index + 1), None).speciality:
				count -= 1
		return count


	def mutate(self) -> None:
		pass

	def evaluate(self) -> list[float]:
		return 0

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
