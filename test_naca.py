"""
Unit tests for NACA airfoil profile generators.
"""

import unittest
import numpy
from naca import NACA_4, NACA_5


class Test_NACA_4(unittest.TestCase):
	"""Test cases for NACA 4-series airfoil calculations."""

	def setUp(self):
		"""Set up test fixtures."""
		self.naca_4 = NACA_4('0018')
		self.points = self.naca_4.points

	def test_returns_tuple(self):
		"""Test that points returns a tuple."""
		self.assertIsInstance(self.points, tuple)
		self.assertEqual(len(self.points), 2)

	def test_x_positions_structure(self):
		"""Test that x positions are returned as a numpy array."""
		x_positions = self.points[0]
		self.assertIsInstance(x_positions, numpy.ndarray)

	def test_y_positions_structure(self):
		"""Test that y positions are returned as a numpy array."""
		y_positions = self.points[1]
		self.assertIsInstance(y_positions, numpy.ndarray)

	def test_point_count(self):
		"""Test that the correct number of points are generated.
		
		With 200 points each for upper and lower surfaces,
		and skipping the duplicate leading edge, we get 200 + 199 = 399 total points.
		"""
		self.assertEqual(self.points[0].shape[0], 399)
		self.assertEqual(self.points[1].shape[0], 399)

	def test_symmetric_airfoil(self):
		"""Test that NACA 0018 produces symmetric upper and lower surfaces."""
		x_all = self.points[0]
		y_all = self.points[1]
		
		# For a symmetric airfoil, the outline should be symmetric about the x-axis
		# The path goes: trailing edge upper -> leading edge -> trailing edge lower
		# Upper is first 200 points (reversed), lower is last 199 points
		x_upper = x_all[:200]
		y_upper = y_all[:200]
		x_lower = x_all[200:]
		y_lower = y_all[200:]
		
		# Reverse upper to compare properly (both should go leading->trailing)
		x_upper_forward = x_upper[::-1]
		y_upper_forward = y_upper[::-1]
		
		# X coordinates should match (excluding the duplicated leading edge point)
		numpy.testing.assert_array_almost_equal(x_upper_forward[1:], x_lower)
		
		# Y coordinates should be negatives of each other
		numpy.testing.assert_array_almost_equal(y_upper_forward[1:], -y_lower)

	def test_expected_values(self):
		"""Test that NACA 0018 produces expected coordinate values."""
		x_all = self.points[0]
		y_all = self.points[1]
		
		# Expected first 5 points starting from trailing edge (upper surface reversed)
		expected_x = numpy.array([1.0, 0.99210663, 0.98421376, 0.97632187, 0.96843145])
		expected_y = numpy.array([0.00189, 0.0035432, 0.00518033, 0.00680155, 0.00840701])
		
		numpy.testing.assert_array_almost_equal(x_all[:5], expected_x, decimal=6)
		numpy.testing.assert_array_almost_equal(y_all[:5], expected_y, decimal=6)

	def test_leading_edge_at_origin(self):
		"""Test that the leading edge is near x=0."""
		# Leading edge is at index 199 (last point of reversed upper surface)
		self.assertAlmostEqual(self.points[0][199], 0.0, places=5)

	def test_thickness_matches_specification(self):
		"""Test that maximum thickness is approximately 18% of chord (NACA 0018)."""
		y_all = self.points[1]
		
		# Maximum thickness is the max distance from the x-axis
		max_thickness = numpy.max(numpy.abs(y_all))
		# For symmetric airfoil, this should be about 0.09 (half of 18%)
		self.assertAlmostEqual(max_thickness, 0.09, delta=0.01)


