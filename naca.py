"""
[summary]
"""

import abc
from collections import namedtuple
import math
import matplotlib.pyplot # FOR TESTING ONLY. TO BE REMOVED WHEN THIS LIBRARY GOES INTO PRODUCTION.
import numpy

Mean_Line_Data = namedtuple( 'Mean_Line_Data', [ 'm', 'k1' ] )


class NACA_Base( abc.ABC ):
	"""
	[summary]

	Arguments:
		naca_number {str} -- [description]

	Keyword Arguments:
		num_points {int} -- [description]
		cosine_spacing {bool} -- [description]
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
		'''Getter for the NACA number being used as the input to this class.'''
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
		"""


	@abc.abstractmethod
	def _mean_camber_line( self ):
		"""
		[summary]
		"""



class NACA_4( NACA_Base ):
	"""
	https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil (has 4, 5, 6, 7, and 8 series information.)
	http://airfoiltools.com/airfoil/naca4digit

	Arguments:
		naca_number {str} -- [description]

	Keyword Arguments:
		num_points {int} -- [description]
		cosine_spacing {bool} -- [description]
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

		return( x_pos, y_pos )


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
		naca_number {str} -- [description]

	Keyword Arguments:
		num_points {int} -- [description]
		cosine_spacing {bool} -- [description]
	"""

	def __init__( self, naca_number, num_points = 200, cosine_spacing = True ):
		super( ).__init__( naca_number, num_points = num_points, cosine_spacing = cosine_spacing )

		self._mean_line_map = { 0.05 : Mean_Line_Data( m = 0.0580, k1 = 361.400 ),
										0.10 : Mean_Line_Data( m = 0.1260, k1 = 51.640 ),
										0.155 : Mean_Line_Data( m = 0.2025, k1 = 15.957 ),
										0.20 : Mean_Line_Data( m = 0.2900, k1 = 6.643 ),
										0.25 : Mean_Line_Data( m = 0.3910, k1 = 3.230 ), }

		self._a = ( 0.2969, -0.1260, -0.3516, 0.2843, -0.1036 )

		# LPSTT
		# NACA 23112 profile describes an airfoil with design lift coefficient of 0.3 (0.15*2), the point of maximum camber located at 15% chord (5*3)
		# reflex camber (1), and maximum thickness of 12% of chord length (12).

		# coeficient of lift
		self._cl = int( str( naca_number )[ 0 ] ) * 3.0 / 2.0 / 10.0 # 0.3

		# point of maximum camber
		self._p = float( '%.3f' % ( int( str( naca_number ) [ 1 : 3 ] ) / 2.0 / 100.0 ) ) #.155

		# maximum thickness as percentage along chord length
		self._t = int( str( naca_number ) [ 3 : 5 ] ) / 100.0 # 0.12

		self._m, self._k1 = self._mean_line_map.get( self._p ) #.2025, 15.957


	def _calculate_points( self ):
		'''
		'''

		yt = [ 5 * self._t * ( self._a[ 0 ] * math.sqrt( x ) + self._a[ 1 ] * x +self._a[ 2 ] * math.pow( x, 2 ) + self._a[ 3 ] * math.pow( x, 3 ) + self._a[ 4 ] * pow( x, 4 ) ) for x in self._x_points ]

		xc1 = [x for x in self._x_points if x <= self._p]
		xc2 = [x for x in self._x_points if x > self._p]
		xc = xc1 + xc2

		if self._p == 0:
			xu = self._x_points
			yu = yt

			xl = self._x_points
			yl = [ -x for x in yt ]

			zc = [ 0 ] * len( xc )
		else:
			yc1 = [ self._k1 / 6.0 * ( math.pow( x, 3) - 3 * self._m * math.pow( x, 2 ) + math.pow( self._m, 2 ) * ( 3 - self._m ) * x ) for x in xc1 ]
			yc2 = [ self._k1 / 6.0 * math.pow( self._m, 3 ) * ( 1 - x ) for x in xc2 ]
			zc  = [ self._cl / 0.3 * x for x in yc1 + yc2 ]

			dyc1_dx = [ self._cl / 0.3 * ( 1.0 / 6.0 ) * self._k1 * ( 3 * math.pow( x, 2 ) - 6 * self._m * x + math.pow( self._m, 2) * ( 3 - self._m ) ) for x in xc1 ]
			dyc2_dx = [ self._cl / 0.3 * ( 1.0 / 6.0 ) * self._k1 * math.pow( self._m, 3 ) ] *len( xc2 )

			dyc_dx = dyc1_dx + dyc2_dx
			th = [ numpy.arctan( x ) for x in dyc_dx ]

			xu = [ x - y * numpy.sin( z ) for x, y, z in zip( self._x_points, yt, th ) ]
			yu = [ x + y * numpy.cos( z ) for x, y, z in zip( zc, yt, th ) ]

			xl = [ x + y * numpy.sin( z ) for x, y, z in zip( self._x_points, yt, th ) ]
			yl = [ x - y * numpy.cos( z ) for x, y, z in zip( zc, yt, th ) ]


		X = xu[ ::-1 ] + xl[ 1: ]
		Z = yu[ ::-1 ] + yl[ 1: ]

		return X, Z


	def _mean_camber_line( self ):
		pass



if __name__ == '__main__':
	naca_4 = NACA_4( '0018' )
	for point in naca_4.points:
		matplotlib.pyplot.plot( point[ 0 ], point[ 1 ], 'b' )

	matplotlib.pyplot.plot( naca_4.x_points, naca_4.mean_camber_line, 'r' )
	matplotlib.pyplot.axis( 'equal' )
	matplotlib.pyplot.grid( True )
	matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
	matplotlib.pyplot.show( )


	naca_5 = NACA_5( 23112, cosine_spacing = False )
	matplotlib.pyplot.plot( naca_5.points[ 0 ], naca_5.points[ 1 ], 'b' )
	#matplotlib.pyplot.plot( naca_5.x_points, naca_5.mean_camber_line, 'r' )

	matplotlib.pyplot.axis( 'equal' )
	matplotlib.pyplot.grid( True )
	matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
	matplotlib.pyplot.show( )
