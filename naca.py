'''
https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil
'''

import numpy


class NACA_4( ):
	'''
	TODO: Should the class create the points at init or on demand? Maybe a generator?
	'''

	def __init__( self, naca_number, num_points ):
		self._naca_number = int( naca_number )
		assert 0 <= self._naca_number <= 9999

		self._m = ( self._naca_number - self._naca_number % 1e3 ) / 1e5
		self._p = ( self._naca_number % 1e3 - self._naca_number % 1e2 ) / 1e3
		self._t = self._naca_number % 1e2 / 1e2
		self._c = 1.0
		self._x = numpy.linspace( 0, 1, num_points )


	@property
	def camber_line( self ):
		'''Getter for the points that define the mean camber line of the airfoil this class represents.'''
		return self._camber_line( )

	@property
	def points( self ):
		'''Getter for the points that define the airfoil this class represents.'''
		return self._calculate_points( )

	@property
	def x( self ):
		'''TODO: This needs a more descriptive/verbose name.'''
		return self._x


	def _camber_line( self ):
		'''
		'''

		return numpy.where( ( self._x >= 0 ) & ( self._x <= self._c * self._p ),
								  self._m * ( self._x / numpy.power( self._p, 2 ) ) * ( 2.0 * self._p - ( self._x / self._c ) ),
								  self._m * ( ( self._c - self._x ) / numpy.power( 1 - self._p, 2 ) ) * ( 1.0 + ( self._x / self._c ) - 2.0 * self._p ) )

	def _dyc_over_dx( self ):
		'''
		'''

		return numpy.where( ( self._x >= 0 ) & ( self._x <= self._c * self._p ),
								  2.0 * self._m / numpy.power( self._p, 2 ) * ( self._p - self._x / self._c ),
								  2.0 * self._m / numpy.power( 1 - self._p, 2 ) * ( self._p - self._x / self._c ) )

	def _thickness( self ):
		'''
		'''

		term1 =  0.2969 * numpy.sqrt( self._x / self._c )
		term2 = -0.1260 * self._x / self._c
		term3 = -0.3516 * numpy.power( self._x / self._c, 2 )
		term4 =  0.2843 * numpy.power( self._x / self._c, 3 )
		term5 = -0.1015 * numpy.power( self._x / self._c, 4 )
		return 5 * self._t * self._c * ( term1 + term2 + term3 + term4 + term5 )


	def _calculate_points( self ):
		'''
		TODO: Should this be a generator?
		'''

		dyc_dx = self._dyc_over_dx( )
		th = numpy.arctan( dyc_dx )
		yt = self._thickness( )
		yc = self._camber_line( )

		x_pos = ( self._x - yt * numpy.sin( th ), yc + yt * numpy.cos( th ) )
		y_pos = ( self._x + yt * numpy.sin( th ), yc - yt * numpy.cos( th ) )
		return ( x_pos, y_pos )



if __name__ == '__main__':
	naca_4 = NACA_4( "0018", 200 )

	'''
	TESTING PLOT
	Yes, it is bad form putting an import here instead of at the top of the file.
	matplotlib should only be imported if this module is used as a library, not as a self-running script.
	'''

	import matplotlib.pyplot	
	for item in naca_4.points:
		matplotlib.pyplot.plot( item[ 0 ], item[ 1 ], 'b' )

	matplotlib.pyplot.plot( naca_4.x, naca_4.camber_line, 'r' )
	matplotlib.pyplot.axis( 'equal' )
	matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
	matplotlib.pyplot.show( )
