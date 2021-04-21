/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes
#include "GRParmParse.hpp"
#include "ChomboParameters.hpp"
#include "FixedBGSimulationParametersBase.hpp"

// pout()
#include "parstream.H" 

class SimulationParameters : public FixedBGSimulationParametersBase
{
  public:
    SimulationParameters(GRParmParse &pp) : FixedBGSimulationParametersBase(pp)
    {
     	// read the problem specific params
        readParams(pp);
    }

    void readParams(GRParmParse &pp)
    {
	// get directories
	pp.get("data_rootdir", data_rootdir);
	pp.get("data_subdir", data_subdir);
	pp.get("output_rootdir", output_rootdir);
	pp.get("suffix", suffix);

        // Files setup
        pp.get("plot_interval", plot_interval);
	pp.get("start_number", start_number);
	pp.get("end_number", end_number);

        // basic extraction params
        //dx.fill(coarsest_dx);
        //origin.fill(coarsest_dx / 2.0);
	//pout() << "coarsest_dx = " << coarsest_dx << endl;
    }

    int plot_interval, start_number, end_number;
  //std::array<double, CH_SPACEDIM> origin,
  //     dx; // location of coarsest origin and dx
    string data_rootdir, data_subdir, suffix, output_rootdir;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
