from models.solution import Solution
from models.employee import Employee
from models.mission import Mission
from models.center import Center
from config import *
from copy import deepcopy
from random import choice, random


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
		
			if employee.skill != mission.skill:  # if the skill does not match, does not consider this employee
				continue
		
			if employee.schedule.is_empty_for_day(mission.day):  # if the employee has no mission for the current day, he starts from its center
				employees_distances_from_missions[employee_index] = distance_matrix[employee.center_id - 1][centers_nb + mission_index]
			else:  # gets the distance from the last mission of the employee
				distance_from_last_mission = distance_matrix[centers_nb + employee.schedule.missions[-1].id - 1][centers_nb + mission_index]
				travel_time_from_last_mission = distance_from_last_mission * TRAVEL_SPEED

				if employee.schedule.missions[-1].end_time + travel_time_from_last_mission < mission.start_time:  # if the employee cannot make it before the end of its last mission, does not consider him
					continue

				employees_distances_from_missions[employee_index] = distance_from_last_mission


		min_distance = float('inf')
		nearest_employees_indices = []  # finds the indices of all the closest employees from the mission

		for employee_index, employee_distance in enumerate(employees_distances_from_missions):
			if employee_distance < min_distance:
				min_distance = employee_distance
				nearest_employees_indices = [employee_index]
			elif employee_distance == min_distance:
				nearest_employees_indices.append(employee_index)

		solution.assignments[mission.id - 1] = employees[choice(nearest_employees_indices)].id  # picks a random employee from the closest one to add diversity

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
		# as the nearest neighbour function has random choices, the population will be diverse enough
		solutions[i] = get_nearest_neighbour_solution(employees, missions, distance_matrix)
	
	return solutions


def crossover(solution1: Solution, solution2: Solution) -> list[Solution|Solution]:
	"""
	Performs a crossover between two solutions using uniform crossover
	:param solution1: first solution
	:param solution2: second solution
	:return: two children solutions
	"""
	size = len(solution1.assignments)
	mask = [round(random()) for _ in range(size)]
	child1 = Solution(size)
	child2 = Solution(size)

	for i in range(size):
		child1.assignments[i] = mask[i] * solution1.assignments[i] + (1 - mask[i]) * solution2.assignments[i]
		child2.assignments[i] = mask[i] * solution2.assignments[i] + (1 - mask[i]) * solution1.assignments[i]

	return child1, child2


def tournament_choice(population: list[Solution], k: int) -> list[Solution|Solution]:
	"""
	Performs a tournament iteration 
	:param population: list of solutions
	:param k: number of solutions to pick
	:return: list of solutions
	"""
	solutions = [None] * k
	for i in range(k):
		solutions[i] = choice(population)

	return pick_best_solution(solutions)


def pick_best_solution(solutions: list[Solution]) -> Solution:
	"""
	Picks the best solution in a list using cascade sorting
	:param solutions: solutions from which we pick the best
	:return: the best solution in the list
	"""
	size: int = len(solutions)

	solutions.sort(key=lambda x: x.get_fitness_1(), reverse=True)  # first sorts by assignment number fitness
	for i in range(size - 1, 0, -1):
		if solutions[i].get_fitness_1() < solutions[0].get_fitness_1():  # eliminates all the solutions with a smaller assignments number
			break
		solutions.pop()

	solutions.sort(key=lambda x: x.get_fitness_2())  # then sorts by travel cost of employees
	for i in range(size - 1, 0, -1):
		if solutions[i].get_fitness_2() < solutions[0].get_fitness_2():  # eliminates all the solutions with a bigger travel cost
			break
		solutions.pop()

	solutions.sort(key=lambda x: x.get_fitness_3(), reverse=True)  # finally sorts by corresponding speciality assignments number
	for i in range(size - 1, 0, -1):
		if solutions[i].get_fitness_3() < solutions[0].get_fitness_3():  # eliminates all the solutions with a smaller corresponding speciality assignments number
			break
		solutions.pop()
	
	return choice(solutions)  # if there are more than one solution remaining, picks a random one to add diversity


def genetic_algorithm_iteration(population: list[Solution], distance_matrix: list[list[float]], size: int) -> Solution:

	new_population: list[Solution] = []

	# selection tournoi

	# croisement

	# mutation

	# selection  des meilleurs

	return new_population