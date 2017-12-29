(
	struct Cross_Section (
		position = ( Point3 0 0 0 ),
		naca_number = "0000",
		chord_length = 0.0,
		max_points = 0,
		equal_spacing = False,
		sharp_trailing_edge = True,
		edge_coefficient = 0,
		spar_position = ( Point3 0 0 0 ),
		points = #( ),
		
		
		private
		fn _calculate_spar_position = (
			for i = 1 to this.points.count do (
				if this.points[ i ].z > this.spar_position.z then this.spar_position = this.points[ i ]
			)
		),
		
		
		fn _linspace start stop = (
			stop -= start
			
			lin_points = #( )

			step = stop / ( this.max_points - 1 as float )

			for i = 0 to this.max_points - 1 do (
				append lin_points ( start + ( i * step ) )
			)

			return lin_points
		),
		
		
		fn _cosspace start stop = (
			-- Actually half cosine. Packs more verts at leading ege.
			
			cos_points = #( )
			beta = this._linspace 0 stop
			
			for b in beta do (
				append cos_points ( 1 - ( cos ( pi * 0.5 * ( radToDeg b ) ) ) )
			)
						
			return cos_points
		),
		
		
		fn _naca_four max_camber_pos max_camber y_pos unused:unsupplied upper:True = (
			if y_pos <= max_camber_pos then (
				z_camber = max_camber * y_pos / max_camber_pos^2 * ( 2 * max_camber_pos - y_pos )
				theta = atan 2 * max_camber / max_camber_pos^2 * ( max_camber_pos - y_pos )
			) else (
				z_camber = max_camber * ( 1 - y_pos ) / ( 1 - max_camber_pos )^2 * ( 1 + y_pos - 2 * max_camber_pos )
				theta = atan max_camber / ( 1 -  max_camber_pos )^2 * ( 2 * max_camber_pos - 2 * y_pos )
			)
			
			return #( theta, z_camber )
		),

		
		fn _naca_five r k1 y_pos k2k1:unsupplied upper:True = (
			if y_pos <= r then (
				if k2k1 == undefined then (
					z_camber = k1 / 6 * ( y_pos^3 - 3 * r * y_pos^2 + r^2 * ( 3 - r ) * y_pos )
					theta = atan k1 / 6 * ( 3 * y_pos^2 - 6 * r * y_pos + r^2 * ( 3 - r ) )
				) else (
					z_camber = k1 / 6 * ( ( y_pos - r )^3 - k2k1 * ( 1 - r )^3 * y_pos - r^3 * y_pos + r^3 )
					theta = atan k1 / 6 * ( 3 * ( y_pos - r )^2 - k2k1 * ( 1 - r )^3 - r^3 )
				)
			) else (
				if k2k1 == undefined then (
					z_camber = k1 * r^3 / 6 * ( 1 - y_pos )
					theta = atan -(k1 * r^3 / 6 )
				) else (
					z_camber = k1 / 6 * ( k2k1 * ( y_pos - r )^3 - k2k1 * ( 1 - r )^3 * y_pos - r^3 * y_pos + r^3 )
					theta = atan k1 / 6 * ( 3 * k2k1 * ( y_pos - r )^2 - k2k1 * ( 1 - r )^3 - r^3 )
				)
			)

			return #( theta, z_camber )
		),
		
		
		fn _thickness_at_pos thickness y_pos = (
			y_thick = thickness * 5 * ( ( 0.2969 * sqrt y_pos ) + ( ( ( ( -this.edge_coefficient * y_pos + 0.2843 ) * y_pos - 0.3516 ) * y_pos ) - 0.126 ) * y_pos )
			return y_thick
		),
		

		public
		fn align_cross_section_to_spar root_spar_position = (
			y_offset = root_spar_position.y - this.spar_position.y
			
			for i = 1 to this.points.count do (
				this.points[ i ].y += y_offset
			)
		),
		
		
		fn get_points = (
			return this.points
		),


		fn init = ( 
			if this.max_points < 2 then this.max_points = 2 -- Can't add less than 2 knots to a spline shape.
			if this.sharp_trailing_edge == True then this.edge_coefficient = 0.1036 else this.edge_coefficient = 0.1015
			if this.equal_spacing == True then spacing_fn = this._linspace else spacing_fn = this._cosspace
			naca_digits = this.naca_number as integer
			thickness = mod naca_digits 100
			k2k1 = undefined

			case this.naca_number.count of (
				4	: (
							naca_fn = this._naca_four
							
							max_camber_pos = mod naca_digits 1000 - thickness
							max_camber = ( mod naca_digits 10000 - max_camber_pos - thickness ) / 1e5
							max_camber_pos /= 1e3

							arg1 = max_camber_pos
							arg2 = max_camber
						)		
				5 	: (
							naca_fn = this._naca_five
		
							thickness = mod naca_digits 100
							max_camber_pos = mod naca_digits 10000 - thickness

							identifier = ( naca_digits / 100 ) as integer
							case identifier of (
								-- standards
								210	: (
											r = 0.0580
											k1 = 361.400
										  )
								220	: (
											r = 0.1260
											k1 = 51.640
										  )
								221	: (
											r = 0.1300
											k1 = 51.990
											k2k1 = 0.000764
										  )
								230	: (
											r = 0.2025
											k1 = 15.957
										  )
								231	: (
											r = 0.2170
											k1 = 15.793
											k2k1 = 0.00677
										  )
								240	: (
											r = 0.2900
											k1 = 6.643
										  )
								241	: (
											r = 0.3180
											k1 = 6.520
											k2k1 = 0.303
										  )
								250	: (
											r = 0.3910
											k1 = 3.230
										  )
								251	: (
											r = 0.4410
											k1 = 3.191
											k2k1 = 0.1355
										  )
							)

							arg1 = r
							arg2 = k1							
						)
			)

			thickness /= 1e2
			y_points = spacing_fn 0 1
			new_points = #( this.position )
			
			-- Upper surface
			for y_pos in y_points do (
				point_info = naca_fn arg1 arg2 y_pos k2k1:k2k1 upper:True -- theta, z_camber
				y_thick = this._thickness_at_pos thickness y_pos
				y_pos = ( y_pos + y_thick * sin point_info[ 1 ] ) * this.chord_length
				z_pos = ( point_info[ 2 ] + y_thick * cos point_info[ 1 ] ) * this.chord_length
				
				new_point = ( Point3 this.position[ 1 ] ( this.position[ 2 ] + y_pos ) ( this.position[ 3 ] + z_pos ) )
				append new_points new_point
			)

			-- Lower surface
			y_points = for i = ( y_points.count - 1 ) to 1 by -1 collect y_points[ i ]
			for y_pos in y_points do (
				point_info = naca_fn arg1 arg2 y_pos k2k1:k2k1 upper:False -- theta, z_camber
				y_thick = this._thickness_at_pos thickness y_pos
				y_pos = ( y_pos + y_thick * sin point_info[ 1 ] ) * this.chord_length
				z_pos = ( point_info[ 2 ] - y_thick * cos point_info[ 1 ] ) * this.chord_length
				
				new_point = ( Point3 this.position[ 1 ] ( this.position[ 2 ] + y_pos ) ( this.position[ 3 ] + z_pos ) )
				append new_points new_point
			)

			-- The first two knots back from the exact leading edge have such infinitesimally small values that Max can't resolve them.
			if equal_spacing == False then (
				deleteItem new_points 2
				deleteItem new_points new_points.count
			)

			this.points = new_points
			this._calculate_spar_position()
		)
	)
		
	
	
	fn linspace start stop max_points end_point:True = (
		stop -= start
		
		points = #( )

		if end_point == True then step_div = max_points - 1 as float else step_div = max_points as float
		step = stop / step_div

		for i = 0 to max_points - 1 do (
			append points ( start + ( i * step ) )
		)

		return points
	)
		
		
	fn create_wing root_pos root_naca_number root_chord tip_naca_number tip_chord wing_length num_points num_cross_sections incidence_angle:0 dihedral_angle:0 sweep_angle:0 = (
		tip_pos = ( point3 ( root_pos.x + wing_length ) root_pos.y root_pos.z )				
		airfoil_x_locations = linspace root_pos.x tip_pos.x num_cross_sections end_point:True
		chord_lengths = linspace tip_chord root_chord num_cross_sections end_point:True
		chord_lengths = for i = chord_lengths.count to 1 by -1 collect chord_lengths[ i ] -- Have to revese it since the spacing went from tip -> root.
		
		-- Now make a collection of structs, 1 for each cross section.
		cross_sections = #( )
		
		for i = 1 to airfoil_x_locations.count do (
			x = airfoil_x_locations[ i ]
			airfoil_pos = ( Point3 x root_pos.y root_pos.z )
			
			if i < airfoil_x_locations.count then (
				naca_number = root_naca_number
			) else (
				naca_number = tip_naca_number
			)
			
			cs = Cross_Section position:airfoil_pos naca_number:naca_number chord_length:chord_lengths[ i ] max_points:num_points equal_spacing:False sharp_trailing_edge:True
			cs.init()
			
			append cross_sections cs
		)
		
		wing = editable_mesh name:( uniquename "Wing" )
		convertTo wing Editable_Poly
		
		-- Align each cross section to a standard spar location and make verts		
		for cs in cross_sections do (
			cs.align_cross_section_to_spar cross_sections[ 1 ].spar_position
			
			for p in cs.get_points() do (
				polyOp.createVert wing p
			)
		)
		
		-- Create faces from verts (ccw winding order)
		num_verts_per_cross_section = wing.verts.count / cross_sections.count
		
		for i = 0 to cross_sections.count - 2 do (
			for j = 1 to num_verts_per_cross_section - 1 do (
				ll = j + ( i * num_verts_per_cross_section )
				lr = ll + num_verts_per_cross_section
				ur = lr + 1
				ul = ll + 1
				
				polyOp.createPolygon wing #( ll, lr, ur, ul )
			)
			
			-- Special case to wrap around to starting vert # on each cross section in order to get the last polygon strip on the wing.
			ll = ( i + 1 ) * num_verts_per_cross_section
			lr = ll + ( num_verts_per_cross_section )
			ur = ll + 1
			ul = ll - num_verts_per_cross_section + 1
			
			polyOp.createPolygon wing #( ll, lr, ur, ul )
		)
		
		-- Rotate for dihedral angle
		rot_obj = eulerAngles -incidence_angle -dihedral_angle 0 --sweep_angle
		rotate wing rot_obj
	)
	
	
	-- MAIN
	create_wing ( point3 0 0 0 ) "0018" 228 "0010" 106.7 622.6899996 25 2 incidence_angle:3.5 dihedral_angle:4.5 sweep_angle:8.25	
	/* BOEING B-17G
		ROOT NACA 0018
		ROOT CHORD 228
		TIP NACA 0010
		TIP CHORD 106.7
		LENGTH (1/2 wingspan ) 622.689996
		INCIDENCE ANGLE 3.5deg
		DIHEDRAL ANGLE 4.5deg
		WING SWEEP ANGLE 8.25deg
	*/

	create_wing ( point3 0 0 0 ) "23016" 117 "4412" 36 312 25 2 incidence_ang1e:2 dihedral_angle:5.66
	/* LOCKHEED P-38J
		ROOT NACA 23016
		ROOT CHORD 17
		TIP NACA 4412
		TIP CHORD 36
		LENGTH (1/2 wingspan ) 312
		INCIDENCE ANGLE 2deg
		DIHEDRAL ANGLE 5.66deg
	*/
	
	create_wing ( point3 24 0 0 ) "2412" 64 "2412" 44.5 191 25 2 incidence_angle:1.5 dihedral_angle:1.733
	/* CESSNA 172
	   ROOT NACA 2412
	   ROOT CHORD 64
	   TIP NACA 2412
	   TIP CHORD 44.5
	   LENGTH( 1/2 WINGSPAN ) 191
	   INCIDENCE ANGLE AT ROOT 1.5DEG
	   INCIDENCE ANGLE AT TIP -1.5DEG
	   DIHEDRAL ANGLE 1.7333DEG
   */
   
	-- NACA 2412 from airfoiltools.com/airfoil/naca4digit
	-- NACA 24012 from airfoiltools.com/airfoil/naca5digit
	-- NACA 24112 from airfoiltools.com/airfoil/naca5digit
)