from models.solution import Solution
from models.employee import Employee
from models.mission import Mission
from models.center import Center
from config import *
from copy import deepcopy
from random import choice


def get_nearest_neighbour_solution(employees: list[Employee], missions: list[Mission], centers: list[Center], distance_matrix: list[list[float]]) -> Solution:
	"""
	Generates a valid solution using the nearest neighbour algorithm
	:param employees: list of employees
	:param missions: list of missions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:return: A valid solution
	"""
	solution = Solution(len(missions))
	centers_nb = len(centers)

	for mission_index, mission in enumerate(missions):
		employees_distances_from_missions = [float('inf') for _ in range(len(employees))]
		
		for employee_index, employee in enumerate(employees):
		
			if employee.skill != mission.skill:
				continue
		
			if employee.schedule.is_empty_for_day(mission.day):
				employees_distances_from_missions[employee_index] = distance_matrix[employee.center_id - 1][centers_nb + mission_index]
			else:
				distance_from_last_mission = distance_matrix[centers_nb + employee.schedule.missions[-1].id - 1][centers_nb + mission_index]
				travel_time_from_last_mission = distance_from_last_mission * TRAVEL_SPEED

				if employee.schedule.missions[-1].end_time + travel_time_from_last_mission < mission.start_time:
					continue

				employees_distances_from_missions[employee_index] = distance_from_last_mission


		min_distance = float('inf')
		nearest_employees_indices = []

		for employee_index, employee_distance in enumerate(employees_distances_from_missions):
			if employee_distance < min_distance:
				min_distance = employee_distance
				nearest_employees_indices = [employee_index]
			elif employee_distance == min_distance:
				nearest_employees_indices.append(employee_index)

		solution.assignments[mission.id - 1] = employees[choice(nearest_employees_indices)].id

	return solution


def generate_initial_population(employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]], size: int) -> list[Solution]:
	"""
	Generates an initial population of solutions
	:param employees: list of employees
	:param missions: list of missions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:return: list of valid solutions
	"""
	solutions = [None] * size
	for i in range(size):
		solutions[i] = get_nearest_neighbour_solution(employees, missions, distance_matrix)
	
	return solutions


def genetic_algorithm_iteration(population: list[Solution], distance_matrix: list[list[float]]) -> Solution:

	new_population: list[Solution] = []

	# selection tournoi

	# croisement

	# mutation

	# selection  des meilleurs

	return new_population