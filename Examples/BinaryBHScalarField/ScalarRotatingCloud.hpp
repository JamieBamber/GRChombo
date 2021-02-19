/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SCALARROTATINGCLOUD_HPP_
#define SCALARROTATINGCLOUD_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "MatterCCZ4.hpp"
#include "ScalarField.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total no. components
#include "VarsTools.hpp"
#include "simd.hpp"

#include "assoc_legendre.hpp" // I want this for the associted legendre polynomials needed for spherical harmonics

//! Class which creates a rotating cloud of scalar field given params for initial
//! matter config
class ScalarRotatingCloud
{
  public:
    //! A structure for the input params for scalar field properties
    struct params_t
    {
        double field_amplitude; //!< Amplitude of initial SF
        std::array<double, CH_SPACEDIM>
            center;   //!< Centre of perturbation in initial SF bubble
        double omega; //!< frequency of scalar field
	int l; //!< axial number
	int m; //!< azimuthal number
	double alignment; //!< angle between Kerr BH spin and cloud spin in units of PI
        double phase;
    };

    //! Radial function
    template <class data_t>
    data_t R_function(data_t r) const {
      //
      data_t output;
      output = 1.0;
      return output;
    }

    template <class data_t>
    data_t dR_function(data_t r) const {
      //                                                                                                                                                                        
      data_t output;
      output = 0.0;
      return output;
    }
  
    //! The constructor for the class
    ScalarRotatingCloud(params_t a_params, const double a_dx)
        : m_params(a_params), m_dx(a_dx)
    {
    }

    //! Function to compute the value of all the initial vars on the grid
    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
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
	data_t r_function = m_params.field_amplitude * R_function<data_t>(r); 
	//angular dependence of phi
	data_t angular_function = cos(m_params.m * azimuth_prime + M_PI * m_params.phase) * g_function;
        // set the field vars 
	// phi
        data_t phi = r_function * angular_function;
	
	// dphi
	data_t dphidt = r_function * g_function *m_params.omega*sin(m_params.m*azimuth_prime + M_PI * m_params.phase);
	//!< derivative of phi w.r.t the cloud azimuthal angle
	data_t dphid_azimuth_prime = - r_function * g_function *m_params.m*sin(m_params.m*azimuth_prime + M_PI * m_params.phase);
	//!< derivative of phi w.r.t the cloud theta angle
 	data_t dphid_theta_prime = r_function * g_function_prime * cos(m_params.m*azimuth_prime + M_PI * m_params.phase);
	// data_t dphid_azimuth = - sin_alignment * (x / rho_prime) * dphid_theta_prime + (rho2 * cos_alignment - y*z*sin_alignment)*dphid_azimuth_prime/rho_prime2;
	data_t dphid_r = m_params.field_amplitude * dR_function<data_t>(r) * angular_function;
	
	// load lapse and shift
	data_t lapse = current_cell.load_vars(c_lapse);
	data_t shift1 = current_cell.load_vars(c_shift1);
	data_t shift2 = current_cell.load_vars(c_shift2);
	data_t shift3 = current_cell.load_vars(c_shift3);
	//
	data_t shift1_prime = shift1;
        data_t shift2_prime = shift2 * cos_alignment + shift3 * sin_alignment;
        data_t shift3_prime = shift3 * cos_alignment - shift2 * sin_alignment;
	//
	data_t dtheta_prime_dx = ((x*z_prime)/(r*r*rho));
	data_t dtheta_prime_dy_prime = ((y_prime*z_prime)/(r*r*rho_prime));
	data_t dtheta_prime_dz_prime = -1/rho_prime;
	//
	data_t dazimuth_prime_dx = - y_prime/(rho_prime*x);
	data_t dazimuth_prime_dy_prime = 1/rho_prime;
	//
	data_t dr_dx = x/r;
	data_t dr_dy_prime = y_prime/r;
	data_t dr_dz_prime = z_prime/r;

	//
	data_t dphi_dx = dphid_theta_prime * dtheta_prime_dx + dphid_azimuth_prime * dazimuth_prime_dx + dphid_r * dr_dx;
	data_t dphi_dy_prime = dphid_theta_prime * dtheta_prime_dy_prime + dphid_azimuth_prime * dazimuth_prime_dy_prime + dphid_r * dr_dy_prime;
	data_t dphi_dz_prime = dphid_theta_prime * dtheta_prime_dz_prime + dphid_r * dr_dz_prime;
	
	// Pi = alpha * d_t phi + beta^i d_i phi

        // beta_phi in IsotropicKerrFixedBG.hpp
        data_t Pi = lapse * dphidt + shift1_prime * dphi_dx + shift2_prime * dphi_dy_prime + shift3_prime * dphi_dz_prime;

        // Store the initial values of the variables
	current_cell.store_vars(phi, c_phi);
        current_cell.store_vars(Pi, c_Pi);
    }

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params
};

#endif /* ScalarRotatingCloud_HPP_ */
