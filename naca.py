"""
NACA airfoil profile generator.

This module provides classes for calculating NACA 4-series and 5-series airfoil coordinates. 
NACA (National Advisory Committee for Aeronautics) airfoils are standardized wing cross-sections used in 
aerospace engineering.

https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil
"""

import abc
import numpy
from typing import NamedTuple


Mean_Line_Data = NamedTuple('Mean_Line_Data', [('m', float), ('k1', float)])


class NACA_Base(abc.ABC):
	"""
	Base class for NACA airfoil profile calculations.

	Arguments:
		naca_number {str} -- A string of digits specifing the NACA number of the airfoil cross section to caclulate.

	Keyword Arguments:
		num_points {int} -- The number of points to calculate on each half (top and bottom) of the wing profile.
		half_cosine_spacing {bool} -- If true then half-cosine-spacing is used to calculate the distances between x axis 
		points. This packs more points toward the front of the wing profile, to increase fidelity of the leading edge.
	"""
	def __init__(self, naca_number, num_points = 200, half_cosine_spacing = True):
		self._naca_number : int = int(naca_number)
		assert 0 <= self._naca_number <= 99999
		self._x_points = self._half_cosine_spacing(0, 1, num_points) if half_cosine_spacing else numpy.linspace(0, 1, num_points)

	@property
	def naca_number(self):
		'''Getter for the NACA number being used as the input to this class.'''
		return self._naca_number

	@property
	def points(self):
		'''Getter for the points that define the airfoil this class represents.'''
		return self._calculate_points()

	@property
	def x_points(self):
		'''Getter for the x axis points calculated along the mean camber line.'''
		return self._x_points

	@staticmethod
	def _half_cosine_spacing(start, stop, max_points):
		"""
		Generate x-axis points using half-cosine spacing distribution.

		This spacing method concentrates more points near the leading edge (x=0) of the airfoil,
		providing higher fidelity where the curvature is greatest.

		Arguments:
			 start {float} -- Starting value (typically 0).
			 stop {float} -- Ending value (typically 1).
			 max_points {int} -- Number of points to generate.

		Returns:
			 numpy.ndarray -- Array of x-coordinates with half-cosine spacing.
		"""
		vals = [numpy.pi * 0.5 * x for x in numpy.linspace(start, stop, max_points)]
		x_points = numpy.array([1 - x for x in numpy.cos(vals)])
		return x_points

	@abc.abstractmethod
	def _calculate_points(self) -> tuple:
		"""
		Calculate the upper and lower surface coordinates of the airfoil.

		Returns:
			 tuple -- A tuple containing (x_positions, y_positions) for the airfoil profile.
		"""


