from mission import Mission


class Schedule:
	missions: list[Mission]

	def __init__(self, missions: list[Mission] = []):
		self.missions = missions
