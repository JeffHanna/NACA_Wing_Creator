'''
https://en.wikipedia.org/wiki/NACA_airfoil#Equation_for_a_cambered_4-digit_NACA_airfoil
'''

#import math
import matplotlib.pyplot
import numpy


class NACA_4( ):
	'''
	Testing NACA number = 2412
	'''

	def __init__( naca_number, num_points ):
		self._naca_number = int( naca_number )
		assert 0 <= self._naca_number <= 9999

		self._m = 0.02
		self._p = 0.4
		self._t = 0.12
		self._cc = 1.0

		self._x = numpy.linspace( 0, 1, num_points )

		
	def camber_line( x, m, p, c ):
		'''
		'''

		return numpy.where( ( x >= 0 ) & ( x <= c * p ),
								m * ( x / numpy.power( p, 2 ) ) * ( 2.0 * p - ( x / c ) ),
								m * ( ( c - x ) / numpy.power( 1 - p, 2 ) ) * ( 1.0 + ( x / c ) - 2.0 * p ) )

	def dyc_over_dx( x, m, p, c ):
		'''
		'''

		return numpy.where( ( x >= 0 ) & ( x <= c * p ),
								2.0 * m / numpy.power( p, 2 ) * ( p - x / c ),
								2.0 * m / numpy.power( 1 - p, 2 ) * ( p - x / c ) )

	def thickness( x, t, c ):
		'''
		'''

		term1 =  0.2969 * numpy.sqrt( x / c )
		term2 = -0.1260 * x / c
		term3 = -0.3516 * numpy.power( x / c, 2 )
		term4 =  0.2843 * numpy.power( x / c, 3 )
		term5 = -0.1015 * numpy.power( x / c, 4 )
		return 5 * t * c * ( term1 + term2 + term3 + term4 + term5 )

	def calculate_points( x, m, p, t, c = 1 ):
		'''
		'''

		dyc_dx = dyc_over_dx( x, m, p, c )
		th = numpy.arctan( dyc_dx )
		yt = thickness( x, t, c )
		yc = camber_line( x, m, p, c )
		return ( ( x - yt * numpy.sin( th ), yc + yt * numpy.cos( th ) ),
		( x + yt * numpy.sin( th ), yc - yt * numpy.cos( th ) ) )


	def plot airfoil( self ):
		for item in self.calculate_points( x, m, p, t, c ):
			matplotlib.pyplot.plot( item[ 0 ], item[ 1 ], 'b' )

		matplotlib.pyplot.plot( x, camber_line( x, m, p, c ), 'r' )
		matplotlib.pyplot.axis( 'equal' )
		matplotlib.pyplot.xlim( ( -0.05, 1.05 ) )
		matplotlib.pyplot.show( )


if __name__ == '__main__':
	#naca2412 
	

	naca_4 = NACA_4( "0018", 200 )

	# half-cosine spacing.
	#x = numpy.array( [ 1 - ( numpy.cos( math.pi * 0.5 * math.degrees( x ) ) ) for x in x ] )

	
