/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef HEUNCLOUDS_HPP_
#define HEUNCLOUDS_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "MatterCCZ4.hpp"
#include "ScalarField.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total no. components
#include "VarsTools.hpp"
#include "simd.hpp"
#include "BoostedBH.hpp"

#include "KerrBH_Rfunc.hpp"

//! Class which creates a uniform scalar field 
//!
class HeunClouds
{
  public:
    //! A structure for the input params for scalar field properties and initial
    //! conditions
    struct params_t
    {
        double field_amplitude; //!< Amplitude of SF clouds
	double scalar_mass;     //!< mass of scalar field
	BoostedBH::params_t bh1, bh2; //!< initial parameters for the binary BHs
    };

    HeunClouds(params_t a_params, double a_dx) : m_params(a_params), m_dx(a_dx),
    		KRF(m_params.bh1.mass, m_params.scalar_mass, m_params.scalar_mass, 0.0, 0, 0)

    {
    };

    //! Function to compute the value of all the initial vars on the grid
    template <class data_t>
    void compute(Cell<data_t> current_cell) const
    {
	Coordinates<data_t> coords(current_cell, m_dx);	
	data_t x = coords.x;
	double y = coords.x;
	double z = coords.z;
	Tensor<1, data_t> X;
	X[0] = x;
	X[1] = y;
	X[2] = z; 
	data_t R1sqrd = std::pow(x - m_params.bh1.center[0], 2) + std::pow(y - m_params.bh1.center[1], 2) + std::pow(z - m_params.bh1.center[2], 2);
	// the Kerr Schild radius r
        /*const data_t r1 = sqrt(0.5 * (R1sqrd - a2) 
                                  + sqrt(0.25 * (R1sqrd - a2) * (R1sqrd - a2) 
                                            + a2 * z1*z1));*/
	const double min_r = m_params.bh1.mass*2;
	data_t r1 = simd_max(sqrt(R1sqrd), min_r);
	data_t R2sqrd = std::pow(x - m_params.bh2.center[0], 2) + std::pow(y - m_params.bh2.center[1], 2) + std::pow(z - m_params.bh2.center[2], 2);
	data_t r2 = simd_max(sqrt(R2sqrd), min_r);
	data_t lapse = current_cell.load_vars(c_lapse);
	Tensor<1, data_t> shift;
	shift[0] = current_cell.load_vars(c_shift1);
	shift[1] = current_cell.load_vars(c_shift2);
	shift[2] = current_cell.load_vars(c_shift3);
	// compute HeunC functions
	Rfunc_with_deriv cloud1 = KRF.compute_with_deriv(r1, 0.0, false, true);
	Rfunc_with_deriv cloud2 = KRF.compute_with_deriv(r2, 0.0, false, true);
	data_t phi = m_params.field_amplitude*(cloud1.Rfunc + cloud2.Rfunc);
	data_t d_phi_dt = m_params.field_amplitude*(cloud1.Rfunc + cloud2.d_Rfunc_dt);
	data_t Pi = lapse * d_phi_dt;
	FOR(j){ Pi += shift[j]*m_params.field_amplitude*( (X[j] - m_params.bh1.center[j])*cloud1.d_Rfunc_dr/r1 + (X[j] - 
			m_params.bh2.center[j])*cloud2.d_Rfunc_dr/r2); }
    	// set the field vars
   	current_cell.store_vars(phi, c_phi);
   	current_cell.store_vars(Pi, c_Pi);
    };

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params
    KerrBH_Rfunc KRF;
};

#endif /* HEUNCLOUDS_HPP_ */
