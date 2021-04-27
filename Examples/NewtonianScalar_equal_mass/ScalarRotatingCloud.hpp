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
    ScalarRotatingCloud(params_t a_params, const double a_dx)
        : m_params(a_params), m_dx(a_dx)
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

	auto my_P_lm = AssocLegendre::assoc_legendre_with_deriv(m_params.l, m_params.m, cos_theta_prime, sin_theta_prime);
	data_t g_function = my_P_lm.Magnitude;
        data_t g_function_prime = my_P_lm.Derivative;

	// r dependence of phi
	data_t r_function = m_params.amplitude; 
	//angular dependence of phi
	data_t angular_function = cos(m_params.m * azimuth_prime) * g_function;
        // set the field vars 
	// phi
        data_t phi = r_function * angular_function;
	
	// dphi
	data_t dphidt = r_function * g_function *m_params.omega*sin(m_params.m*azimuth_prime);
	//!< derivative of phi w.r.t the cloud azimuthal angle
	data_t dphid_azimuth_prime = - r_function * g_function *m_params.m*sin(m_params.m*azimuth_prime);
	//!< derivative of phi w.r.t the cloud theta angle
 	data_t dphid_theta_prime = r_function * g_function_prime * cos(m_params.m*azimuth_prime);
	data_t dphid_azimuth = - sin_alignment * (x / rho_prime) * dphid_theta_prime + (rho2 * cos_alignment - y*z*sin_alignment)*dphid_azimuth_prime/rho_prime2;
	
	// Pi = alpha * d_t phi + beta^i d_i phi
        data_t Pi = dphidt;

        // Store the initial values of the variables
	current_cell.store_vars(phi, c_phi_Re);
        current_cell.store_vars(0.0, c_phi_Im);
        current_cell.store_vars(Pi, c_Pi_Re);
        current_cell.store_vars(0, c_Pi_Im);
    }

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params

    // Now the non grid ADM vars
    template <class data_t> using MetricVars = ADMFixedBGVars::Vars<data_t>;

};

#endif /* ScalarRotatingCloud_HPP_ */
