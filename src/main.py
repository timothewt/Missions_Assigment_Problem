from utils import *

if __name__ == "__main__":
	print(open_missions_csv("../instances/30Missions-2centres/missions.csv"))
	print(open_centers_csv("../instances/30Missions-2centres/centers.csv"))
	print(open_employees_csv("../instances/30Missions-2centres/employees.csv"))
	print(open_distances_matrix("../instances/30Missions-2centres/distances.csv"))
