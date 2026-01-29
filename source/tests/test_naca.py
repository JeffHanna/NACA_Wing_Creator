"""
Unit tests for NACA airfoil profile generators.
"""

import unittest
import numpy
from source.naca import NACA_4, NACA_5


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
		self.naca_5 = NACA_5(23016)
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
		expected_x = [0.9999999999999999, 0.9920730311441528, 0.9841468969130287, 0.9762220855321193, 0.9682990852764679, 0.9603783844435549, 0.9524604713259847, 0.9445458341839783, 0.9366349612176695, 0.9287283405392065, 0.9208264601446603, 0.9129298078857395, 0.9050388714413143, 0.8971541382887503, 0.8892760956750554, 0.8814052305878408, 0.8735420297260978, 0.8656869794707948, 0.8578405658552938, 0.8500032745355949, 0.8421755907604062, 0.834357999341045, 0.8265509846211752, 0.8187550304463802, 0.8109706201335813, 0.8031982364403017, 0.7954383615337796, 0.7876914769599378, 0.7799580636122149, 0.7722386017002578, 0.7645335707184879, 0.7568434494145404, 0.7491687157575834, 0.741509846906526, 0.7338673191781152, 0.7262416080149328, 0.718633187953295, 0.7110425325910613, 0.7034701145553618, 0.6959164054702439, 0.6883818759242514, 0.6808669954379384, 0.6733722324313238, 0.6658980541912995, 0.6584449268389914, 0.6510133152970862, 0.643603683257129, 0.6362164931467976, 0.6288522060971654, 0.6215112819099533, 0.6141941790247859, 0.606901354486453, 0.5996332639121891, 0.5923903614589742, 0.5851730997908668, 0.5779819300463759, 0.5708173018058783, 0.563679663059092, 0.5565694601726104]
		
		expected_y = [-5.3045818363293206e-17, 0.0016958769972471336, 0.0033762196308114584, 0.005041177775634219, 0.006690896289184211, 0.008325514852683642, 0.009945167821485043, 0.011549984084671873, 0.013140086933945477, 0.014715593941852373, 0.016276616849393064, 0.017823261463046525, 0.019355627561231895, 0.02087380881022092, 0.022377892689503256, 0.023867960426597574, 0.02534408694129099, 0.026806340799280494, 0.028254784175179355, 0.029689472824841592, 0.031110456066949527, 0.03251777677379847, 0.033911471371203344, 0.035291569847444915, 0.036658095771160304, 0.03801106631807745, 0.03935049230648191, 0.040676378241297266, 0.04198872236664945, 0.043287516726781064, 0.04457274723516934, 0.04584439375169555, 0.04710243016770778, 0.04834682449880573, 0.049577538985176244, 0.050794530199294675, 0.05199774916080467, 0.05318714145837963, 0.05436264737836434, 0.05552420203998838, 0.05667173553693605, 0.05780517308505456, 0.05892443517597344, 0.06002943773640537, 0.061120092292892884, 0.062196306141760395, 0.06325798252402778, 0.06430502080503632, 0.06533731665853443, 0.06635476225496827, 0.06735724645371713, 0.0683446549990122, 0.06931687071927314, 0.07027377372959676, 0.07121524163712734, 0.07214114974903857, 0.07305137128285474, 0.07394577757883683, 0.07482423831416049]
		
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
