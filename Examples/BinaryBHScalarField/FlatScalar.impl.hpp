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
    // get coordinates
    Coordinates<data_t> coords(current_cell, m_dx);

    // store phi and Pi
    current_cell.store_vars(m_params.field_amplitude, c_phi);
    // current_cell.store_vars(0, c_Pi);
}

// Compute the value of phi at the current point
/*template <class data_t>
data_t FlatScalar::compute_phi(Coordinates<data_t> coords) const
{
    //data_t rr = coords.get_radius();
    //data_t rr2 = rr * rr;
    //data_t out_phi = m_params.amplitudeSF * rr2 *
    //                exp(-pow(rr - m_params.r_zero / m_params.widthSF, 2.0));

    return m_params.field_amplitude;
}
*/
#endif /* FLATSCALAR_IMPL_HPP_ */
