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
#include "IsotropicKerrFixedBG.hpp"

#include "legendre.hpp" // I want this for the derivatives of legendre polynomials

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
    ScalarRotatingCloud(params_t a_params, const IsotropicKerrFixedBG::params_t a_bg_params, const double a_dx)
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
	// perform rotation about x axis by the alignment angle
	double cos_alignment = cos(m_params.alignment*M_PI);
	double sin_alignment = sin(m_params.alignment*M_PI);
	double y_prime = y * cos_alignment + z * sin_alignment;
	double z_prime = z * cos_alignment - y * sin_alignment; 
	data_t r = coords.get_radius();
	// the radius in xy' plane, subject to a floor
        data_t rho_prime2 = simd_max(x * x + y_prime * y_prime, 1e-8);
        data_t rho_prime = sqrt(rho_prime2);
	data_t cos_theta_prime = z_prime / r;
	data_t sin_theta_prime = rho_prime / r;
	data_t azimuth_prime = atan2(y_prime, x);	// need to use atan2 to obtain full 0 to 2pi range
	// radius in the xy plane, subject to a floor
	data_t rho2 = simd_max(x * x + y * y, 1e-8); // try making this 1e-4
        data_t rho = sqrt(rho2);

	// get the metric vars
        IsotropicKerrFixedBG kerr_bh(m_bg_params, m_dx);
        MetricVars<data_t> metric_vars;
        kerr_bh.compute_metric_background(metric_vars, coords);

	data_t g_function = my_legendre_p(m_params.l, cos_theta_prime);
        data_t g_function_prime = my_legendre_p_prime(m_params.l, cos_theta_prime);

	// r dependence of phi
	data_t r_function = m_params.amplitude; 
	//angular dependence of phi
	data_t angular_function = sin(m_params.m * azimuth_prime) * g_function;
        // set the field vars 
	// phi
        vars.phi = r_function * angular_function;
	
	// dphi
	data_t dphidt = - r_function * g_function *m_params.omega*cos(m_params.m*azimuth_prime);
	//!< derivative of phi w.r.t the cloud azimuthal angle
	data_t dphid_azimuth_prime = r_function * g_function *m_params.m*cos(m_params.m*azimuth_prime);
	//!< derivative of phi w.r.t the cloud theta angle
 	data_t dphid_theta_prime = r_function * (-sin_theta_prime) * 
g_function_prime *sin(m_params.m*azimuth_prime);

	data_t dphid_azimuth = - sin_alignment * (x / rho_prime) * dphid_theta_prime + (rho2 * cos_alignment - 
y*z*sin_alignment)*dphid_azimuth_prime/rho_prime2;
	
	//beta^azimuth
	data_t beta_azimuth = sqrt( (pow(metric_vars.shift[0],2) + pow(metric_vars.shift[1],2))/rho2 );
	// ---> its kind of annoying to have to recompute this, it would be better to get it directly from
	// beta_phi in IsotropicKerrFixedBG.hpp

	// Pi = alpha * d_t phi + beta^i d_i phi
        vars.Pi = metric_vars.lapse * dphidt + beta_azimuth * dphid_azimuth;

        // Store the initial values of the variables
        current_cell.store_vars(vars);
    }

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params
    const IsotropicKerrFixedBG::params_t m_bg_params; //!< the background metric parameters

    // Now the non grid ADM vars
    template <class data_t> using MetricVars = ADMFixedBGVars::Vars<data_t>;

};

#endif /* ScalarRotatingCloud_HPP_ */
