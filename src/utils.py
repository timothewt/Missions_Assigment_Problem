import csv
import operator
from models.mission import Mission
from models.employee import Employee
from models.center import Center


def open_missions_csv(path_to_folder: str) -> list[Mission]:
	"""
	Opens the missions csv file and returns a list of missions
	:param path_to_folder: path to the folder of the csv file
	:return: list of missions
	"""
	missions = []
	with open(path_to_folder + "missions.csv", newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			missions.append(Mission(int(row[0]), int(row[1]), int(row[2]), int(row[3]), row[4], row[5]))
	missions.sort(key=operator.attrgetter('day', 'start_time'))
	return missions


def open_employees_csv(path_to_folder: str) -> list[Employee]:
	"""
	Opens the employees csv file and returns a list of employees
	:param path_to_folder: path to the csv file
	:return: list of employees
	"""
	employees = []
	with open(path_to_folder + "employees.csv", newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			employees.append(Employee(int(row[0]), int(row[1]), row[2], row[3]))
	return employees


def open_centers_csv(path_to_folder: str) -> list[Center]:
	"""
	Opens the centers csv file and returns a list of centers
	:param path_to_folder: path to the csv file
	:return: list of centers
	"""
	centers = []
	with open(path_to_folder + "centers.csv", newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			centers.append(Center(int(row[0]), row[1]))
	return centers


def open_distances_matrix(path_to_folder: str) -> list[list[float]]:
	"""
	Opens the distances matrix csv file and returns the matrix
	:param path_to_folder: path to the csv file
	:return: list of lists
	"""
	distances = []
	with open(path_to_folder + "distances.csv", newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			distances.append([float(x) for x in row])
	return distances
	

def prompt_instance_parameters() -> list[int|int]:
	"""
	Prompts the user to choose an instance and returns the number of missions and centers
	:return: list of missions number and centers number
	"""
	missions_nb = [30, 66, 94, 94, 100, 200]
	centers_nb = [2, 2, 2, 3, 2, 2]

	print(f"Please enter the instance number (1-{len(missions_nb)}):")
	for i in range(len(missions_nb)):
		print(f"{i+1} - {missions_nb[i]} missions, {centers_nb[i]} centers")

	instance_id = int(input('>>> '))
	while instance_id < 1 or instance_id > 6:
		print(f"Please enter a valid number (1-{len(missions_nb)}):")
		instance_id = int(input('>>> '))

	return [missions_nb[instance_id - 1], centers_nb[instance_id - 1]]
	

def prompt_genetic_algorithm_parameters(default_size: int, default_crossover_rate: float, default_mutation_rate: float, default_max_time: float, default_k: int) -> list[int|float|float|float|int]:
	"""
	Prompts the user to choose the parameters of the genetic algorithm and returns them
	These are : population size, crossover rate, mutation rate, max execution time, k (number of solutions picked for a tournament)
	:return: list of parameters
	"""
	print("Default parameters:")
	print("Population size:", default_size)
	print("Crossover rate:", default_crossover_rate)
	print("Mutation rate:", default_mutation_rate)
	print("Max execution time:", default_max_time)
	print("Number of individuals to pick for a tournament:", default_k)
	print("Do you want to input custom parameters or keep the default one (C: custom/D: default) ?")
	choice = input(">>> ")
	while choice != 'C' and choice != 'c' and choice != 'D' and choice != 'd':
		print("Please enter a valid choice (C: custom/D: default):")
		choice = input(">>> ")

	if choice == "D" or choice == "d":
		return default_size, default_crossover_rate, default_mutation_rate, default_max_time, default_k

	print("Please enter the parameters of the genetic algorithm:")

	print('Population size:')
	size = int(input(">>> "))
	while size < 0:
		print("Please enter a valid population size (positive integer):")
		size = int(input(">>> "))

	print('Crossover rate:')
	crossover_rate = float(input(">>> "))
	while crossover_rate < 0 or crossover_rate > 1:
		print("Please enter a valid crossover rate (between 0 and 1):")
		crossover_rate = float(input(">>> "))

	print('Mutation rate:')
	mutation_rate = float(input(">>> "))
	while mutation_rate < 0 or mutation_rate > 1:
		print("Please enter a valid mutation rate (between 0 and 1):")
		mutation_rate = float(input(">>> "))

	print('Max execution time (in seconds):')
	max_execution_time = float(input(">>> "))
	while max_execution_time < 0:
		print("Please enter a valid max execution time (positive float):")
		max_execution_time = float(input(">>> "))

	print('Number of best individuals to pick for a tournament:')
	k = int(input(">>> "))
	while k < 0:
		print("Please enter a valid number (positive integer):")
		k = int(input(">>> "))

	return size, crossover_rate, mutation_rate, max_execution_time, k