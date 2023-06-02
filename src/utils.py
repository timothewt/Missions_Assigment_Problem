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
	missions_nb = [100, 200, 30, 66, 94, 94]
	centers_nb = [2, 2, 2, 2, 2, 3]

	print(f"Please enter the instance number (1-{len(missions_nb)})):")
	for i in range(len(missions_nb)):
		print(f"{i+1} - {missions_nb[i]} missions, {centers_nb[i]} centers")

	instance_id = int(input('>>>'))
	while instance_id < 1 or instance_id > 6:
		print(f"Please enter a valid number (1-{len(missions_nb)}):")
		instance_id = int(input('>>>'))

	return [missions_nb[instance_id - 1], centers_nb[instance_id - 1]]
	