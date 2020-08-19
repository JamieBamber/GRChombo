/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#if !defined(Y00INTEGRATION_HPP_)
#error "This file should only be included through Y00Integration.hpp"
#endif

#ifndef Y00INTEGRATION_IMPL_HPP_
#define Y00INTEGRATION_IMPL_HPP_

//! Set up and execute the interpolation query
inline void Y00Integration::execute_query(
    AMRInterpolator<Lagrange<4>> *a_interpolator) const
{
    CH_TIME("Y00Integration::execute_query");
    if (a_interpolator == nullptr)
    {
        MayDay::Error("Interpolator has not been initialised in GRAMR class.");
    }

    std::vector<double> interp_val(m_num_points * m_params.num_integration_radii);
    std::vector<double> interp_x(m_num_points * m_params.num_integration_radii);
    std::vector<double> interp_y(m_num_points * m_params.num_integration_radii);
    std::vector<double> interp_z(m_num_points * m_params.num_integration_radii);

    double a = m_params.bh_a;
    // Work out the coordinates
    for (int iradius = 0; iradius < m_params.num_integration_radii; ++iradius)
    {
        for (int idx = 0; idx < m_num_points; ++idx)
        {
            int itheta = idx / m_params.num_points_phi;
            int iphi = idx % m_params.num_points_phi;
            // don't put a point at z = 0
            double theta = m_params.theta_min + (itheta + 0.5) * m_dtheta;
            double phi = iphi * m_dphi;
	    double r = m_params.integration_radii[iradius];
            interp_x[iradius * m_num_points + idx] =
                m_params.integration_center[0] + sin(theta) * (r * cos(phi) + a * sin(phi));
            interp_y[iradius * m_num_points + idx] =
                m_params.integration_center[1] + sin(theta) * (r * sin(phi) - a * cos(phi));
            interp_z[iradius * m_num_points + idx] =
                m_params.integration_center[2] + r * cos(theta);
        }
    }
    for (int ivar = 0; ivar < m_params.num_vars; ++ivar)
    {
	int var = m_params.var_indices[ivar];
    	// set up the query
    	InterpolationQuery query(m_num_points * m_params.num_integration_radii);
    	query.setCoords(0, interp_x.data())
        	.setCoords(1, interp_y.data())
        	.setCoords(2, interp_z.data())
        	.addComp(var, interp_val.data());
	
    	// submit the query
    	a_interpolator->interp(query);
    	auto integral = integrate_surface(interp_val);
	
    	// linear or log label
    	std::string log_label;
    	if (m_params.linear_or_log){
        	log_label = "_linear_";
    	}
    	else {
        	log_label = "_log_";
    	}
	
    	// number label 
    	std::ostringstream nlabel;
    	nlabel << std::setw(6) << std::setfill('0') << m_start_number;
    	std::string nstring = "n" + nlabel.str();

    	std::string integral_filename = m_params.output_rootdir + m_data_subdir + "_" + UserVariables::variable_names[var] + log_label + nstring + 
    	m_params.suffix;
	
    	write_integral(integral, integral_filename);
	
    	if (m_params.write_extraction)
    	{
        	write_extraction("ExtractionOut_", var, interp_val);
    	}
   }
}

