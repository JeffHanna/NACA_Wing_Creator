"""[summary]

Returns:
	 [type] -- [description]
"""

import abc
from collections import namedtuple
import matplotlib.pyplot # FOR TESTING ONLY. TO BE REMOVED WHEN THIS LIBRARY GOES INTO PRODUCTION.
import numpy

Mean_Line_Data = namedtuple( 'Mean_Line_Data', [ 'm', 'k1' ] )


class NACA_Base( abc.ABC ):
	"""
	[summary]

	Raises:
		 NotImplementedError: [description]
		 NotImplementedError: [description]

	Returns:
		 [type] -- [description]
	"""

	def __init__( self, naca_number, num_points = 200, cosine_spacing = True ):
		self._naca_number = int( naca_number )
		assert 0 <= self._naca_number <= 99999

		self._x_points = self._cosspace( 0, 1, num_points ) if cosine_spacing else numpy.linspace( 0, 1, num_points )


	@property
	def mean_camber_line( self ):
		'''Getter for the points that define the mean camber line of the airfoil this class represents.'''
		return self._mean_camber_line( )

	@property
	def naca_number( self ):
		''' '''
		return self._naca_number

	@property
	def points( self ):
		'''Getter for the points that define the airfoil this class represents.'''
		return self._calculate_points( )

	@property
	def x_points( self ):
		'''Getter for the x axis points calculated along the mean camber line.'''
		return self._x_points

	@staticmethod
	def _cosspace( start, stop, max_points ):
		"""
		[summary]

		Arguments:
			 stop {[type]} -- [description]
			 max_points {[type]} -- [description]

		Returns:
			 [type] -- [description]
		"""

		vals = [ numpy.pi * 0.5 * x for x in numpy.linspace( start, stop, max_points ) ]
		cosspace_vals = numpy.array( [ 1 - x for x in numpy.cos( vals ) ] )

		return cosspace_vals


	@abc.abstractmethod
	def _calculate_points( self ):
		"""
		[summary]

		Raises:
			 NotImplementedError: [description]
		"""

		pass


	@abc.abstractmethod
	def _mean_camber_line( self ):
		"""
		[summary]

		Raises:
			 NotImplementedError: [description]
		"""

		pass



class NACA_4( NACA_Base ):
	"""
	https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil (has 4, 5, 6, 7, and 8 series information.)
	http://airfoiltools.com/airfoil/naca4digit

	Arguments:
		 NACA_Base {[type]} -- [description]

	Returns:
		 [type] -- [description]
	"""

	def __init__( self, naca_number, num_points = 200, cosine_spacing = True ):
		super( ).__init__( naca_number, num_points = num_points, cosine_spacing = cosine_spacing )

		self._cl = 1.0
		self._p = ( self._naca_number % 1e3 - self._naca_number % 1e2 ) / 1e3
		self._t = self._naca_number % 1e2 / 1e2
		self._m = ( self._naca_number - self._naca_number % 1e3 ) / 1e5
		self._x_over_c = self._x_points / self._cl


	def _mean_camber_line( self ):
		"""
		[summary]

		Returns:
			 [type] -- [description]
		"""

		return numpy.where( ( self._x_points >= 0 ) & ( self._x_points <= self._cl * self._p ),
									 self._m * ( self._x_points / numpy.power( self._p, 2 ) ) * ( 2.0 * self._p - self._x_over_c ),
									 self._m * ( ( self._cl - self._x_points ) / numpy.power( 1 - self._p, 2 ) ) * ( 1.0 + self._x_over_c - 2.0 * self._p ) )


	def _calculate_points( self ):
		"""
		[summary]

		Returns:
			 [type] -- [description]
		"""

		dyc_dx = self._dyc_over_dx( )
		th = numpy.arctan( dyc_dx )

		yt = self._thickness( )
		yc = self._mean_camber_line( )

		x_pos = ( self._x_points - yt * numpy.sin( th ), yc + yt * numpy.cos( th ) )
		y_pos = ( self._x_points + yt * numpy.sin( th ), yc - yt * numpy.cos( th ) )
		return ( x_pos, y_pos )


	def _dyc_over_dx( self ):
		"""
		[summary]

		Returns:
			 [type] -- [description]
		"""

		return numpy.where( ( self._x_points >= 0 ) & ( self._x_points <= self._cl * self._p ),
									 2.0 * self._m / numpy.power( self._p, 2 ) * ( self._p - self._x_over_c ),
									 2.0 * self._m / numpy.power( 1 - self._p, 2 ) * ( self._p - self._x_over_c ) )


	def _thickness( self ):
		"""
		[summary]

		Returns:
			 [type] -- [description]
		"""

		term1 = 0.2969 * numpy.sqrt( self._x_over_c )
		term2 = -0.1260 * self._x_over_c
		term3 = -0.3516 * numpy.power( self._x_over_c, 2 )
		term4 = 0.2843 * numpy.power( self._x_over_c, 3 )
		term5 = -0.1015 * numpy.power( self._x_over_c, 4 )
		return 5 * self._t * self._cl * ( term1 + term2 + term3 + term4 + term5 )



