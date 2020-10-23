/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef REPROCESSINGLEVEL_HPP_
#define REPROCESSINGLEVEL_HPP_

#include "parstream.H" // gives us pout()
#include "GRAMRLevel.hpp"
#include "Y00Integration.hpp"

class ReprocessingLevel : public GRAMRLevel
{
    friend class DefaultLevelFactory<ReprocessingLevel>;
    // Inherit the contructors from GRAMRLevel
    using GRAMRLevel::GRAMRLevel;

    //! Initialize data for the field and metric variables
    virtual void initialData() { m_state_new.setVal(0.); }

    //! function to do ... ?
    void postRestart()
    {
        // Add code here to do what you need it to do on each level
        //pout() << "The time is " << m_time << " on level " << m_level 
        //       << ". Your wish is my command." << endl;

	// what exactly is m_time ???
	// what is m_restart_time ???

	bool m_first_step;
	double m_true_restart_time = m_p.coarsest_dx * m_p.dt_multiplier * m_p.start_number; 	
	//pout() << "m_time = " << m_time << std::endl;
        //pout() << "m_true_restart_time = " << m_true_restart_time << std::endl;
	if ((m_time == m_true_restart_time) && (m_p.resume == 0)){
                m_first_step = 1;
        } else {
                m_first_step = 0;
        }
	
	// Do the extraction on the min integration level
        if (m_level == m_p.integration_params.min_integration_level)
        {
            // Now refresh the interpolator and do the interpolation
            m_gr_amr.m_interpolator->refresh();
            Y00Integration phi_integration(m_p.integration_params, m_dt, m_time,
                                         m_first_step, m_p.data_subdir, m_p.start_number, m_p.end_number, m_restart_time);
            phi_integration.execute_query(m_gr_amr.m_interpolator); //! <--- This routine includes performing the integration and writing the output to a file
        }		

    }

	//! RHS routines used at each RK4 step
    virtual void specificEvalRHS(GRLevelData &a_soln, GRLevelData &a_rhs,
                                 const double a_time)
    {
    }

	//! Tell Chombo how to tag cells for regridding
    virtual void computeTaggingCriterion(FArrayBox &tagging_criterion,
                                         const FArrayBox &current_state){};
};

#endif /* REPROCESSINGLEVEL_HPP_ */