class Test_NACA_5(unittest.TestCase):
	"""Test cases for NACA 5-series airfoil calculations."""

	def setUp(self):
		"""Set up test fixtures."""
		self.naca_5 = NACA_5(23112)
		self.points = self.naca_5.points

	def test_returns_tuple(self):
		"""Test that points returns a tuple."""
		self.assertIsInstance(self.points, tuple)
		self.assertEqual(len(self.points), 2)

	def test_positions_structure(self):
		"""Test that positions are returned as numpy arrays."""
		x_positions = self.points[0]
		y_positions = self.points[1]
		self.assertIsInstance(x_positions, numpy.ndarray)
		self.assertIsInstance(y_positions, numpy.ndarray)

	def test_point_count(self):
		"""Test that the correct number of points are generated.
		
		With 200 points each for upper and lower surfaces,
		and skipping the duplicate leading edge, we get 200 + 199 = 399 total points.
		"""
		self.assertEqual(self.points[0].shape[0], 399)
		self.assertEqual(self.points[1].shape[0], 399)

	def test_expected_values(self):
		"""Test that NACA 23112 produces expected coordinate values."""
		x_all = self.points[0]
		y_all = self.points[1]
		
		# Expected first 5 points starting from trailing edge (upper surface reversed)
		expected_x = [0.9999999999999999, 0.9920759434321833, 0.9841526917768977, 0.9762307335672841, 0.9683105573764292, 0.9603926517899455, 0.9524775053783701, 0.9445656066693884, 0.9366574441198768, 0.9287535060877709, 0.9208542808037568, 0.9129602563427879, 0.9050719205954285, 0.8971897612390253, 0.8893142657087102, 0.8814459211682353, 0.8735852144806416, 0.8657326321787658, 0.8578886604355853, 0.8500537850344078, 0.8422284913389049, 0.8344132642629946, 0.8266085882405766, 0.8188149471951223, 0.8110328245091246, 0.8032627029934128, 0.7955050648563324, 0.7877603916727971, 0.7800291643532197, 0.7723118631123201, 0.7646089674378224, 0.7569209560590402, 0.7492483069153583, 0.741591497124616, 0.7339510029513954, 0.7263272997752231, 0.7187208620586885, 0.7111321633154842, 0.703561676078379, 0.6960098718671219, 0.6884772211562907, 0.6809641933430874, 0.6734712567150859, 0.6659988784179435, 0.6585475244230758, 0.6511176594953088, 0.6437097471605078, 0.6363242496731968, 0.6289616279841708, 0.6216223417081073, 0.6143068490911899, 0.6070156069787428, 0.5997490707828906, 0.5925076944502464, 0.5852919304296357, 0.5781022296398656, 0.5709390414375435, 0.5638028135849562, 0.5566939922180124]
		
		expected_y = [-3.863222309798263e-17, 0.0013533386942992636, 0.0026950229050624205, 0.004025159942585562, 0.005343853355137039, 0.006651202810207523, 0.007947303982622497, 0.009232248449571604, 0.010506123592601873, 0.011769012506615207, 0.013020993915901082, 0.014262142097229993, 0.015492526810023803, 0.016712213233613132, 0.017921261911583296, 0.019119728703203585, 0.02030766474192667, 0.021485116400938385, 0.022652125265730134, 0.02380872811365875, 0.024954956900452407, 0.026090838753613343, 0.02721639597266076, 0.028331646036152278, 0.02943660161541243, 0.03053127059489281, 0.03161565609908035, 0.03268975652586451, 0.03375356558626623, 0.03480707235042805, 0.03585026129975574, 0.0368831123850973, 0.037905601090840665, 0.03891769850480168, 0.039919371393773856, 0.04091058228460117, 0.041891289550633565, 0.04286144750341719, 0.04382100648946867, 0.044769912991976885, 0.04570810973727082, 0.04663553580588982, 0.04755212674808607, 0.04845781470358676, 0.049352528525439456, 0.05023619390776013, 0.05110873351720112, 0.051970067127952095, 0.05282011176008456, 0.053658781821048884, 0.05448598925012839, 0.05530164366565508, 0.05610565251478718, 0.05689792122564966, 0.057678353361634786, 0.05844685077766, 0.0592033137781792, 0.059947641276741355, 0.06067973095689183]
		
		for i in range(len(expected_x)):
			self.assertAlmostEqual(x_all[i], expected_x[i], places=6)
			self.assertAlmostEqual(y_all[i], expected_y[i], places=6)

	def test_camber_present(self):
		"""Test that NACA 23112 produces cambered airfoil (not symmetric)."""
		# For a cambered airfoil, the mean y value should not be zero
		y_all = self.points[1]
		y_mean = numpy.mean(y_all)
		self.assertNotAlmostEqual(y_mean, 0.0, places=3)

	def test_coordinates_match_count(self):
		"""Test that x and y coordinate arrays have matching lengths."""
		self.assertEqual(self.points[0].shape[0], self.points[1].shape[0])


if __name__ == '__main__':
	unittest.main()
