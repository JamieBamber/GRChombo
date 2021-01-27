/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef GRAMR_HPP_
#define GRAMR_HPP_

// Chombo includes
#include "AMR.H"
#include "Interval.H"

// Other includes
#include "AMRInterpolator.hpp"
#include "VariableType.hpp"
#include "Lagrange.hpp"
#include <algorithm>
#include <chrono>
#include <ratio>
#include <vector>

// Chombo namespace
#include "UsingNamespace.H"

/// A child of Chombo's AMR class to interface with tools which require
/// access to the whole AMR hierarchy (such as the AMRInterpolator)
/**
 *It is necessary for many experimental features and allows us to
 *add said features later without breaking any user code.
 */

// Forward declaration for get_gramrlevels function declarations
class GRAMRLevel;

class GRAMR : public AMR
{
  private:
    using Clock = std::chrono::steady_clock;
    using Hours = std::chrono::duration<double, std::ratio<3600, 1>>;
    std::chrono::time_point<Clock> start_time = Clock::now();

    // This is used by computeSum, computeNorm, etc.
    Vector<LevelData<FArrayBox> *> getLevelDataPtrs();

  public:
    AMRInterpolator<Lagrange<4>> *m_interpolator; //!< The interpolator pointer

    GRAMR();

    // defined here due to auto return type
    auto get_walltime()
    {
        auto now = Clock::now();
        auto duration = std::chrono::duration_cast<Hours>(now - start_time);

        return duration.count();
    }

    // Called after AMR object set up
    void set_interpolator(AMRInterpolator<Lagrange<4>> *a_interpolator);

    // returs a std::vector of GRAMRLevel pointers
    // similar to AMR::getAMRLevels()
    std::vector<GRAMRLevel *> get_gramrlevels();

    // const version of above
    std::vector<const GRAMRLevel *> get_gramrlevels() const;

    // Fill ghosts on multiple levels
    void fill_multilevel_ghosts(
        const VariableType a_var_type,
	const Interval &a_comps = Interval(0, std::numeric_limits<int>::max()),
        const int a_min_level = 0,
        const int a_max_level = std::numeric_limits<int>::max()) const;

    // Returns the volume-weighted sum of a grid variable
    Real compute_sum(const int a_comp, const Real a_dx_coarse);

    // Returns the volume-weighted p-norm of an interval of grid variables
    Real compute_norm(const Interval a_comps, const double a_p,
                      const Real a_dx_coarse);

    // Returns the max value of an interval of grid variables
    Real compute_max(const Interval a_comps);

    // Returns the min value of an interval of grid variables
    Real compute_min(const Interval a_comps);

    // Returns the Infinity norm of an interval of grid variables
    // This function is a bit pointless because a_p = 0 in compute_norm does the
    // same
    Real compute_inf_norm(const Interval a_comps);
};

#endif /* GRAMR_HPP_ */
