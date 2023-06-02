from utils import *
from genetic_algorithm import *


if __name__ == "__main__":
	
	missions_nb, centers_nb = prompt_instance_parameters()

	instance_path = f"../instances/{missions_nb}Missions-{centers_nb}centres/"

	employees = open_employees_csv(instance_path)
	missions = open_missions_csv(instance_path)
	centers = open_centers_csv(instance_path)
	distance_matrix = open_distances_matrix(instance_path)

	solution = genetic_algorithm(employees, missions, distance_matrix, size=100, crossover_rate=0.8, mutation_rate=0.1, max_execution_time=10)
