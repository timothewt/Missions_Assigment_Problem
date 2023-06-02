from utils import *


if __name__ == "__main__":
	
	missions_nb, centers_nb = prompt_instance_parameters()

	instance_path = f"../instances/{missions_nb}Missions-{centers_nb}centres/"

	print(instance_path)
	