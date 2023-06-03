from random import randint, random
from models.employee import Employee
from models.mission import Mission
from utils import *


class Solution:
	"""
	Represents a solution to the assigment problem, and an individual for the genetic algorithm
	"""
	
	assignments: dict[int, int]  # hash table to store employees assigned to mission, assigments[i] is the id of the employee assigned to mission of id i


	def __init__(self) -> None:
		self.assignments = dict()


	def get_fitness_1(self) -> float:
		"""
		Computes the fitness corresponding to the number of missions assigned
		:return: the number of missions assigned
		"""
		return len(self.assignments)


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:
		"""
		Computes the distance fitness, i.e. the total distance traveled
		:param distance_matrix: the distance matrix
		:return: the distance fitness
		"""


		return 0

	# def compute_E(self, nb_employee: int, nb_mission : int) -> list[list[int]]:
	# 	E = [[0] * nb_mission for _ in range(nb_employee)]  # Matrice vide pour stocker les assignations des intervenants
	# 	for employee in range(1, nb_employee+1):
	# 		for n in self.assignments:
	# 			if n == employee:
	# 				check_schedule
	# 				insertion
	# 	return E

	# def check_schedule(self, E: list[list[int]], M: ):
	# 	for

	def get_fitness_3(self, employees: list[Employee], missions: dict[int, Mission]) -> float:
		"""
		Computes the specialities fitness, i.e. the number of corresponding speciality between missions and employees
		:param employees: the employees
		:param missions: the missions
		:return: the specialities fitness
		"""
		count = len(self.assignments)
		for mission_id, assigned_employee_id in self.assignments.items():
			if employees[assigned_employee_id - 1].speciality != missions[mission_id].speciality:
				count -= 1
		return count


	def mutate(self, missions: dict[Mission], employees: list[Employee]) -> None:
		"""
		Mutates the solution to add diversity
		Selects two genes randomly and swaps them
		If one of the genes is not assigned, it is assigned to a random employee
		"""
		gene1 = randint(1, len(missions))
		skill = missions[gene1].skill

		if gene1 not in self.assignments:
			self.assignments[gene1] = randint(1, len(employees))

			while employees[self.assignments[gene1] - 1].skill != skill:
				self.assignments[gene1] = randint(1, len(employees))

		else:
			gene2 = randint(1, len(missions))

			while missions[gene2].skill != skill or gene2 not in self.assignments or self.assignments[gene1] == self.assignments[gene2]:
				gene2 = randint(1, len(missions))

			self.assignments[gene1], self.assignments[gene2] = self.assignments[gene2], self.assignments[gene1]


	def evaluate(self, distance_matrix: list[list[float]], employees: list[Employee], missions: dict[int, Mission]) -> list[float|float|float]:
		"""
		Evaluates the solution, i.e. computes the fitnesses
		:param distance_matrix: the distance matrix
		:param employees: the employees
		:param missions: the missions
		:return: the list of the fitnesses
		"""
		return self.get_fitness_1(), self.get_fitness_2(distance_matrix), self.get_fitness_3(employees, missions)


	def is_valid(self, employees: list[Employee], missions: dict[int, Mission], distance_matrix: list[list[float]], centers_nb: int) -> bool:
		"""
		Checks if the solution is valid, i.e. if no mission overlaps another mission for each employee
		:param employees: the employees
		:param missions: the missions
		:param distance_matrix: the distance matrix
		:param centers_nb: the number of centers used in the distance matrix indices
		:return: True if the solution is valid, False otherwise
		"""
		is_valid = True
		
		for mission_id, mission in missions.items():

			if mission_id not in self.assignments:
				continue

			if mission.skill != employees[self.assignments[mission_id] - 1].skill:
				is_valid = False
				break

			if employees[self.assignments[mission_id] - 1].schedule.can_fit_in_schedule(mission, distance_matrix, centers_nb):
				employees[self.assignments[mission_id] - 1].schedule.add_mission(mission)
			else:
				is_valid = False
				break

		for employee in employees:
			employee.reset_schedule()
			
		return is_valid


	def copy(self):
		copy = Solution()
		copy.assignments = self.assignments.copy()
		return copy


	def __str__(self) -> str:
		return f"{self.assignments}"


	def __repr__(self) -> str:
		return self.__str__()
