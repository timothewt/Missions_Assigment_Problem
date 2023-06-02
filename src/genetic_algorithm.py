from models.solution import Solution
from models.employee import Employee
from models.mission import Mission


def get_nearest_neighbour_solution(employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]]) -> Solution:
	"""
	Generates a solution using the nearest neighbour algorithm
	:param employees: list of employees
	:param missions: list of missions
	:param distance_matrix: matrix of distances between missions
	:return: a solution
	"""
	solution = Solution()
	return solution


def generate_initial_population(employees: list[Employee], missions: list[Mission], distance_matrix: list[list[float]]) -> list[Solution]:
	solution




	return []


def genetic_algorithm_iteration(population: list[Solution], distance_matrix: list[list[float]]) -> Solution:

	new_population: list[Solution] = []

	# selection tournoi

	# croisement

	# mutation

	# selection  des meilleurs

	return new_population