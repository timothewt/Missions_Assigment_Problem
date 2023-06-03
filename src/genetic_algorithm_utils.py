import operator
from copy import deepcopy
from random import choice, random
from config import *
from models.solution import Solution
from models.employee import Employee
from models.mission import Mission
from models.center import Center


def generate_initial_population(employees: list[Employee], missions: list[Mission], centers: list[Center], distance_matrix: list[list[float]], size: int) -> list[Solution]:
	"""
	Generates an initial population of solutions
	:param employees: list of employees
	:param missions: list of missions
	:param centers: list of centers
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:return: list of valid solutions
	"""
	solutions = [None] * size
	for i in range(size):
		# as the nearest neighbour function has random choices, the population will be diverse enough
		solutions[i] = get_nearest_neighbour_solution(employees, missions, centers, distance_matrix)

	return solutions


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

	for mission_id, mission in missions.items():
		employees_distances_from_missions = [float('inf') for _ in range(len(employees))]

		for employee_index, employee in enumerate(employees):

			if employee.skill != mission.skill:  # if the skill does not match, does not consider this employee
				continue
		
			if employee.schedule.is_empty_for_day(mission.day):  # if the employee has no mission for the current day, he starts from its center
				employees_distances_from_missions[employee_index] = distance_matrix[employee.center_id - 1][centers_nb + mission_id - 1]
			else:  # gets the distance from the last mission of the employee
				last_mission = employee.schedule.missions[-1]

				distance_from_last_mission = distance_matrix[centers_nb + last_mission.id - 1][centers_nb + mission_id - 1]
				travel_time_from_last_mission = distance_from_last_mission * TRAVEL_SPEED

				if (last_mission.end_time + travel_time_from_last_mission) >= mission.start_time:  # if the employee cannot make it before the end of its last mission, does not consider him
					continue

				employees_distances_from_missions[employee_index] = distance_from_last_mission

		if (min_distance := min(employees_distances_from_missions)) == float('inf'):  # if no employee can make it to the mission, the mission is not assigned
			continue
		else:
			nearest_employees_indices = []  # finds the indices of all the closest employees from the mission
			for employee_index, employee_distance in enumerate(employees_distances_from_missions):
				if employee_distance == min_distance:
					nearest_employees_indices.append(employee_index)

			picked_employee =  employees[choice(nearest_employees_indices)]
			solution.assignments[mission_id - 1] = picked_employee.id  # picks a random employee from the closest one to add diversity
			picked_employee.schedule.add_mission(mission)

	for employee in employees:
		employee.reset_schedule()

	return solution


def tournament_choice(population: list[Solution], employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]], k: int) -> Solution:
	"""
	Performs a tournament iteration 
	:param population: list of solutions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param k: number of solutions to pick
	:return: list of solutions
	"""
	solutions = [None] * k
	for i in range(k):
		solutions[i] = choice(population)

	return pick_best_solutions(solutions, employees, missions, distance_matrix, 1)[0]


def pick_best_solutions(solutions: list[Solution], employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]], number_of_solutions_to_keep: int) -> list[Solution]:
	"""
	Picks the best solution in a list using cascade sorting
	:param solutions: solutions from which we pick the best
	:param employees: list of employees
	:param missions: list of missions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param number_of_solutions_to_keep: number of solutions to keep
	:return: the best solution in the list
	"""
	if len(solutions) <= number_of_solutions_to_keep:
		return solutions
	# sorts by assignment number, -1 * travel cost of employees and corresponding speciality assignments number, in descending order (the -1* is to sort in ascending order)
	solutions.sort(key=lambda sol: (sol.get_fitness_1(), -sol.get_fitness_2(distance_matrix), sol.get_fitness_3(employees, missions)), reverse=True)

	return solutions[:number_of_solutions_to_keep]


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
