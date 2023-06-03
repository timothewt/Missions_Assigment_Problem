from utils import *
from genetic_algorithm import *


if __name__ == "__main__":
	
	missions_nb, centers_nb = prompt_instance_parameters()

	instance_path = f"../instances/{missions_nb}Missions-{centers_nb}centres/"

	employees = open_employees_csv(instance_path)
	missions = open_missions_csv(instance_path)
	centers = open_centers_csv(instance_path)
	distance_matrix = open_distances_matrix(instance_path)

	size, crossover_rate, mutation_rate, max_execution_time, k = prompt_genetic_algorithm_parameters(300, .8, .4, 10, 3)

	solution = genetic_algorithm(employees, missions, centers, distance_matrix, size=size, crossover_rate=crossover_rate, mutation_rate=mutation_rate, max_execution_time=max_execution_time, k=k)

	print("\nSolution:")

	for i in range(1, len(missions) + 1):
		if i in solution.assignments:
			print(f"Mission {missions[i].id} assigned to employee no.{solution.assignments[i]} and center no.{employees[solution.assignments[i] - 1].center_id}")
		else:
			print(f"Mission {missions[i].id} not assigned")

	evaluation = solution.evaluate(distance_matrix, employees, missions)

	print(f"\nNumber of missions assigned: {evaluation[0]}")
	print(f"Total distance traveled: {evaluation[1]}")
	print(f"Number of corresponding specialities: {evaluation[2]}")
	