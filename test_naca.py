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
		"""Test that x positions are returned as numpy arrays in a tuple."""
		x_positions = self.points[0]
		self.assertIsInstance(x_positions, tuple)
		self.assertEqual(len(x_positions), 2)
		self.assertIsInstance(x_positions[0], numpy.ndarray)
		self.assertIsInstance(x_positions[1], numpy.ndarray)

	def test_y_positions_structure(self):
		"""Test that y positions are returned as numpy arrays in a tuple."""
		y_positions = self.points[1]
		self.assertIsInstance(y_positions, tuple)
		self.assertEqual(len(y_positions), 2)
		self.assertIsInstance(y_positions[0], numpy.ndarray)
		self.assertIsInstance(y_positions[1], numpy.ndarray)

	def test_point_count(self):
		"""Test that the correct number of points are generated (200 default)."""
		self.assertEqual(self.points[0][0].shape[0], 200)
		self.assertEqual(self.points[0][1].shape[0], 200)
		self.assertEqual(self.points[1][0].shape[0], 200)
		self.assertEqual(self.points[1][1].shape[0], 200)

	def test_symmetric_airfoil(self):
		"""Test that NACA 0018 produces symmetric upper and lower surfaces."""
		x_upper = self.points[0][0]
		y_upper = self.points[0][1]
		x_lower = self.points[1][0]
		y_lower = self.points[1][1]
		
		# For symmetric airfoil, x coordinates should be the same
		numpy.testing.assert_array_almost_equal(x_upper, x_lower)
		
		# Y coordinates should be negatives of each other
		numpy.testing.assert_array_almost_equal(y_upper, -y_lower)

	def test_expected_values(self):
		"""Test that NACA 0018 produces expected coordinate values."""
		x_upper = self.points[0][0]
		y_upper = self.points[0][1]
		
		# Expected first 5 points (captured from known good output)
		expected_x = numpy.array([0.00000000e+00, 3.11531058e-05, 1.24610482e-04, 
								   2.80366307e-04, 4.98410874e-04])
		expected_y = numpy.array([0., 0.0014879, 0.0029687, 0.00444238, 0.0059089])
		
		numpy.testing.assert_array_almost_equal(x_upper[:5], expected_x, decimal=6)
		numpy.testing.assert_array_almost_equal(y_upper[:5], expected_y, decimal=6)

	def test_leading_edge_at_origin(self):
		"""Test that the leading edge starts at x=0."""
		self.assertAlmostEqual(self.points[0][0][0], 0.0)
		self.assertAlmostEqual(self.points[1][0][0], 0.0)

	def test_thickness_matches_specification(self):
		"""Test that maximum thickness is approximately 18% of chord (NACA 0018)."""
		y_upper = self.points[0][1]
		y_lower = self.points[1][1]
		
		# Maximum thickness should be approximately 0.18 (18%)
		max_thickness = numpy.max(y_upper - y_lower)
		self.assertAlmostEqual(max_thickness, 0.18, delta=0.01)


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
		"""Test that positions are returned as lists."""
		x_positions = self.points[0]
		y_positions = self.points[1]
		self.assertIsInstance(x_positions, list)
		self.assertIsInstance(y_positions, list)

	def test_point_count(self):
		"""Test that the correct number of points are generated.
		
		NACA 5 generates upper points reversed + lower points (minus first),
		so 200 + 199 = 399 total points.
		"""
		self.assertEqual(len(self.points[0]), 399)
		self.assertEqual(len(self.points[1]), 399)

	def test_expected_values(self):
		"""Test that NACA 23112 produces expected coordinate values."""
		x_positions = self.points[0]
		y_positions = self.points[1]
		
		# Expected first 5 points (captured from known good output)
		# Note: Values are reversed (starting from trailing edge)
		expected_x = [0.9999999999999999, 0.9920814316306863, 0.9841636121813623, 
					  0.9762470307649335, 0.9683321765161483]
		expected_y = [-3.917141339646752e-17, 0.0013154867596106587, 0.0026193200312160827, 
					  0.003911609505948258, 0.005192461112173172]
		
		for i in range(5):
			self.assertAlmostEqual(x_positions[i], expected_x[i], places=6)
			self.assertAlmostEqual(y_positions[i], expected_y[i], places=6)

	def test_camber_present(self):
		"""Test that NACA 23112 produces cambered airfoil (not symmetric)."""
		# For a cambered airfoil, mean of y values should not be zero
		y_mean = numpy.mean(self.points[1])
		self.assertNotAlmostEqual(y_mean, 0.0, places=3)

	def test_coordinates_match_count(self):
		"""Test that x and y coordinate lists have matching lengths."""
		self.assertEqual(len(self.points[0]), len(self.points[1]))


if __name__ == '__main__':
	unittest.main()
