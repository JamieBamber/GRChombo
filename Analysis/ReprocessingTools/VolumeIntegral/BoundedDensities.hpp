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

#include "Tensor.hpp"
#include "ADMFixedBGVars.hpp"
#include "CCZ4Geometry.hpp"
#include "FourthOrderDerivatives.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
template <class matter_t, class background_t> class BoundedDensities
{
  protected:

    //! Params for integration
    const FourthOrderDerivatives
        m_deriv; //!< An object for calculating derivatives of the variables
    const matter_t m_matter;                        //!< The matter object
    const integration_params_t m_params;
    const double m_dx;                              //!< The grid spacing
    const std::array<double, CH_SPACEDIM> m_center; //!< The grid center
  public:
    BoundedDensities(matter_t a_matter, integration_params_t a_params, background_t a_background, double a_dx, std::array<double, CH_SPACEDIM> a_center)
        : m_matter(a_matter), m_deriv(a_dx), m_dx(a_dx), m_center(a_center), m_params(a_params) 
    {
    }

    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
	// get the metric vars from the background
        const Coordinates<data_t> coords(current_cell, m_dx, m_center);
	const auto d1 = m_deriv.template diff1<MatterVars>(current_cell);
	// coordinates
        data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;    
	data_t R = coords.get_radius();
	// get KerrSchild r
	/*double a = m_params.bh_a;
	data_t disc = simd_max((R*R - a*a), 0.001);
	data_t r2 = disc/2 + sqrt(disc*disc/4 + (a*z)*(a*z));
	data_t r = sqrt(r2);*/

	// get the metric vars from the background
        MetricVars<data_t> metric_vars;
	m_background.compute_metric_background(metric_vars, coords);

	using namespace TensorAlgebra;
        const auto gamma_UU = compute_inverse_sym(metric_vars.gamma);
        const auto chris_phys =
            compute_christoffel(metric_vars.d1_gamma, gamma_UU);
        const emtensor_t<data_t> emtensor = m_matter.compute_emtensor(
            vars, metric_vars, d1, gamma_UU, chris_phys.ULL);
        const data_t det_gamma = 
            TensorAlgebra::compute_determinant_sym(metric_vars.gamma);

	// get rho and rho_azimuth
	data_t rho, rho_azimuth;
	rho = current_cell.load_vars(c_rho);
	//rho_azimuth = current_cell.load_vars(c_rho_azimuth);

	// conserved rho = -sqrt(-g)T^0_0 = sqrt(det_gamma)*(alpha*rho_3+1 - beta^i * S_i)
        data_t rho_out = metric_vars.lapse*rho;
        FOR1(k){ rho_out += -metric_vars.shift[k]*emtensor.Si[k];   }
        rho_out = rho_out*sqrt(det_gamma);

	//
	// data_t inside = simd_compare_lt(r,m_params.max_integration_radius)*simd_compare_gt(r,m_params.min_integration_radius);
	data_t inside = (R < m_params.max_integration_radius) && (R > m_params.min_integration_radius);
	
        // assign values of density in output box
        current_cell.store_vars(inside*rho_out, c_rho);
        //current_cell.store_vars(inside*rho_azimuth, c_rho_azimuth);
    }
};

#endif /* BOUNDEDDENSITIES_HPP_ */