class NACA_4(NACA_Base):
	"""	
	http://airfoiltools.com/airfoil/naca4digit

	Arguments:
		naca_number {str} -- A four digit string specifing the NACA number of the airfoil cross section to caclulate.

	Keyword Arguments:
		num_points {int} -- The number of points to calculate on each half (top and bottom) of the wing profile.
		half_cosine_spacing {bool} -- If true then half-cosine-spacing is used to calculate the distances between x axis 
		points. This packs more points toward the front of the wing profile, to increase fidelity of the leading edge.
	"""
	def __init__(self, naca_number, num_points = 200, half_cosine_spacing = True):
		super().__init__(naca_number, num_points = num_points, half_cosine_spacing = half_cosine_spacing)
		# Coeficient of lift
		self._cl : float = 1.0
		# Point of maximum camber
		self._p : float = (self._naca_number % 1e3 - self._naca_number % 1e2) / 1e3
		# Point of maximum thickness as a percentage along chord length
		self._t : float = self._naca_number % 1e2 / 1e2
		self._m : float = (self._naca_number - self._naca_number % 1e3) / 1e5
		self._x_over_c = self._x_points / self._cl

	def _mean_camber_line(self):
		"""
		Calculate the mean camber line y-coordinates for a NACA 4-series airfoil.

		The mean camber line is the curve halfway between the upper and lower surfaces.
		For symmetric airfoils (p=0), this returns zeros.

		Returns:
			 numpy.ndarray -- Y-coordinates of the mean camber line at each x_point.
		"""
		if self._p != 0:
			return numpy.where((self._x_points >= 0) & (self._x_points <= self._cl * self._p),
								self._m * (self._x_points / numpy.power(self._p, 2)) * (2.0 * self._p - self._x_over_c),
								self._m * ((self._cl - self._x_points) / numpy.power(1 - self._p, 2)) * (1.0 + self._x_over_c - 2.0 * self._p))		
		return numpy.where((self._x_points >= 0) & (self._x_points <= self._cl * self._p), 0, 0)

	def _calculate_points(self) -> tuple:
		"""
		Calculate the upper and lower surface coordinates for a NACA 4-series airfoil.

		Combines the mean camber line, thickness distribution, and camber angle to compute
		the final airfoil surface coordinates.

		Returns:
			 tuple -- (x_positions, y_positions) containing the complete airfoil outline.
			 The outline goes from trailing edge (upper) -> leading edge -> trailing edge (lower).
		"""
		dyc_dx = self._dyc_over_dx()
		th = numpy.arctan(dyc_dx)
		yt = self._thickness()
		yc = self._mean_camber_line()
		x_upper = self._x_points - yt * numpy.sin(th)
		y_upper = yc + yt * numpy.cos(th)
		x_lower = self._x_points + yt * numpy.sin(th)
		y_lower = yc - yt * numpy.cos(th)
		# Create continuous outline: upper reversed + lower (skip first to avoid duplicate leading edge)
		x_pos = numpy.concatenate([x_upper[::-1], x_lower[1:]])
		y_pos = numpy.concatenate([y_upper[::-1], y_lower[1:]])
		return(x_pos, y_pos)

	def _dyc_over_dx(self):
		"""
		Calculate the derivative of the mean camber line (dyc/dx) for a NACA 4-series airfoil.

		This derivative is used to determine the angle of the camber line, which is needed
		to properly offset the thickness distribution perpendicular to the camber line.

		Returns:
			 numpy.ndarray -- Slope of the mean camber line at each x_point.
		"""
		if self._p != 0:
			return numpy.where((self._x_points >= 0) & (self._x_points <= self._cl * self._p),
								2.0 * self._m / numpy.power(self._p, 2) * (self._p - self._x_over_c),
								2.0 * self._m / numpy.power(1 - self._p, 2) * (self._p - self._x_over_c))
		return numpy.where((self._x_points >= 0) & (self._x_points <= self._cl * self._p), 0, 0)

	def _thickness(self):
		"""
		Calculate the thickness distribution for a NACA 4-series airfoil.

		Uses the standard NACA 4-digit thickness formula with coefficients that define
		the airfoil shape. The thickness is half the distance between upper and lower surfaces.

		Returns:
			 numpy.ndarray -- Half-thickness values at each x_point.
		"""
		term1 = 0.2969 * numpy.sqrt(self._x_over_c)
		term2 = -0.1260 * self._x_over_c
		term3 = -0.3516 * numpy.power(self._x_over_c, 2)
		term4 = 0.2843 * numpy.power(self._x_over_c, 3)
		term5 = -0.1015 * numpy.power(self._x_over_c, 4)
		return 5 * self._t * self._cl * (term1 + term2 + term3 + term4 + term5)


