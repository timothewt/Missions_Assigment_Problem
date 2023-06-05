from copy import deepcopy
import numpy as np
from random import choice, random, randint
from config import *
from models.solution import Solution
from models.employee import Employee
from models.mission import Mission
from models.center import Center


def generate_initial_population(employees: dict[int, Employee], missions: dict[int, Mission], centers: list[Center], distance_matrix: list[list[float]], size: int) -> np.ndarray[Solution]:
	"""
	Generates an initial population of solutions
	:param employees: list of employees
	:param missions: dict of missions
	:param centers: list of centers
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:return: list of valid solutions
	"""
	solutions = np.array([None] * size)
	for i in range(size):
		# as the nearest neighbour function has random choices, the population will be diverse enough
		solutions[i] = get_nearest_neighbour_solution(employees, missions, centers, distance_matrix)

	return solutions


def get_nearest_neighbour_solution(employees: dict[int, Employee], missions: dict[int, Mission], centers: list[Center], distance_matrix: list[list[float]]) -> Solution:
	"""
	Generates a valid solution using the nearest neighbour algorithm
	:param employees: list of employees
	:param missions: dict of missions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:return: A valid solution
	"""
	solution = Solution()
	centers_nb = len(centers)

	for mission_id, mission in sorted(missions.items(), key=lambda m: (m[1].day, m[1].start_time)):
		employees_distances_from_mission: dict[int, float] = {}

		for employee_id, employee in employees.items():

			if employee.skill != mission.skill:  # if the skill does not match, does not consider this employee
				continue
		
			if employee.schedule.is_empty_for_day(mission.day):
				# if the employee has no mission for the current day, he starts from its center
				employees_distances_from_mission[employee_id] = distance_matrix[employee.center_id - 1][centers_nb + mission_id - 1]
			else:
				# gets the distance from the last mission of the employee
				last_mission = employee.schedule.missions[-1]

				distance_from_last_mission = distance_matrix[centers_nb + last_mission.id - 1][centers_nb + mission_id - 1]
				travel_time_from_last_mission = distance_from_last_mission * TRAVEL_SPEED

				if (last_mission.end_time + travel_time_from_last_mission) >= mission.start_time:
					# if the employee cannot make it before the end of its last mission, does not consider him
					continue

				employees_distances_from_mission[employee_id] = distance_from_last_mission

		if len(employees_distances_from_mission) == 0:  # if no employee can make it to the mission, the mission is not assigned
			continue
		else:
			min_distance = min(employees_distances_from_mission.values())
			if random() < .3:
				# 30% of chances to pick an employee among all available ones, who may not be the closest, to add diversity to the initial solutions
				nearest_employees_ids = [employee_id for employee_id in employees_distances_from_mission.keys()]
			else:
				nearest_employees_ids = [employee_id for employee_id, employee_distance in employees_distances_from_mission.items() if employee_distance == min_distance]  # finds the indices of all the closest employees from the mission

			picked_employee = employees[choice(nearest_employees_ids)]

			solution.assignments[mission_id] = picked_employee.id  # picks a random employee from the closest one to add diversity
			picked_employee.schedule.add_mission(mission, distance_matrix, centers_nb, picked_employee.center_id)

	for _, employee in employees.items():
		employee.reset_schedule()

	return solution


def tournament_choice(population: list[Solution], employees: dict[int, Employee], missions: dict[int, Mission], distance_matrix: list[list[float]], k: int, centers_nb: int, fitness_memo: dict[Solution, tuple[int,int,int]]) -> Solution:
	"""
	Performs a tournament iteration 
	:param population: list of solutions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param k: number of solutions to pick
	:return: list of solutions
	"""
	solutions = np.array([None] * k)
	for i in range(k):
		solutions[i] = choice(population)

	return pick_best_solutions(solutions, employees, missions, distance_matrix, 1, centers_nb, fitness_memo)[0]


def pick_best_solutions(solutions: np.ndarray[Solution], employees: dict[int, Employee], missions: dict[int, Mission], distance_matrix: list[list[float]], number_of_solutions_to_keep: int, centers_nb: int, fitness_memo: dict[Solution, tuple[int,int,int]]) -> np.ndarray[Solution]:
	"""
	Picks the best solution in a list using cascade sorting
	:param solutions: solutions from which we pick the best
	:param employees: dict of employees
	:param missions: dict of missions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param number_of_solutions_to_keep: number of solutions to keep
	:return: the best solution in the list
	"""
	if len(solutions) <= number_of_solutions_to_keep:
		return solutions

	for sol in solutions:
		if sol not in fitness_memo:
			fitness_memo[sol] = (sol.get_fitness_1(), sol.get_fitness_2(employees, missions, distance_matrix, centers_nb), sol.get_fitness_3(employees, missions))

	# sorts by assignment number, -1 * travel cost of employees and corresponding speciality assignments number, in descending order (the -1* is to sort in ascending order)

	intermediate_arr = np.array([fitness_memo[x] for x in solutions], dtype=[('value1', float), ('value2', float), ('value3', float)])
	sorted_indices = np.lexsort((-intermediate_arr['value1'], intermediate_arr['value2'], -intermediate_arr['value3']))

	return solutions[sorted_indices][:number_of_solutions_to_keep]

def crossover(solution1: Solution, solution2: Solution, missions_nb: int) -> list[Solution|Solution]:
	"""
	Performs a crossover between two solutions using uniform crossover
	:param solution1: first solution
	:param solution2: second solution
	:return: two children solutions
	"""
	child1 = Solution()
	child2 = Solution()

	for mission_id in range(1, missions_nb + 1):
		gene_mask = randint(0, 1)
		assignment1 = solution1.assignments[mission_id] if mission_id in solution1.assignments else None
		assignment2 = solution2.assignments[mission_id] if mission_id in solution2.assignments else None

		if gene_mask:
			if assignment1 is not None:
				child1.assignments[mission_id] = assignment1
			if assignment2 is not None:
				child2.assignments[mission_id] = assignment2
		else:
			if assignment2 is not None:
				child1.assignments[mission_id] = assignment2
			if assignment1 is not None:
				child2.assignments[mission_id] = assignment1

	return child1, child2
