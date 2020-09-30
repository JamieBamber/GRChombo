/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef REDEFINEDDENSITIES_HPP_
#define REDEFINEDDENSITIES_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "GRInterval.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total number of components
#include "VarsTools.hpp"
#include "simd.hpp"
#include "SimulationParameters.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
class RedefinedDensities
{
  protected:

    //! Params for integration
    const double m_dx;                              //!< The grid spacing
    const std::array<double, CH_SPACEDIM> m_center; //!< The grid center
  public:
    RedefinedDensities(double a_dx, std::array<double, CH_SPACEDIM> a_center)
        : m_dx(a_dx), m_center(a_center) 
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

	// get rho, rho_azimuth and chi
	data_t rho, rho_azimuth, chi, inv_det_gamma;
	rho = current_cell.load_vars(c_rho);
	rho_azimuth = current_cell.load_vars(c_rho_azimuth);
	chi = current_cell.load_vars(c_chi);
	// sqrt(gamma) = chi^{-3/2}
	inv_det_gamma = pow(chi, 3/2);

	//
        // assign values of density in output box
        current_cell.store_vars(inv_det_gamma*rho, c_rho);
        current_cell.store_vars(inv_det_gamma*rho_azimuth, c_rho_azimuth);
    }
};

#endif /* REDEFINEDDENSITIES_HPP_ */
