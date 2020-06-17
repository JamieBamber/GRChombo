/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

// General includes common to most GR problems
#include "ScalarFieldLevel.hpp"
#include "BoxLoops.hpp"
#include "NanCheck.hpp"

// For RHS update
#include "KerrSchildFixedBG.hpp"
#include "Excision.hpp"
#include "FixedBGEvolution.hpp"

// For density calculation
#include "FixedBGDensityAndMom_v3.hpp"

// For tag cells
#include "FixedGridsTaggingCriterion.hpp"

// Problem specific includes
#include "ComputePack.hpp"
#include "FixedBGScalarField.hpp"
#include "Potential.hpp"
#include "ScalarRotatingCloud.hpp"
#include "SetValue.hpp"
#include "KerrSchildFluxExtraction.hpp"

// Things to do at each advance step, after the RK4 is calculated
void ScalarFieldLevel::specificAdvance()
{
    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck(), m_state_new, m_state_new,
                       EXCLUDE_GHOST_CELLS, disable_simd());
}

// Initial data for field and metric variables
void ScalarFieldLevel::initialData()
{
    CH_TIME("ScalarFieldLevel::initialData");
    if (m_verbosity)
        pout() << "ScalarFieldLevel::initialData " << m_level << endl;

    // First set everything to zero ... we don't want undefined values in
    // constraints etc, then initial conditions for scalar field
    KerrSchildFixedBG kerr_bg(m_p.bg_params, m_dx);
    ScalarRotatingCloud initial_sf(m_p.initial_params, m_p.bg_params, m_dx);
    BoxLoops::loop(make_compute_pack(SetValue(0.0), kerr_bg, initial_sf),
                   m_state_new, m_state_new, INCLUDE_GHOST_CELLS);
}

// Things to do after each timestep
void ScalarFieldLevel::specificPostTimeStep()
{
    // At any level, but after the coarsest timestep
    double coarsest_dt = m_p.coarsest_dx * m_p.dt_multiplier;
    const double remainder = fmod(m_time, coarsest_dt);
    if (min(abs(remainder), abs(remainder - coarsest_dt)) < 1.0e-8)
    {    
	// Calculate density and flux variables
        fillAllGhosts();
        Potential potential(m_p.potential_params);
        ScalarFieldWithPotential scalar_field(potential);
        KerrSchildFixedBG kerr_bg(m_p.bg_params, m_dx);
        BoxLoops::loop(FixedBGDensityAndMom<ScalarFieldWithPotential, KerrSchildFixedBG>(
                       scalar_field, kerr_bg, m_dx, m_p.center, m_p.initial_params.alignment),
                   m_state_new, m_state_new, EXCLUDE_GHOST_CELLS);
     }
     
     // write out the integral after each coarse timestep
     if (m_level == 0)
     {
        // Refresh the interpolator and integrate the fluxes
        m_gr_amr.m_interpolator->refresh();
        KSFluxExtraction my_extraction(m_p.extraction_params, m_dt, m_time, m_p.flux_file_name,
                                  	m_restart_time);
        my_extraction.execute_query(m_gr_amr.m_interpolator);
    }
}

// Things to do before outputting a plot file
void ScalarFieldLevel::prePlotLevel()
{}

/*    // Calculate matter density function
    fillAllGhosts();
    Potential potential(m_p.potential_params);
    ScalarFieldWithPotential scalar_field(potential);
    KerrSchildFixedBG kerr_bg(m_p.bg_params, m_dx);
    BoxLoops::loop(FixedBGDensityAndMom<ScalarFieldWithPotential, KerrSchildFixedBG>(
                       scalar_field, kerr_bg, m_dx, m_p.center, m_p.initial_params.alignment),
                   m_state_new, m_state_new, EXCLUDE_GHOST_CELLS);
}*/

// Things to do in RHS update, at each RK4 step
void ScalarFieldLevel::specificEvalRHS(GRLevelData &a_soln, GRLevelData &a_rhs,
                                       const double a_time)
{
    // Calculate right hand side with matter_t = ScalarField
    // and background_t = IsotropicKerrBH
    // RHS for non evolution vars is zero, to prevent undefined values
    Potential potential(m_p.potential_params);
    ScalarFieldWithPotential scalar_field(potential);
    KerrSchildFixedBG kerr_bg(m_p.bg_params, m_dx);
    FixedBGEvolution<ScalarFieldWithPotential, KerrSchildFixedBG> my_evolution(
        scalar_field, kerr_bg, m_p.sigma, m_dx, m_p.center);
    SetValue set_static_rhs_zero(0.0, Interval(c_chi, NUM_VARS-1));
    auto compute_pack = make_compute_pack(my_evolution, set_static_rhs_zero);
    BoxLoops::loop(compute_pack, a_soln, a_rhs, EXCLUDE_GHOST_CELLS);

    // Do excision within horizon
    BoxLoops::loop(Excision<ScalarFieldWithPotential, KerrSchildFixedBG>(
                       m_dx, m_p.center, kerr_bg),
                   a_soln, a_rhs, EXCLUDE_GHOST_CELLS, disable_simd());
}

// Note that for the fixed grids this only happens on the initial timestep
// simd is disabled to allow simpler use of logical operators
void ScalarFieldLevel::computeTaggingCriterion(FArrayBox &tagging_criterion,
                                               const FArrayBox &current_state)
{
    BoxLoops::loop(FixedGridsTaggingCriterion(m_dx, m_level, m_p.L, m_p.center),
                   current_state, tagging_criterion, disable_simd());
}

// Specify if you want any plot files to be written, with which vars
void ScalarFieldLevel::specificWritePlotHeader(std::vector<int> &plot_states) const;
