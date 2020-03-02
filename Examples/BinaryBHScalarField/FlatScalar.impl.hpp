/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#if !defined(FLATSCALAR_HPP_)
#error "This file should only be included through FlatScalar.hpp"
#endif

#ifndef FLATSCALAR_IMPL_HPP_
#define FLATSCALAR_IMPL_HPP_

inline FlatScalar::FlatScalar(params_t a_params, double a_dx)
    : m_dx(a_dx), m_params(a_params)
{
}

// Compute the value of the initial vars on the grid
template <class data_t>
void FlatScalar::compute(Cell<data_t> current_cell) const
{
    MatterCCZ4<ScalarField<>>::Vars<data_t> vars;
    VarsTools::assign(vars, 0.); // Set only the non-zero components below
    // Coordinates<data_t> coords(current_cell, m_dx, m_params.centerSF);

    // set the field vars
    vars.phi = m_params.amplitudeSF; // uniform phi field
    vars.Pi = 0;

    // Store the initial values of the variables
    current_cell.store_vars(vars);
}

#endif /* FLATSCALAR_IMPL_HPP_ */
