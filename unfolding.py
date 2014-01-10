# unfolding.py
# generates tikz code which draws a specified unfolding
# USAGE: unfolding.py theta1 theta2 leading_angle combinatorial_type

import sys
from math import sin, cos, atan2, pi

# opacity level for alternate triangles
opacity = .4

# determines the point of intersection of two lines starting at p1 and p2 with angles alpha1 and alpha2 respectively
def intersection(p1, alpha1, p2, alpha2):
	x1, y1 = p1
	x2, y2 = p2
	det = cos(alpha1) * sin(alpha2) - sin(alpha1) * cos(alpha2)
	t1 = (-sin(alpha2) * (x1 - x2) + cos(alpha2) * (y1 - y2)) / det
	return (x1 + t1 * cos(alpha1), y1 + t1 * sin(alpha1))

# reflects a point (z, w) across a line starting at (x, y) with angle alpha
def reflect(z, w, x, y, alpha):
	return cos(2 * alpha) * (z - x) + sin(2 * alpha) * (w - y) + x, sin(2 * alpha) * (z - x) - cos(2 * alpha) * (w - y) + y

class Triangle:
	def __init__(self, theta1, theta2, leading_angle):
		self.p1 = (0, 0)
		self.p2 = (cos(leading_angle), sin(leading_angle))
		self.p3 = intersection(self.p1, theta1 + leading_angle, self.p2, pi - theta2 + leading_angle)
		self.fill = False

	# gives result in tikz format
	def __str__(self):
		x1, y1 = self.p1
		x2, y2 = self.p2
		x3, y3 = self.p3
		outline = "({0:.4f}, {1:.4f}) -- ({2:.4f}, {3:.4f}) -- ({4:.4f}, {5:.4f}) -- cycle;".format(x1, y1, x2, y2, x3, y3);
		result = "\\draw " + outline
		if self.fill:
			result += "\n\\fill[opacity = {0:.2f}] ".format(opacity) + outline

		return result

	def reflect(self, edge):
		x1, y1 = self.p1
		x2, y2 = self.p2
		x3, y3 = self.p3
		if edge == '1':
			angle_of_reflection = atan2(y3 - y2, x3 - x2)
			self.p1 = reflect(x1, y1, x2, y2, angle_of_reflection)
		elif edge == '2':
			angle_of_reflection = atan2(y1 - y3, x1 - x3)
			self.p2 = reflect(x2, y2, x3, y3, angle_of_reflection)
		elif edge == '3':
			angle_of_reflection = atan2(y2 - y1, x2 - x1)
			self.p3 = reflect(x3, y3, x1, y1, angle_of_reflection)

		self.fill = not self.fill

	# unfolds the triangle along a combinatorial type specified by a string of 1s, 2s and 3s
	def unfold(self, combinatorial_type):
		print("\\begin{tikzpicture}")
		print(self)
		for edge in combinatorial_type:
			self.reflect(edge)
			print(self)
		print("\\end{tikzpicture}")

if __name__ == "__main__":
	triangle = Triangle(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
	triangle.unfold(sys.argv[4])
