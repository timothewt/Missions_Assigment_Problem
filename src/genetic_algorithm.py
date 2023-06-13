from time import time
from models.solution import Solution
from utils import print_solution_evaluation, get_solution_individual_fitnesses
from genetic_algorithm_utils import *


def genetic_algorithm(employees: dict[int, Employee], missions: dict[Mission], centers: list[Center], distance_matrix: list[list[float]], size: int, crossover_rate: float, mutation_rate: float, max_execution_time: int, k: int, mutated_genes_per_chromosome_rate: float) -> Solution:
	"""
	Performs the genetic algorithm
	:param employees: dict of employees to assign to missions
	:param missions: dict of missions to assign to employees
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:param crossover_rate: probability of crossover
	:param mutation_rate: probability of mutation
	:param max_execution_time: maximum execution time of the algorithm in seconds
	:param k: number of individuals to consider in tournament selection
	:return: the best solution of the population
	"""
	start_time = time()
	population = generate_initial_population(employees, missions, centers, distance_matrix, size)

	fitness_memo = dict()  # used to store the fitness of solutions to avoid computing them multiple times
	best_solution = pick_best_solutions(population, employees, missions, distance_matrix, 1, len(centers), fitness_memo)[0]
	fitness_memo[best_solution] = best_solution.evaluate(distance_matrix, employees, missions, len(centers), fitness_memo)

	print("  Best initial solution:")

	print_solution_evaluation(fitness_memo[best_solution])

	print("\nRunning genetic algorithm...")

	nb_it = 0
	while time() - start_time < max_execution_time:
		population = genetic_algorithm_iteration(employees, missions, population, distance_matrix, size, crossover_rate, mutation_rate, k, len(centers), fitness_memo, mutated_genes_per_chromosome_rate)

		new_best = max(best_solution, population[0], key=lambda sol: (fitness_memo[sol]))
		if fitness_memo[new_best] != fitness_memo[best_solution]:
			best_solution = new_best
			print(f"  New best solution: {get_solution_individual_fitnesses(fitness_memo[best_solution])}")
		
		nb_it += 1
	print(f"  {nb_it} iterations")

	return best_solution


def genetic_algorithm_iteration(employees: dict[int, Employee], missions: dict[Mission], population: np.ndarray[Solution], distance_matrix: list[list[float]], size: int, crossover_rate: float, mutation_rate: float, k: int, centers_nb: int, fitness_memo: dict[Solution, tuple[int,int,int]], mutated_genes_per_chromosome_rate: float) -> list[Solution]:
	"""
	Performs a single iteration of the genetic algorithm
	:param employees: dict of employees to assign to missions
	:param missions: dict of missions to assign to employees
	:param population: list of solutions
	:param distance_matrix: matrix of distances between center-center, centers-missions, missions-missions
	:param size: size of the population
	:param crossover_rate: probability of crossover
	:param mutation_rate: probability of mutation
	:param k: number of individuals to consider in tournament selection
	:param centers_nb: number of centers
	:return: the best solution of the population
	"""

	for _ in range(round(crossover_rate * size / 2)):

		# choosing the parents for the crossover
		parent1 = tournament_choice(population, employees, missions, distance_matrix, k, centers_nb, fitness_memo)
		parent2 = tournament_choice(population, employees, missions, distance_matrix, k, centers_nb, fitness_memo)
		child1, child2 = crossover(parent1, parent2, len(missions))

		# mutating the children
		if random() < mutation_rate:
			child1.mutate(missions, employees, mutated_genes_per_chromosome_rate)
		if random() < mutation_rate:
			child2.mutate(missions, employees, mutated_genes_per_chromosome_rate)

		# adding the children to the population if they are valid
		if child1.is_valid(employees, missions, distance_matrix, centers_nb):
			population = np.append(population, child1)
		if child2.is_valid(employees, missions, distance_matrix, centers_nb):
			population = np.append(population, child2)
			
	return pick_best_solutions(population, employees, missions, distance_matrix, size, centers_nb, fitness_memo)
