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
		expected_x = [0.9999999999999999, 0.9920814316306863, 0.9841636121813623,
					  0.9762470307649335, 0.9683321765161483]
		expected_y = [-3.917141339646752e-17, 0.0013154867596106587, 0.0026193200312160827,
					  0.003911609505948258, 0.005192461112173172]
		
		for i in range(5):
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
