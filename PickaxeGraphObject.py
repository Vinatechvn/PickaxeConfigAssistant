import json
class PickaxeGraphObject():
	def __init__(self, a, b, c, d):
		self.name = a
		self.units = b
		self.x = c
		self.y = d
		self.y_label = "{} {}".format(str(self.y), self.units)
	def __str__(self):
		return json.dumps({
			"name": self.name,
			"units": self.units,
			"x": self.x,
			"y": self.y,
			"y_label": self.y_label,
			"colour": "#406485"
		})
