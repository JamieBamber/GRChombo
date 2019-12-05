#if !defined(RHO_HPP_)
#error "This file should only be included through MatterConstraints.hpp"
#endif

#ifndef RHO_IMPL_HPP_
#define RHO_IMPL_HPP_
#include "DimensionDefinitions.hpp"

template <class matter_t>
// template parameter declaration for the member function of the template class "MatterConstraints"
Rho<matter_t>::Rho(const matter_t a_matter,
                                               double dx, double G_Newton)
    : Constraints(dx, 0.0 /*No cosmological constant*/), my_matter(a_matter),
      m_G_Newton(G_Newton) // this initialiser list initialises the protected variables "my_matter" and "m_G_Newton", maybe also the class "Constraints"?
{
}

template <class matter_t>
template <class data_t>
void Rho<matter_t>::compute(Cell<data_t> current_cell) const
{
    current_cell.store_vars(1.0, c_rho);
}


#endif /* RHO_IMPL_HPP_ */