class NACA_5(NACA_Base):
	"""
	(From Wikipedia)
	The NACA five-digit series describes more complex airfoil shapes. Its format is: LPSTT, where:

	L: a single digit representing the theoretical optimum lift coefficient at ideal angle-of-attack CLI = 0.15*L 
	(this is not the same as the lift coefficient, CL)
	P: a single digit for the x-coordinate of the point of maximum camber (max camber at x = 0.05*P)
	S: a single digit indicating whether the camber is simple (S=0) or reflex (S=1)
	TT: the maximum thickness in percent of chord, as in a four-digit NACA airfoil code
	For example, the NACA 23112 profile describes an airfoil with design lift coefficient of 0.3 (0.15*2), the point of 
	maximum camber located at 15% chord (5*3), reflex camber (1), and maximum thickness of 12% of chord length (12).

	https://en.wikipedia.org/wiki/NACA_airfoil#Five-digit_series
	http://airfoiltools.com/airfoil/naca5digit

	Arguments:
		naca_number {str} -- A five digit string specifing the NACA number of the airfoil cross section to caclulate.

	Keyword Arguments:
		num_points {int} -- The number of points to calculate on each half (top and bottom) of the wing profile.
		half_cosine_spacing {bool} -- If true then half-cosine-spacing is used to calculate the distances between x axis 
		points. This packs more points toward the front of the wing profile, to increase fidelity of the leading edge.
	"""
	def __init__(self, naca_number, num_points = 200, half_cosine_spacing = True):
		super().__init__(naca_number, num_points = num_points, half_cosine_spacing = half_cosine_spacing)		
		identifier = int(self._naca_number / 100)

		mean_line_map = {
			210 : Mean_Line_Data(m = 0.0580, k1 = 361.400),
			220 : Mean_Line_Data(m = 0.1260, k1 = 51.640),
			221 : Mean_Line_Data(m = 0.1300, k1 = 51.990),
			230 : Mean_Line_Data(m = 0.2025, k1 = 15.957),
			231 : Mean_Line_Data(m = 0.2170, k1 = 15.793),
			240 : Mean_Line_Data(m = 0.2900, k1 = 6.643),
			241 : Mean_Line_Data(m = 0.3180, k1 = 6.520),
			250 : Mean_Line_Data(m = 0.3910, k1 = 3.230),
			251 : Mean_Line_Data(m = 0.4410, k1 = 3.191)}
		mean_line_data = mean_line_map.get(identifier)
		assert mean_line_data is not None, f"No mean line data for {naca_number}"
		
		# Thickness coefficients
		self._a = (0.2969, -0.1260, -0.3516, 0.2843, -0.1036)
		# Coeficient of lift
		self._cl : float = int(str(naca_number)[0]) * 3.0 / 2.0 / 10.0
		# Point of maximum camber
		self._p : float = float('%.3f' % (int(str(naca_number) [1 : 3]) / 2.0 / 100.0))
		# Point of maximum thickness as percentage along chord length
		self._t : float = int(str(naca_number) [3 : 5]) / 100.0
		# mean_line_data = self._mean_line_map.get(self._p)
		self._m, self._k1 = mean_line_data

	def _mean_camber_line(self):
		"""Calculate the mean camber line y-coordinates for a NACA 5-series airfoil.

		Currently returns zeros - this is a placeholder implementation.

		Returns:
			 numpy.ndarray -- Y-coordinates of the mean camber line.
		"""
		return numpy.where((self._x_points <= self._p) & (self._x_points > self._p), 0, 0)

	def _calculate_points(self) -> tuple:
		"""Calculate the upper and lower surface coordinates for a NACA 5-series airfoil.

		For 5-series airfoils, the mean camber line is defined piecewise before and after
		the maximum camber position, using tabulated coefficients for different camber locations.

		Returns:
			 tuple -- (x_positions, y_positions) containing the complete airfoil outline.
			 The outline goes from trailing edge (upper) -> leading edge -> trailing edge (lower).
		"""
		yt = self._thickness()
		xc_1_mask = self._x_points <= self._p
		
		if self._p == 0:
			x_upper = self._x_points
			y_upper = yt
			x_lower = self._x_points
			y_lower = -yt
			zc = numpy.zeros_like(self._x_points)
		else:
			# Calculate yc for both regions
			yc_1 = self._k1 / 6.0 * (numpy.power(self._x_points, 3) - 3 * self._m * numpy.power(self._x_points, 2) +
									 numpy.power(self._m, 2) * (3 - self._m) * self._x_points)
			yc_2 = self._k1 / 6.0 * numpy.power(self._m, 3) * (1 - self._x_points)
			# Use the appropriate formula based on position
			yc = numpy.where(xc_1_mask, yc_1, yc_2)
			zc = self._cl / 0.3 * yc
			
			dyc_dx = self._dyc_over_dx()
			th = numpy.arctan(dyc_dx)
			x_upper = self._x_points - yt * numpy.sin(th)
			y_upper = zc + yt * numpy.cos(th)
			x_lower = self._x_points + yt * numpy.sin(th)
			y_lower = zc - yt * numpy.cos(th)
		
		# Create continuous outline: upper reversed + lower (skip first to avoid duplicate leading edge)
		x_pos = numpy.concatenate([x_upper[::-1], x_lower[1:]])
		y_pos = numpy.concatenate([y_upper[::-1], y_lower[1:]])
		return x_pos, y_pos

	def _dyc_over_dx(self):
		"""Calculate the derivative of the mean camber line for a NACA 5-series airfoil.

		The derivative is calculated separately for points before and after the maximum
		camber position using different formulas for each region.

		Returns:
			 numpy.ndarray -- Slope values of the mean camber line for all x positions.
		"""
		xc_1_mask = self._x_points <= self._p
		
		dyc_dx_1 = self._cl / 0.3 * (1.0 / 6.0) * self._k1 * (3 * numpy.power(self._x_points, 2) - 
															  6 * self._m * self._x_points + 
															  numpy.power(self._m, 2) * (3 - self._m))
		dyc_dx_2 = self._cl / 0.3 * (1.0 / 6.0) * self._k1 * numpy.power(self._m, 3) * numpy.ones_like(self._x_points)
		
		return numpy.where(xc_1_mask, dyc_dx_1, dyc_dx_2)

	def _thickness(self):
		"""Calculate the thickness distribution for a NACA 5-series airfoil.

		Uses the standard NACA 5-digit thickness formula with predefined coefficients.
		The formula is similar to the 4-series but with a slightly different trailing edge coefficient.

		Returns:
			 numpy.ndarray -- Half-thickness values at each x_point.
		"""
		term1 = self._a[0] * numpy.sqrt(self._x_points)
		term2 = self._a[1] * self._x_points
		term3 = self._a[2] * numpy.power(self._x_points, 2)
		term4 = self._a[3] * numpy.power(self._x_points, 3)
		term5 = self._a[4] * numpy.power(self._x_points, 4)
		return 5 * self._t * (term1 + term2 + term3 + term4 + term5)
