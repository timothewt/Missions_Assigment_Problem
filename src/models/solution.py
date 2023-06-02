class Solution:
	assigments: list[int]

	def __init__(self, size: int):
		assigments = [0] * size


	def get_fitness_1(self) -> float:
		return 0


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:
		return 0


	def get_fitness_3(self) -> float:
		return 0


	def mutate(self) -> None:
		pass


	def __str__(self):
		return f"{self.assigments}"


	def __repr__(self):
		return self.__str__()

