/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef REPROCESSINGLEVEL_HPP_
#define REPROCESSINGLEVEL_HPP_

#include "parstream.H" // gives us pout()
#include "GRAMRLevel.hpp"
#include "KerrSchildFluxExtraction.hpp"

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
	pout() << "m_time = " << m_time << std::endl;
        pout() << "m_true_restart_time = " << m_true_restart_time << std::endl;
        if (m_time == m_true_restart_time){
		m_first_step = 1;
	} else {
		m_first_step = 0;
	}
	
	// Do the extraction on the min extraction level
        if (m_level == m_p.extraction_params.min_extraction_level())
        {
	 
            // Now refresh the interpolator and do the interpolation
            m_gr_amr.m_interpolator->refresh();
            KSFluxExtraction my_extraction(m_p.extraction_params, m_dt, m_time, m_p.flux_file_name,
                                        m_restart_time);
            my_extraction.execute_query(m_gr_amr.m_interpolator); 
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
