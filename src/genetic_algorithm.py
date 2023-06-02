from time import time
from models.solution import Solution
from genetic_algorithm_utils import *

def genetic_algorithm_iteration(population: list[Solution], distance_matrix: list[list[float]], size: int, crossover_rate: float, mutation_rate: float) -> list[Solution]:
	"""
	Performs a single iteration of the genetic algorithm
	:param population: list of solutions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:param crossover_rate: probability of crossover
	:param mutation_rate: probability of mutation
	:return: the best solution of the population
	"""

	for _ in range(round(crossover_rate * size)):
		parent1 = tournament_choice(population, distance_matrix, k=2)
		parent2 = tournament_choice(population, distance_matrix, k=2)
		child1, child2 = crossover(parent1, parent2)

		if random() < mutation_rate:
			child1.mutate()
		if random() < mutation_rate:
			child2.mutate()

		if child1.is_valid():
			population.append(child1)
		if child2.is_valid():
			population.append(child2)

	return pick_best_solutions(population, distance_matrix, size)


def genetic_algorithm(employees: list[Employee], missions: list[Mission], centers: list[Center], distance_matrix: list[list[float]], size: int, crossover_rate: float, mutation_rate: float, max_execution_time: int) -> Solution:
	"""
	Performs the genetic algorithm
	:param employees: list of employees to assign to missions
	:param missions: list of missions to assign to employees
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:param crossover_rate: probability of crossover
	:param mutation_rate: probability of mutation
	:param max_execution_time: maximum execution time of the algorithm in seconds
	:return: the best solution of the population
	"""
	start_time = time()
	population = generate_initial_population(employees, missions, centers, distance_matrix, size)
	while time() - start_time < max_execution_time:
		population = genetic_algorithm_iteration(population, distance_matrix, size, crossover_rate, mutation_rate)

	return pick_best_solutions(population, distance_matrix, 1)[0]