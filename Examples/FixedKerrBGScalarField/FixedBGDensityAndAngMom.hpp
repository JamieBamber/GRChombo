/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef FIXEDBGDENSITYANDANGMOM_HPP_
#define FIXEDBGDENSITYANDANGMOM_HPP_

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
template <class matter_t, class background_t> class FixedBGDensityAndAngMom
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
    double m_L;					    //!< the simulation box L
    const double m_alignment;		            //!< angle between cloud spin and Kerr BH spin (in units of pi)

  public:
    FixedBGDensityAndAngMom(matter_t a_matter, background_t a_background, double a_dx,
                 std::array<double, CH_SPACEDIM> a_center, double a_L, double a_alignment)
        : m_matter(a_matter), m_deriv(a_dx), m_dx(a_dx),
          m_background(a_background), m_center(a_center), m_L(a_L), m_alignment(a_alignment)
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

	// find angular momentum in Kerr BH direction and the cloud spin direction
	data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;	
        // perform rotation about x axis by the alignment angle
        double cos_alignment = cos(m_alignment*M_PI);
        double sin_alignment = sin(m_alignment*M_PI);
        double y_prime = y * cos_alignment + z * sin_alignment;

	// S_azimuth = x * S_y - y * S_z
	// S_azimuth_prime = x(S_y cos(alignment) + S_z sin(alignment)) - yprime * S_x

	// the boundaries of the box throw up issues with the angular momentum calculation, so 
	// I fix S = 0 on the boundaries
	double lim = 0.9 * 0.5*m_L;
	//bool xfit = simd_compare_lt(-x_lim, x) && simd_compare_lt(x, x_lim);
	bool xfit = (-lim < x) && (x < lim);
	bool yfit = (-lim < y) && (y < lim);
	bool zfit = (-lim < z) && (z < lim);
	bool fit = (xfit && yfit) && zfit;
	data_t S_azimuth = 0.0;
        data_t S_azimuth_prime = 0.0;
	if (fit) {
		// check they are not NaN or too big
		data_t S_azimuth_test = x * emtensor.Si[1] - y * emtensor.Si[0];
		data_t S_azimuth_prime_test = x*(cos_alignment*emtensor.Si[1] + sin_alignment*emtensor.Si[2]) - y_prime*emtensor.Si[0];
		double S_lim = 1000;
		bool isnan_test = ( !isnan(S_azimuth_test) && !isnan(S_azimuth_prime_test) );
		bool too_big_test = ( ((S_azimuth_test < S_lim) && (-S_lim < S_azimuth_test)) 
                          && ((-S_lim < S_azimuth_prime_test) && (S_azimuth_prime_test < S_lim)) );
		pout() << "S_azimuth_test = " << S_azimuth_test << " too_big_test " << too_big_test << endl;
		bool ok_values = isnan_test && too_big_test;
		if (ok_values) {
			S_azimuth = S_azimuth_test;
			S_azimuth_prime = S_azimuth_prime_test;
 		}
	}
        // assign values of density in output box
        current_cell.store_vars(emtensor.rho, c_rho);
	current_cell.store_vars(S_azimuth, c_S_azimuth);
	current_cell.store_vars(S_azimuth_prime, c_S_azimuth_prime);
    }
};

#endif /* FIXEDBGDENSITYANDANGMOM_HPP_ */
