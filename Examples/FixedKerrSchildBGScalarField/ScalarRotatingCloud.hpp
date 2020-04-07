/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SCALARROTATINGCLOUD_HPP_
#define SCALARROTATINGCLOUD_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "ScalarField.hpp"

#include "ADMFixedBGVars.hpp"
#include "KerrSchildFixedBG.hpp"

#include "assoc_legendre.hpp" // I want this for the associted legendre polynomials needed for spherical harmonics

#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total no. components
#include "VarsTools.hpp"
#include "simd.hpp"

//! Class which creates a rotating cloud of scalar field given params for initial
//! matter config
class ScalarRotatingCloud
{
  public:
    //! A structure for the input params for scalar field properties
    struct params_t
    {
        double amplitude; //!< Amplitude of initial SF
        std::array<double, CH_SPACEDIM>
            center;   //!< Centre of perturbation in initial SF bubble
        double omega; //!< frequency of scalar field
	int l; //!< axial number
	int m; //!< azimuthal number
	double alignment; //!< angle between Kerr BH spin and cloud spin in units of PI
    };

    //! The constructor for the class
    ScalarRotatingCloud(params_t a_params, const KerrSchildFixedBG::params_t a_bg_params, const double a_dx)
        : m_params(a_params), m_dx(a_dx), m_bg_params(a_bg_params)
    {
    }

    //! Function to compute the value of all the initial vars on the grid
    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
        ScalarField<>::Vars<data_t> vars;
        
	// extract the coordinates
        Coordinates<data_t> coords(current_cell, m_dx, m_params.center);
	data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;	
	// Kerr Schild parameters
	double a = m_bg_params.spin*m_bg_params.mass;
	double M = m_bg_params.mass;
	double a2 = a*a;

	// perform rotation about x axis by the alignment angle

	// Cartesian radius
	data_t rho = coords.get_radius();
	data_t rho2 = rho * rho;

	// convert to KS r
	data_t r2 = 0.5 * (rho2 - a2) + sqrt(0.25 * (rho2 - a2) * (rho2 - a2) 
                                            + a2 * z*z); 
	data_t r = sqrt(r2);

	// the radius in xy' plane, subject to a floor
	data_t cos_theta = z / r;
	data_t sin_theta = sqrt(1 - cos_theta*cos_theta);

	// --> need to be careful for the Kerr Schild coordinates
	data_t azimuth = atan2(y*r+a*x, x*r - a*y);	// need to use atan2 to obtain full 0 to 2pi range
	// radius in the xy plane, subject to a floor

	// get the metric vars
        KerrSchildFixedBG kerr_bh(m_bg_params, m_dx);
        MetricVars<data_t> metric_vars;
        kerr_bh.compute_metric_background(metric_vars, coords);
	
	auto my_P_lm = AssocLegendre::assoc_legendre_with_deriv(m_params.l, m_params.m, cos_theta, sin_theta);
	data_t g_function = my_P_lm.Magnitude;
        data_t g_function_prime = my_P_lm.Derivative;

	// r dependence of phi
	data_t r_function = m_params.amplitude; 
	//angular dependence of phi
	data_t angular_function = sin(m_params.m * azimuth) * g_function;
        // set the field vars 
	// phi
        vars.phi = r_function * angular_function;
	
	// dphi
	data_t dphidt = - r_function * g_function * m_params.omega*cos(m_params.m*azimuth);
	//!< derivative of phi w.r.t the azimuthal angle and theta
	data_t dphid_azimuth = r_function * g_function * m_params.m*cos(m_params.m*azimuth);
 	//data_t dphid_theta = r_function * g_function_prime * sin(m_params.m*azimuth);
	
	// shift 
	data_t Sigma = r2 + a2*cos_theta*cos_theta;
	data_t beta_azimuth = -2*M*r*a/(Sigma*(a2 + r2));

	// beta_phi in KerSchildFixedBG

	// Pi = alpha * d_t phi + beta^i d_i phi
        vars.Pi = metric_vars.lapse * dphidt + beta_azimuth * dphid_azimuth;

        // Store the initial values of the variables
        current_cell.store_vars(vars);
    }

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params
    const KerrSchildFixedBG::params_t m_bg_params; //!< the background metric parameters

    // Now the non grid ADM vars
    template <class data_t> using MetricVars = ADMFixedBGVars::Vars<data_t>;

};

#endif /* ScalarRotatingCloud_HPP_ */
