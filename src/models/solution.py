class Solution:
	assignments: list[int]
	

	def __init__(self, size: int):
		self.assignments = [0] * size


	def get_fitness_1(self) -> float:
		return 0


	def get_fitness_2(self, distance_matrix: list[list[float]]) -> float:
		return 0


	def get_fitness_3(self) -> float:
		return 0


	def mutate(self) -> None:
		pass

	def is_valid(self):
		return True


	def __str__(self):
		return f"{self.assignments}"


	def __repr__(self):
		return self.__str__()

