from __future__ import annotations
from random import randint, random
import json
from models.employee import Employee
from models.mission import Mission
from utils import *
from config import *


class Solution:
	"""
	Represents a solution to the assigment problem, and an individual for the genetic algorithm
	"""
	
	assignments: dict[int, int]  # hash table to store employees assigned to mission, assigments[i] is the id of the employee assigned to mission of id i


	def __init__(self) -> None:
		self.assignments = dict()


	def get_fitness(self, employees: dict[int, Employee], missions: dict[int, Mission], distance_matrix: list[list[float]], centers_nb: int) -> float:
		"""
		Computes all the fitnesses of the employees in one integer
		Using powers of ten, we can still use cascade sorting. 
		The first fitness is the most important, the second is less important, etc.
		The assignments number, the first, is the dominant number, multiplied by 10^8
		Then, to sort the travel cost (second fitness) in the opposite order of the two others, we take 10^8 - the travel cost in thousands.
		Finally, the number of specialities is the third fitness, it is stored in the last 3 digits.

		Example : 75 missions assigned, 1205 travel cost, 30 corresponding specialities:
		75 * 10^8 + (10^8 - 1205 * 10^3) + 30 = 7,598,795,030

		:param employees: list of employees
		:param missions: dict of missions
		:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
		:param centers_nb: number of centers
		:return: the fitness of the solution
		"""

		# Fitness one: number of missions assigned
		nb_assignments = len(self.assignments)

		# Fitness two: travel cost for employees
		for mission_id, assigned_employee_id in self.assignments.items():
			employees[assigned_employee_id].schedule.add_mission(missions[mission_id], distance_matrix, centers_nb, employees[assigned_employee_id].center_id)

		total_distance = 0
		for _, employee in employees.items():
			total_distance += employee.schedule.distance_traveled
			employee.reset_schedule()

		travel_cost = int(COST_PER_KM * total_distance)


		# Fitness three: number of specialities
		count = len(self.assignments)
		for mission_id, assigned_employee_id in self.assignments.items():
			if employees[assigned_employee_id].speciality != missions[mission_id].speciality:
				count -= 1

		specialities_count = count

		return int(nb_assignments * 1e8 + (1e8 - travel_cost * 1e3) + specialities_count)


	def mutate(self, missions: dict[Mission], employees: dict[int, Employee], mutated_genes_per_chromosome_rate: float) -> None:
		"""
		Mutates the solution to add diversity
		Selects two genes randomly and swaps them
		If one of the genes is not assigned, it is assigned to a random employee
		"""
		for _ in range(randint(1, max(int(mutated_genes_per_chromosome_rate * len(self.assignments)), 1))):
			gene1 = randint(1, len(missions))
			skill = missions[gene1].skill

			if gene1 not in self.assignments:
				self.assignments[gene1] = randint(1, len(employees))

				while employees[self.assignments[gene1]].skill != skill:
					self.assignments[gene1] = randint(1, len(employees))

			else:
				gene2 = randint(1, len(missions))
				while missions[gene2].skill != skill:
					gene2 = randint(1, len(missions))

				if gene2 not in self.assignments:
					self.assignments[gene2] = self.assignments[gene1]

					if random() < .5:
						self.assignments.pop(gene1)

				else:
					self.assignments[gene1], self.assignments[gene2] = self.assignments[gene2], self.assignments[gene1]


	def evaluate(self, distance_matrix: list[list[float]], employees: dict[int, Employee], missions: dict[int, Mission], centers_nb: int, fitness_memo: dict[Solution, int] = None) -> list[float|float|float]:
		"""
		Evaluates the solution, i.e. computes the fitnesses
		:param distance_matrix: the distance matrix
		:param employees: the employees
		:param missions: the missions
		:return: the fitness of the solution
		"""
		if fitness_memo is None:
			return self.get_fitness(employees, missions, distance_matrix, centers_nb)

		if self not in fitness_memo:
			fitness_memo[self] = self.get_fitness(employees, missions, distance_matrix, centers_nb)
		
		return fitness_memo[self]


	def is_valid(self, employees: dict[int, Employee], missions: dict[int, Mission], distance_matrix: list[list[float]], centers_nb: int) -> bool:
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

			if mission.skill != employees[self.assignments[mission_id]].skill:
				is_valid = False
				break

			if employees[self.assignments[mission_id]].schedule.can_fit_in_schedule(mission, distance_matrix, centers_nb, employees[self.assignments[mission_id]].center_id):
				employees[self.assignments[mission_id]].schedule.add_mission(mission, distance_matrix, centers_nb, employees[self.assignments[mission_id]].center_id)
			else:
				is_valid = False
				break

		for _, employee in employees.items():
			employee.reset_schedule()
			
		return is_valid
		

	def __eq__(self, other: Solution) -> bool:
		return self.assignments == other.assignments


	def __neq__(self, other: Solution) -> bool:
		return not self.__eq__(other)


	def __str__(self) -> str:
		return f"{self.assignments}"


	def __repr__(self) -> str:
		return self.__str__()


	def __hash__(self) -> int:
		return hash(json.dumps(self.assignments, sort_keys=True))
