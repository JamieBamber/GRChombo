/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#include "BinaryBHLevel.hpp"
#include "BinaryBH.hpp"
#include "BoxLoops.hpp"
#include "ChiExtractionTaggingCriterion.hpp"
#include "ChiPunctureExtractionTaggingCriterion.hpp"
#include "ComputePack.hpp"
#include "MatterCCZ4.hpp"
#include "MatterConstraints.hpp"
#include "NanCheck.hpp"
#include "PositiveChiAndAlpha.hpp"
#include "Potential.hpp"
#include "PunctureTracker.hpp"
#include "ScalarField.hpp"
#include "SetValue.hpp"
#include "TraceARemoval.hpp"
#include "Weyl4.hpp"
#include "WeylExtraction.hpp"

#include "MatterOnly.hpp"
#include "DensityAndMom.hpp"
#include "ScalarRotatingCloud.hpp"

// Things to do during the advance step after RK4 steps
void BinaryBHLevel::specificAdvance()
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::specificAdvance " << m_level << endl;

    // Enforce the trace free A_ij condition and positive chi and alpha
    BoxLoops::loop(make_compute_pack(TraceARemoval(), PositiveChiAndAlpha()),
                   m_state_new, m_state_new, EXCLUDE_GHOST_CELLS);

    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in specific Advance: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());
}

// This initial data uses an approximation for the metric which
// is valid for small boosts
void BinaryBHLevel::initialData()
{
    CH_TIME("BinaryBHLevel::initialData");
    if (m_verbosity)
        pout() << "BinaryBHLevel::initialData " << m_level << endl;

    // Set up the compute class for the BinaryBH initial data
    BinaryBH binary(m_p.bh1_params, m_p.bh2_params, m_dx);

    
    // set the value of phi - constant over the grid
    /* SetValue set_phi(m_p.initial_params.field_amplitude, Interval(c_phi, c_phi));

    // First set everything to zero (to avoid undefinded values)
    // then calculate initial data
    BoxLoops::loop(make_compute_pack(SetValue(0.), set_phi, binary),
                   m_state_new, m_state_new, INCLUDE_GHOST_CELLS);*/
    
    
    // First set everything to zero (to avoid undefinded values in constraints)
    // then calculate initial data
    BoxLoops::loop(make_compute_pack(SetValue(0.), binary), m_state_new,
                  m_state_new, INCLUDE_GHOST_CELLS);

    // scalar field compute class
    ScalarRotatingCloud initial_sf(m_p.initial_params, m_dx);
    BoxLoops::loop(initial_sf, m_state_new,
                   m_state_new, INCLUDE_GHOST_CELLS);

   // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in initial data: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());

}

// Calculate RHS during RK4 substeps
void BinaryBHLevel::specificEvalRHS(GRLevelData &a_soln, GRLevelData &a_rhs,
                                    const double a_time)
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::specificEvalRHS " << m_level << endl;
 
    // Enforce positive chi and alpha and trace free A
    BoxLoops::loop(make_compute_pack(TraceARemoval(), PositiveChiAndAlpha()),
                   a_soln, a_soln, EXCLUDE_GHOST_CELLS);

    // ---> With Scalar Field
    Potential potential(m_p.potential_params);
    ScalarFieldWithPotential scalar_field(potential);
    if (m_time < m_p.delay){
            MatterOnly<ScalarFieldWithPotential> my_matter(
                scalar_field, m_p.sigma, m_dx);
            BoxLoops::loop(SetValue(0.0),
                a_soln, a_rhs, INCLUDE_GHOST_CELLS);
            BoxLoops::loop(my_matter,
                a_soln, a_rhs, EXCLUDE_GHOST_CELLS);

    } else {
           MatterCCZ4<ScalarFieldWithPotential> my_ccz4_matter(
           scalar_field, m_p.ccz4_params, m_dx, m_p.sigma, m_p.formulation,
           m_p.G_Newton);
           BoxLoops::loop(my_ccz4_matter, a_soln, a_rhs, EXCLUDE_GHOST_CELLS);
	   /*MatterCCZ4<ScalarFieldWithPotential> my_ccz4_matter(
                scalar_field, m_p.ccz4_params, m_dx, m_p.sigma, m_p.formulation,
                m_p.G_Newton);
            BoxLoops::loop(
                make_compute_pack(my_ccz4_matter,
                          SetValue(0, Interval(c_rho, NUM_VARS - 1))),
			  a_soln, a_rhs, EXCLUDE_GHOST_CELLS);*/
    }

    // Calculate CCZ4 right hand side
    /*MatterCCZ4<ScalarFieldWithPotential> my_ccz4_matter(
        scalar_field, m_p.ccz4_params, m_dx, m_p.sigma, m_p.formulation,
        m_p.G_Newton);
	BoxLoops::loop(my_ccz4_matter, a_soln, a_rhs, EXCLUDE_GHOST_CELLS);*/

    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in specificEvalRHS: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());

}

