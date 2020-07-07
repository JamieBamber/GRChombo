/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef FLATSCALAR_HPP_
#define FLATSCALAR_HPP_

#include "Cell.hpp"
#include "Coordinates.hpp"
#include "MatterCCZ4.hpp"
#include "ScalarField.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total no. components
#include "VarsTools.hpp"
#include "simd.hpp"

//! Class which creates a uniform scalar field 
//!
class FlatScalar
{
  public:
    //! A structure for the input params for scalar field properties and initial
    //! conditions
    struct params_t
    {
        double field_amplitude; //!< Amplitude of bump in initial SF bubble
    };

    //! The constructor
    FlatScalar(params_t a_params, double a_dx);

    //! Function to compute the value of all the initial vars on the grid
    template <class data_t> void compute(Cell<data_t> current_cell) const;

  protected:
    double m_dx;
    const params_t m_params; //!< The matter initial condition params

    //! Function to compute the value of phi at each point
    template <class data_t>
    data_t compute_phi(Coordinates<data_t> coords) const;
};

#include "FlatScalar.impl.hpp"

#endif /* FLATSCALAR_HPP_ */
