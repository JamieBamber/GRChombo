/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef REPROCESSINGLEVEL_HPP_
#define REPROCESSINGLEVEL_HPP_

#include "BoxLoops.hpp"
#include "ComputePack.hpp"
#include "CustomExtraction.hpp"
#include "GRAMRLevel.hpp"
#include "OscillotonPotential.hpp"
#include "ScalarField.hpp"
#include "SetValue.hpp"
// Problem specific includes
#include "CustomExtraction.hpp"
#include "KretchmannScalar.hpp"

class ReprocessingLevel : public GRAMRLevel
{
    friend class DefaultLevelFactory<ReprocessingLevel>;
    // Inherit the contructors from GRAMRLevel
    using GRAMRLevel::GRAMRLevel;

    // Typedef for scalar field
    typedef ScalarField<OscillotonPotential> ScalarFieldWithPotential;

    // initialize data
    virtual void initialData() { m_state_new.setVal(0.); }

    void postRestart()
    {
        // Add code here to do what you need it to do on each level
        if (m_level == 0)
        {
            pout() << m_time << "  ";
        }

        // assign kretchmann values
        fillAllGhosts();
        OscillotonPotential potential(m_p.potential_params);
        ScalarFieldWithPotential scalar_field(potential);
        BoxLoops::loop(
            KretchmannScalar<ScalarFieldWithPotential>(scalar_field, m_dx),
            m_state_new, m_state_new, SKIP_GHOST_CELLS);

        if (m_level == 7 && m_time > 0)
        {
            // Now refresh the interpolator and do the extraction of phi
            m_gr_amr.m_interpolator->refresh();
            int num_points = 200;
            int var1 = c_rho;
            CustomExtraction my_extraction1(var1, num_points, m_p.L, m_p.center,
                                            m_dt, m_time);
            my_extraction1.execute_query(m_gr_amr.m_interpolator,
                                         "KretchmannVsR_Mmu1.0NR.txt");
        }
    }

    virtual void specificEvalRHS(GRLevelData &a_soln, GRLevelData &a_rhs,
                                 const double a_time)
    {
    }

    virtual void computeTaggingCriterion(FArrayBox &tagging_criterion,
                                         const FArrayBox &current_state){};
};

#endif /* REPROCESSINGLEVEL_HPP_ */