// enforce trace removal during RK4 substeps
void BinaryBHLevel::specificUpdateODE(GRLevelData &a_soln,
                                      const GRLevelData &a_rhs, Real a_dt)
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::specificUpdateODE " << m_level << endl;

    // Enforce the trace free A_ij condition
    BoxLoops::loop(TraceARemoval(), a_soln, a_soln, EXCLUDE_GHOST_CELLS);

    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in specific update ODE: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());
}

// specify the cells to tag
void BinaryBHLevel::computeTaggingCriterion(FArrayBox &tagging_criterion,
                                            const FArrayBox &current_state)
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::computeTaggingCriterion " << m_level << endl;

    if (m_p.track_punctures)
    {
        const vector<double> puncture_masses = {m_p.bh1_params.mass,
                                                m_p.bh2_params.mass};
        auto puncture_coords = m_bh_amr.m_puncture_tracker.get_puncture_coords();
        // trick tagging to do as if extracting, even though potentially not
        // (just fixes a bug due to insufficient resolution on coarsest level)
        const bool activate_extraction = true;
        BoxLoops::loop(ChiPunctureExtractionTaggingCriterion(
                           m_dx, m_level, m_p.max_level, m_p.extraction_params,
                           puncture_coords, activate_extraction,
                           m_p.track_punctures, puncture_masses),
                       current_state, tagging_criterion);
    }
    else
    {
        BoxLoops::loop(ChiExtractionTaggingCriterion(
                           m_dx, m_level, m_p.max_level, m_p.extraction_params,
                           m_p.activate_extraction),
                       current_state, tagging_criterion);
    }

    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in compute Tagging Criterion: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());
}

void BinaryBHLevel::specificPostTimeStep()
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::specificPostTimeStep " << m_level << endl;

    bool first_step = (m_time == 0.);
    
    CH_TIME("BinaryBHLevel::specificPostTimeStep");
    if (m_p.activate_extraction == 1)
    {
        int min_level = m_p.extraction_params.min_extraction_level();
        bool calculate_weyl = at_level_timestep_multiple(min_level);
        if (calculate_weyl)
        {
            // Populate the Weyl Scalar values on the grid
            fillAllGhosts();
            BoxLoops::loop(Weyl4(m_p.extraction_params.center, m_dx),
                           m_state_new, m_state_diagnostics,
                           EXCLUDE_GHOST_CELLS);

            // Do the extraction on the min extraction level
            if (m_level == min_level)
            {
                CH_TIME("WeylExtraction");
                // Now refresh the interpolator and do the interpolation
                // fill ghosts manually to minimise communication
                bool fill_ghosts = false;
                m_gr_amr.m_interpolator->refresh(fill_ghosts);
                m_gr_amr.fill_multilevel_ghosts(
                    VariableType::diagnostic, Interval(c_Weyl4_Re, c_Weyl4_Im),
                    min_level);
                WeylExtraction my_extraction(m_p.extraction_params, m_dt,
                                             m_time, first_step,
                                             m_restart_time);
                my_extraction.execute_query(m_gr_amr.m_interpolator);
            }
        }
    }

    // do puncture tracking on requested level
    if (m_p.track_punctures == 1 && m_level == m_p.puncture_tracking_level)
    {
        CH_TIME("PunctureTracking");
        // only do the write out for every coarsest level timestep
        int coarsest_level = 0;
        bool write_punctures = at_level_timestep_multiple(coarsest_level);
        m_bh_amr.m_puncture_tracker.execute_tracking(m_time, m_restart_time, m_dt,
                                                   write_punctures);
    }

    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in specific PostTimeStep: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());

}

// Things to do before a plot level
void BinaryBHLevel::prePlotLevel()
{
    if (m_verbosity)
        pout() << "BinaryBHLevel::prePlotLevel " << m_level << endl;   

    fillAllGhosts();
    Potential potential(m_p.potential_params);
    ScalarFieldWithPotential scalar_field(potential);
    BoxLoops::loop(DensityAndMom<ScalarFieldWithPotential>(
                       scalar_field, m_dx, m_p.center, m_p.final_a),
                   m_state_new, m_state_diagnostics, EXCLUDE_GHOST_CELLS);
    // Populate the Weyl Scalar values on the grid                                                                                                                              
    BoxLoops::loop(Weyl4(m_p.center, m_dx),
                           m_state_new, m_state_diagnostics,
                           EXCLUDE_GHOST_CELLS);
    
    // Check for nan's
    if (m_p.nan_check)
        BoxLoops::loop(NanCheck("NaNCheck in prePlotLevel: "), m_state_new,
                       m_state_new, EXCLUDE_GHOST_CELLS, disable_simd());

}
