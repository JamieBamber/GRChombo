#ifndef CRITERION_HPP_
#define CRITERION_HPP_

#include "CCZ4Geometry.hpp"
#include "Cell.hpp"
#include "Constraints.hpp"
#include "FourthOrderDerivatives.hpp"
#include "GRInterval.hpp"
#include "Tensor.hpp"
#include "simd.hpp"
#include <array>

// Copied from MatterConstraints.hpp

template <class matter_t> 
class Criterion : public Constraints
{
  public:
    //!  Constructor of class Criterion
    Criterion(double dx);

    //! The compute member which stores criterion in c_criterion
    template <class data_t>
    void compute(Cell<data_t> current_cell) const;
};

#include "criterion.impl.hpp"

#endif /* CRITERION_HPP_ */
