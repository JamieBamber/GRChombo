/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef REPROCESSINGLEVEL_HPP_
#define REPROCESSINGLEVEL_HPP_

#include "parstream.H" // gives us pout()
#include "BoxLoops.hpp"
#include "ComputePack.hpp"
#include "GRAMRLevel.hpp"
#include "SimulationParametersBase.hpp"
#include "SmallDataIO.hpp"
#include "BoundedDensities.hpp"

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

	bool m_first_step;
	double m_true_restart_time = m_p.coarsest_dx * m_p.dt_multiplier * m_p.start_number; 	
	pout() << "m_time = " << m_time << std::endl;
        pout() << "m_true_restart_time = " << m_true_restart_time << std::endl;
        if (m_time == m_true_restart_time){
		m_first_step = 1;
	} else {
		m_first_step = 0;
	}

	fillAllGhosts();
	// set densities to zero outside the integration region
	BoxLoops::loop(
            BoundedDensities(m_p.integration_params, m_dx, m_p.center),
            m_state_new, m_state_new, EXCLUDE_GHOST_CELLS);	
	
	// Do the extraction on the min integration level
        if (m_level == 7)
        {
	    // Now refresh the interpolator and perform the integration
            m_gr_amr.m_interpolator->refresh();
	    double rho_sum = m_gr_amr.compute_sum(c_rho, m_p.coarsest_dx);
            double rho_J_sum = m_gr_amr.compute_sum(c_rho_azimuth, m_p.coarsest_dx);

	    int r_max = (int)(m_p.integration_params.max_integration_radius+0.5);
	    std::string mass_filename = m_p.output_rootdir + m_p.data_subdir + "_mass_in_r=" + std::to_string(r_max) + "_chombo";
	    std::string J_filename = m_p.output_rootdir + m_p.data_subdir + "_ang_mom_in_r=" + std::to_string(r_max) + "_chombo";
            
	    // write out the integrals
	    write_integral(rho_sum, mass_filename, m_first_step);
	    write_integral(rho_J_sum, J_filename, m_first_step);
        }		

    }

    void write_integral(double a_integral, std::string a_filename, bool m_first_step) const
    {
	// open file for writing
	SmallDataIO integral_file(a_filename, m_dt, m_time, m_restart_time,
                        	SmallDataIO::APPEND, m_first_step);
	
	pout() << "attempting to write integral" << std::endl;
	// remove any duplicate data if this is a restart
	integral_file.remove_duplicate_time_data();
	
	// need to write headers if this is the first timestep
	if (m_first_step)
	{
     		pout() << "making headers ... " << std::endl;
		// r header string        	
	        std::ostringstream r_header;
        	r_header << "integral inside " << m_p.integration_params.min_integration_radius << " < r < " << m_p.integration_params.max_integration_radius;

		// make header strings
        	std::vector<std::string> headers = {r_header.str()};
        	integral_file.write_header_line(headers, "t");
	}
	
	// make vector of data for writing
	std::vector<double> data_for_writing(1);
        data_for_writing[0] = a_integral;
	
	// write data
	pout() << "writing data ... " << std::endl;
	integral_file.write_time_data_line(data_for_writing);
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