//! integrate over a spherical shell with given harmonics for each integration
//! radius and normalise by multiplying by radius
inline std::vector<double>
Y00Integration::integrate_surface(const std::vector<double> a_re_part) const
{
    CH_TIME("Y00Integration::integrate_surface");
    int rank;
    #ifdef CH_MPI
    	MPI_Comm_rank(Chombo_MPI::comm, &rank);
    #else
    	rank = 0;
    #endif
    std::vector<double> integral(m_params.num_integration_radii, 0.);

    const int num_phi_points = m_params.num_points_phi;
    // only rank 0 does the integral, but use OMP threads if available
    if (rank == 0)
    {
        // integrate the values over the sphere (normalised by r^2)
        // for each radius
        // assumes spacings constant, uses trapezium rule for phi and rectangles
        // for theta  note we don't have to fudge the end points for phi because
        // the function is periodic  and so the last point (implied but not part
        // of vector) is equal to the first point
	#ifdef _OPENMP
		#if __GNUC__ > 8
			#define OPENMP_CONST_SHARED shared(a_re_part)
		#else
			#define OPENMP_CONST_SHARED
		#endif
		#pragma omp parallel for collapse(1) default(none)                             \
    				shared(integral) OPENMP_CONST_SHARED
		#undef OPENMP_CONST_SHARED
	#endif
	for (int iradius = 0; iradius < m_params.num_integration_radii;
     	iradius++)
        {
	    double a = m_params.bh_a;
	    double r = m_params.integration_radii[iradius];
	    for (int iphi = 0; iphi < m_params.num_points_phi; ++iphi)
            {
                double phi = iphi * 2 * M_PI / m_params.num_points_phi;
                double inner_integral_re = 0.;
                for (int itheta = 0; itheta < m_params.num_points_theta;
                     itheta++)
                {
	            double theta = m_params.theta_min + (itheta + 0.5) * m_dtheta;
                    int idx = iradius * m_num_points +
                              itheta * m_params.num_points_phi + iphi;
                    double integrand_re = a_re_part[idx];
		    // factor of dOmega
		    double dS = sqrt((1 + (a/r)*(a/r))*(1 + pow(a*cos(theta)/r,2))) * sin(theta) * r * r;
                    // double dS = sin(theta)*r*r;
		    double f_theta_phi_re = integrand_re * dS;
		    // account for the half box by multiplying by 2 here and divide through by theta range
                    inner_integral_re += m_dtheta * f_theta_phi_re / ((m_params.theta_max - m_params.theta_min) * 0.5);
		}
		#ifdef _OPENMP
			#pragma omp atomic
		#endif
       	        integral[iradius] += m_dphi * inner_integral_re;
		//! inner_re = Sum [ r * Re{a_[idx]} * dphi * sin(theta) * dtheta ]
            }
        }
    }
    return integral;
}

//! Write out calculated value of integral for each integration radius
inline void
Y00Integration::write_integral(const std::vector<double> a_integral,
                               std::string a_filename) const
{
    CH_TIME("Y00Integration::write_integral");
    // open file for writing
    SmallDataIO integral_file(a_filename, m_dt, m_time, m_restart_time,
                              SmallDataIO::APPEND, m_first_step);

    pout() << "attempting to write integral" << std::endl;
    // remove any duplicate data if this is a restart
    integral_file.remove_duplicate_time_data();

    // need to write headers if this is the first timestep
    if (m_first_step)
    {
	pout() << "making headers ... " << std::endl;
        // make header strings
        std::vector<std::string> headers = {"r = ..."};
	integral_file.write_header_line(headers, "t");

	// write out radii
	integral_file.write_data_line(m_params.integration_radii, 0);
    }

    // make vector of data for writing
    std::vector<double> data_for_writing(m_params.num_integration_radii);
    for (int iintegral = 0; iintegral < m_params.num_integration_radii;
         iintegral += 1)
    {
        int iradius = iintegral;
        data_for_writing[iintegral] = a_integral[iradius];
    }

    // write data
    pout() << "writing data ... " << std::endl;
    integral_file.write_time_data_line(data_for_writing);
}

//! Write out the result of the integration in phi and theta at each timestep for
//! each integration radius
inline void
Y00Integration::write_extraction(std::string a_file_prefix, int var,
                                 const std::vector<double> a_re_part) const
{
    CH_TIME("Y00Integration::write_integration");
    SmallDataIO integration_file(a_file_prefix, m_dt, m_time, m_restart_time,
                                SmallDataIO::NEW, m_first_step);

    for (int iradius = 0; iradius < m_params.num_integration_radii; ++iradius)
    {
        // Write headers
        std::vector<std::string> header1_strings = {
            "time = " + std::to_string(m_time) + ",",
            "r = " + std::to_string(m_params.integration_radii[iradius])};
        integration_file.write_header_line(header1_strings, "");
        std::vector<std::string> components = {UserVariables::variable_names[var]};
        std::vector<std::string> coords = {"theta", "phi"};
        integration_file.write_header_line(components, coords);

        // Now the data
        for (int idx = iradius * m_num_points;
             idx < (iradius + 1) * m_num_points; ++idx)
        {
            int itheta =
                (idx - iradius * m_num_points) / m_params.num_points_phi;
            int iphi = idx % m_params.num_points_phi;
            // don't put a point at z = 0
            double theta = (itheta + 0.5) * m_dtheta;
            double phi = iphi * m_dphi;

            integration_file.write_data_line({a_re_part[idx]},
                                            {theta, phi});
        }
        integration_file.line_break();
    }
}

#endif /* Y00INTEGRATION_IMPL_HPP_ */
