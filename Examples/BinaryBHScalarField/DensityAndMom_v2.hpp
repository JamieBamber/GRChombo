/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef DENSITYANDMOM_HPP_
#define DENSITYANDMOM_HPP_

#include "CCZ4Geometry.hpp"
#include "Cell.hpp"
#include "BSSNVars.hpp"
#include "Coordinates.hpp"
#include "FourthOrderDerivatives.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total number of components
#include "VarsTools.hpp"
#include "simd.hpp"
#include "DimensionDefinitions.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
template <class matter_t> 
class DensityAndMom
{
  public:
    // Use the variable definition in the matter class
    template <class data_t>
    using MatterVars = typename matter_t::template Vars<data_t>;

    /// CCZ4 variables
    template <class data_t> 
    using MetricVars = BSSNVars::VarsNoGauge<data_t>;

    // Inherit the variables from MatterVars and MetricVars
    template <class data_t>
    struct Vars : public MetricVars<data_t>, public MatterVars<data_t>
    {
        /// Defines the mapping between members of Vars and Chombo grid
        /// variables (enum in User_Variables)
        template <typename mapping_function_t>
        void enum_mapping(mapping_function_t mapping_function)
        {
            MetricVars<data_t>::enum_mapping(mapping_function);
            MatterVars<data_t>::enum_mapping(mapping_function);
        }
    };

    DensityAndMom(matter_t a_matter, double a_dx, std::array<double, CH_SPACEDIM> a_center)
        : m_matter(a_matter), m_deriv(a_dx), m_dx(a_dx), m_center(a_center)
    {
    }

    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
	CH_TIME("DensityAndMom::compute");
        // copy data from chombo gridpoint into local variables, and derivs
	const auto vars = current_cell.template load_vars<Vars>();
        const auto d1 = m_deriv.template diff1<Vars>(current_cell);
        const auto h_UU = TensorAlgebra::compute_inverse_sym(vars.h);
	const auto chris = TensorAlgebra::compute_christoffel(d1.h, h_UU);

    	// Energy Momentum Tensor
    	const auto emtensor = m_matter.compute_emtensor(vars, d1, h_UU, chris.ULL);

    	// assign values of density in output box
    	current_cell.store_vars(emtensor.rho, c_rho);

	// Eulerian momentum density
	const Coordinates<data_t> coords(current_cell, m_dx, m_center);
	data_t x = coords.x;
        double y = coords.y;
        double z = coords.z;
	data_t S_azimuth = x * emtensor.Si[1] - y * emtensor.Si[0];
	data_t r = coords.get_radius();
	data_t S_r = -(x * emtensor.Si[0] + y * emtensor.Si[1] + z * emtensor.Si[2])/r;		
	current_cell.store_vars(S_azimuth, c_S_azimuth);
	current_cell.store_vars(S_r, c_S_r);
     }

  protected:
    const matter_t m_matter;              //!< The matter object
    const FourthOrderDerivatives m_deriv; //!< An object for calculating derivatives of the variables
    const std::array<double, CH_SPACEDIM> m_center; //!< The grid center
    const double m_dx;
};

#endif /* DENSITYANDMOM_HPP_ */
