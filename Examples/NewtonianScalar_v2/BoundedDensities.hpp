/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef BOUNDEDDENSITIES_HPP_
#define BOUNDEDDENSITIES_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "GRInterval.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total number of components
#include "VarsTools.hpp"
#include "simd.hpp"
#include "SimulationParameters.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
class BoundedDensities
{
  protected:

    //! Params for integration
    const integration_params_t m_params;
    const double m_dx;                              //!< The grid spacing
    const std::array<double, CH_SPACEDIM> m_center; //!< The grid center
    double m_time;
  public:
  BoundedDensities(integration_params_t a_params, double a_dx, std::array<double, CH_SPACEDIM> a_center, double a_time)
    : m_dx(a_dx), m_center(a_center), m_params(a_params), m_time(a_time) 
    {
    }

    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
	// get the metric vars from the background
        const Coordinates<data_t> coords(current_cell, m_dx, m_center);
	// coordinates
        data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;    
	data_t R = coords.get_radius();

	// get rho and rho_azimuth
	data_t rho, rho_azimuth, Cphi;
	rho = current_cell.load_vars(c_rho);
	rho_azimuth = current_cell.load_vars(c_rhoJ);
	Cphi = current_cell.load_vars(c_Cphi);
	
	// work out bh_positions
	double omega = sqrt((m_params.M1+m_params.M2) / (m_params.d*m_params.d*m_params.d) );
	double bh_x = (cos(omega * m_time) - 2);
        double bh_y = sin(omega * abs(m_time));
	data_t r_1 = sqrt( pow(x - m_center[0] - bh_x*m_params.disp1,2)+pow(y - m_center[1] - bh_y*m_params.disp1,2)+pow(z - m_center[2],2));
	data_t r_2 = sqrt( pow(x - m_center[0] + bh_x*m_params.disp2,2)+pow(y - m_center[1] + bh_y*m_params.disp2,2)+pow(z - m_center[2],2));
	r_1 = simd_max(r_1, 0.0001); // avoid divergences
	r_1 = simd_max(r_2, 0.0001); 
	data_t Phi = 2*( m_params.M1/r_1 + m_params.M2/r_2);
	//
	// data_t inside = simd_compare_lt(r,m_params.max_integration_radius)*simd_compare_gt(r,m_params.min_integration_radius);
	data_t inside = ((R < m_params.max_integration_radius) && (R > m_params.min_integration_radius)) && (Phi < 1);
	
        // assign values of density in output box
        current_cell.store_vars(inside*rho, c_rho);
        current_cell.store_vars(inside*rho_azimuth, c_rhoJ);
	current_cell.store_vars(inside*Cphi, c_Cphi);
    }
};

#endif /* BOUNDEDDENSITIES_HPP_ */
