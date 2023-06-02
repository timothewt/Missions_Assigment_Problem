from utils import *
from genetic_algorithm import *


if __name__ == "__main__":
	
	missions_nb, centers_nb = prompt_instance_parameters()

	instance_path = f"../instances/{missions_nb}Missions-{centers_nb}centres/"

	employees = open_employees_csv(instance_path)
	missions = open_missions_csv(instance_path)
	centers = open_centers_csv(instance_path)
	distance_matrix = open_distances_matrix(instance_path)

	size, crossover_rate, mutation_rate, max_execution_time, k = prompt_genetic_algorithm_parameters(100, .8, .1, 10, 3)

	print("Running genetic algorithm...")

	solution = genetic_algorithm(employees, missions, centers, distance_matrix, size=size, crossover_rate=crossover_rate, mutation_rate=mutation_rate, max_execution_time=max_execution_time, k=k)

	missions.sort(key=lambda mission: mission.id)

	print("\nSolution:")

	for i in range(len(solution.assignments)):
		print("Mission", missions[i].speciality, "is assigned to employee", employees[solution.assignments[i] - 1].speciality)

	evaluation = solution.evaluate(employees, missions, distance_matrix)

	print(f"\nNumber of missions assigned: {evaluation[0]}")
	print(f"Total distance traveled: {evaluation[1]}")
	print(f"Number of corresponding specialities: {evaluation[2]}")
	