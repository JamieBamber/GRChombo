/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef FIXEDBGDENSITYANDMOM_HPP_
#define FIXEDBGDENSITYANDMOM_HPP_

#include "ADMFixedBGVars.hpp"
#include "CCZ4Geometry.hpp"
#include "Cell.hpp"
#include "Coordinates.hpp"
#include "FourthOrderDerivatives.hpp"
#include "GRInterval.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total number of components
#include "VarsTools.hpp"
#include "simd.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
template <class matter_t, class background_t> class FixedBGDensityAndMom
{
    // Use the variable definition in the matter class
    template <class data_t>
    using MatterVars = typename matter_t::template Vars<data_t>;

    // Now the non grid ADM vars
    template <class data_t> using MetricVars = ADMFixedBGVars::Vars<data_t>;

  protected:
    const FourthOrderDerivatives
        m_deriv; //!< An object for calculating derivatives of the variables
    const matter_t m_matter;                        //!< The matter object
    const double m_dx;                              //!< The grid spacing
    const background_t m_background;                //!< The metric background
    const std::array<double, CH_SPACEDIM> m_center; //!< The grid center
    const double m_alignment;		            //!< angle between cloud spin and Kerr BH spin (in units of pi)

  public:
    FixedBGDensityAndMom(matter_t a_matter, background_t a_background, double a_dx,
                 std::array<double, CH_SPACEDIM> a_center, double a_alignment)
        : m_matter(a_matter), m_deriv(a_dx), m_dx(a_dx),
          m_background(a_background), m_center(a_center), m_alignment(a_alignment)
    {
    }

    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
        // copy data from chombo gridpoint into local variables, and derivs
        const auto vars = current_cell.template load_vars<MatterVars>();
        const auto d1 = m_deriv.template diff1<MatterVars>(current_cell);

	// get the metric vars from the background
        MetricVars<data_t> metric_vars;
        const Coordinates<data_t> coords(current_cell, m_dx, m_center);
        m_background.compute_metric_background(metric_vars, coords);

        using namespace TensorAlgebra;
        const auto gamma_UU = compute_inverse_sym(metric_vars.gamma);
        const auto chris_phys =
            compute_christoffel(metric_vars.d1_gamma, gamma_UU);
        const emtensor_t<data_t> emtensor = m_matter.compute_emtensor(
            vars, metric_vars, d1, gamma_UU, chris_phys.ULL);
	const data_t det_gamma = 
            TensorAlgebra::compute_determinant_sym(metric_vars.gamma);

        // first rho. True rho = -sqrt(-g)T^0_0 = sqrt(det_gamma)*(alpha*rho_3+1 - beta^i * S_i)
        data_t rho = metric_vars.lapse*emtensor.rho;
        FOR1(k){ rho += -metric_vars.shift[k]*emtensor.Si[k];   }
        rho = rho*sqrt(det_gamma);

        // find angular momentum in Kerr BH direction and the cloud spin direction
        data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;    

	// conserved j^i = -sqrt(-g)T^i_0 = det(gamma)*alpha*gamma^ij[ alpha * S_j - beta^k S_kj ] for the cartesian coordinates
        Tensor<1, data_t> Sbeta; 
        FOR2(i, j){ Sbeta[i] += metric_vars.shift[j]*emtensor.Sij[i][j]; }                      
        Tensor<1, data_t> J; 
        FOR2(i, j){ J[i] += sqrt(det_gamma)*metric_vars.lapse*( gamma_UU[i][j]*(metric_vars.lapse*emtensor.Si[j] - Sbeta[j]) ); }                       

        // J_azimuth = x * S_y - y * S_z
        // J_azimuth_prime = x(S_y cos(alignment) + S_z sin(alignment)) - yprime * S_x
        data_t J_azimuth = (x * emtensor.Si[1] - y * emtensor.Si[0]);

        // fine the inward radial momentum (i.e. radial mass flux density)
        // S_r = (x * S_x + y * S_y + z * S_z)/r
        data_t r = coords.get_radius();
        data_t J_r = -(x * J[0] + y * J[1] + z * J[2])/r;

        // assign values of density in output box
        current_cell.store_vars(rho, c_rho);
        current_cell.store_vars(J_azimuth, c_J_azimuth);
        current_cell.store_vars(J_r, c_J_r);
    }
};

#endif /* FIXEDBGDENSITYANDMOM_HPP_ */