class NACA_5( NACA_Base ):
	"""
	(From Wikipedia)
	The NACA five-digit series describes more complex airfoil shapes. Its format is: LPSTT, where:

	L: a single digit representing the theoretical optimum lift coefficient at ideal angle-of-attack CLI = 0.15*L (this is not the same as
	the lift coefficient, CL)
	P: a single digit for the x-coordinate of the point of maximum camber (max camber at x = 0.05*P)
	S: a single digit indicating whether the camber is simple (S=0) or reflex (S=1)
	TT: the maximum thickness in percent of chord, as in a four-digit NACA airfoil code
	For example, the NACA 23112 profile describes an airfoil with design lift coefficient of 0.3 (0.15*2), the point of maximum camber
	located at 15% chord (5*3), reflex camber (1), and maximum thickness of 12% of chord length (12).

	https://en.wikipedia.org/wiki/NACA_airfoil#Five-digit_series
	http://airfoiltools.com/airfoil/naca5digit

	Arguments:
		 NACA_Base {[type]} -- [description]

	Returns:
		 [type] -- [description]
	"""

	def __init__( self, naca_number, num_points = 200, cosine_spacing = True ):
		super( ).__init__( naca_number, num_points = num_points, cosine_spacing = cosine_spacing )

		self._mean_line_map = { 0.05 : Mean_Line_Data( m = 0.0580, k1 = 361.400 ),
										0.10 : Mean_Line_Data( m = 0.1260, k1 = 51.640 ),
										0.15 : Mean_Line_Data( m = 0.2025, k1 = 15.957 ),
										0.20 : Mean_Line_Data( m = 0.2900, k1 = 6.643 ),
										0.25 : Mean_Line_Data( m = 0.3910, k1 = 3.230 ), }

		# LPSTT
		# NACA 23112 profile describes an airfoil with design lift coefficient of 0.3 (0.15*2), the point of maximum camber located at 15% chord (5*3), reflex camber (1), and maximum thickness of 12% of chord length (12).

		# coeficient of lift
		self._cl = int( str( naca_number )[ 0 ] ) * 3 / 2 / 10

		# point of maximum camber
		self._p = float( '%.2f' % ( int( str( naca_number ) [ 1 : 3 ] ) / 2 / 100 ) )

		# maximum thickness as percentage along chord length
		self._t = int( str( naca_number ) [ 3 : 5 ] )

		self._m, self._k1 = self._mean_line_map.get( self._p )


	def _calculate_points( self ):
		'''
		'''

		pairs = [ ]

		for x in self._x_points:
			if x >= 0 and x <= self._m:
				yc = self._k1 / 6 * ( numpy.power( x, 3 ) - ( 3 * self._m * numpy.power( x, 2 ) ) + ( numpy.power( self._m, 2 ) * ( 3 - self._m ) * x ) )

			else:
				yc = self._k1 * numpy.power( self._m, 3 ) / 6 * ( 1 - x )

			pairs.append( ( x, yc ) )

		return pairs



if __name__ == '__main__':
	naca_4 = NACA_4( '0018' )
	for point in naca_4.points:
		matplotlib.pyplot.plot( point[ 0 ], point[ 1 ], 'b' )

	matplotlib.pyplot.plot( naca_4.x_points, naca_4.mean_camber_line, 'r' )
	matplotlib.pyplot.axis( 'equal' )
	matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
	matplotlib.pyplot.show( )


	# naca_5 = NACA_5( 23112 )
	# for point in naca_5.points:
	# 	print( point )
	# 	matplotlib.pyplot.plot( point[ 0 ], point[ 1 ], 'b' )

	# matplotlib.pyplot.axis( 'equal' )
	# matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
	# matplotlib.pyplot.show( )
