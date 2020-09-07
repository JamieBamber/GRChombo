/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes

#include "GRParmParse.hpp"
#include "SimulationParametersBase.hpp"

// Problem specific includes:
#include "BoostedBH.hpp"
#include "ScalarPotential.hpp"
#include "FlatScalar.hpp"

class SimulationParameters : public SimulationParametersBase
{
  public:
    SimulationParameters(GRParmParse &pp) : SimulationParametersBase(pp)
    {
	pout() << "@@@@@ start SimulationParameters::readParams(pp)" << endl;
        readParams(pp);
    }

    /// Read parameters from the parameter file
    void readParams(GRParmParse &pp)
    {
    	// Initial and SF data
        pp.load("G_Newton", G_Newton, 0.0);
        pp.load("scalar_mass", potential_params.scalar_mass);
        pp.load("field_amplitude", initial_params.field_amplitude);
    	
        // Initial data
        pp.load("massA", bh1_params.mass);
        pp.load("momentumA", bh1_params.momentum);
        pp.load("massB", bh2_params.mass);
        pp.load("momentumB", bh2_params.momentum);

        // Get the centers of the BHs either explicitly or as
        // an offset (not both, or they will be offset from center
        // provided)
        std::array<double, CH_SPACEDIM> offsetA, offsetB;
        pp.load("offsetA", offsetA, {0.0, 0.0, 0.0});
        pp.load("offsetB", offsetB, {0.0, 0.0, 0.0});

	// scale to achieve desired seperation
	double base_seperation_squared = 0;
	FOR1(idir){
	base_seperation += pow((offsetA[idir]-offsetB[idir]),2); 
	}
	double base_seperation = sqrt(base_seperation_squared);
	double desired_sep;
	pp.load("desired_seperation", desired_sep);
	double scaling = desired_sep/base_seperation;
	
        std::array<double, CH_SPACEDIM> centerA, centerB;
        pp.load("centerA", centerA, center);
        pp.load("centerB", centerB, center);
        FOR1(idir)
        {
            bh1_params.center[idir] = centerA[idir] + scaling*offsetA[idir];
            bh2_params.center[idir] = centerB[idir] + scaling*offsetB[idir];
            bh1_params.momentum[idir] = scaling*bh1_params.momentum[idir];
            bh2_params.momentum[idir] = scaling*bh2_params.momentum[idir];
	}
	bh1_params.mass = scaling*bh1_params.mass;
	bh2_params.mass = scaling*bh2_params.mass;

        // Do we want Weyl extraction and puncture tracking?
        pp.load("activate_extraction", activate_extraction, false);
        pp.load("track_punctures", track_punctures, false);

        // hard code num punctures to 2 for now
        int num_punctures = 2;
        initial_puncture_coords.resize(num_punctures);
        initial_puncture_coords[0] = bh1_params.center;
        initial_puncture_coords[1] = bh2_params.center;
	pout() << "@@@@@ Finished SimulationParameters: readParams(pp)" << endl;
    }

    // Initial data
    bool activate_extraction, track_punctures;
    std::vector<std::array<double, CH_SPACEDIM>> initial_puncture_coords;
    double G_Newton;
    FlatScalar::params_t initial_params;
    ScalarPotential::params_t potential_params;
    
    // Collection of parameters necessary for initial conditions
    BoostedBH::params_t bh2_params;
    BoostedBH::params_t bh1_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
