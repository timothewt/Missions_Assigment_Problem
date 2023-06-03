from models.employee import Employee
from models.mission import Mission
from utils import *


class Solution:
	"""
	Represents a solution to the assigment problem, and an individual for the genetic algorithm
	"""
	
	assignments: list[int]  # list of the assignments of the missions to the employees, assigments[i] is the id of the employee assigned to mission i


	def __init__(self, size: int) -> None:
		self.assignments = [0] * size


	def get_fitness_1(self) -> float:
		"""
		Computes the fitness corresponding to the number of missions assigned
		:return: the number of missions assigned
		"""
		count = len(self.assignments)
		for assigned_employee_id in self.assignments:
			if assigned_employee_id == 0:
				count -= 1
		return count


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:
		"""
		Computes the distance fitness, i.e. the total distance traveled
		:param distance_matrix: the distance matrix
		:return: the distance fitness
		"""


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
			if assigned_employee_id == 0:  # mission not assigned
				count -= 1
				continue
			if employees[assigned_employee_id - 1].speciality != get_missions_by_id(missions, mission_index + 1).speciality:  # the second part of the boolean expression is to get the mission corresponding to the mission index (which is the mission id - 1)
				count -= 1
		return count


	def mutate(self) -> None:
		pass


	def evaluate(self, distance_matrix: list[list[float]], employees: list[Employee], missions: list[Mission]) -> list[float|float|float]:
		"""
		Evaluates the solution, i.e. computes the fitnesses
		:param distance_matrix: the distance matrix
		:param employees: the employees
		:param missions: the missions
		:return: the list of the fitnesses
		"""
		return self.get_fitness_1(), self.get_fitness_2(distance_matrix), self.get_fitness_3(employees, missions)


	def is_valid(self, employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]], centers_nb: int) -> bool:
		"""
		Checks if the solution is valid, i.e. if no mission overlaps another mission for each employee
		:param employees: the employees
		:param missions: the missions
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the solution is valid, False otherwise
		"""
		is_valid = True
		
		for i, mission in enumerate(missions):
			employees[self.assignments[i] - 1].schedule.add_mission(get_missions_by_id(missions, i + 1))

		for i, employee in enumerate(employees):

			if not employee.schedule.is_valid(distance_matrix, centers_nb):
				is_valid = False
				break

		for employee in employees:
			employee.reset_schedule()
			
		return is_valid


	def __str__(self) -> str:
		return f"{self.assignments}"


	def __repr__(self) -> str:
		return self.__str__()
