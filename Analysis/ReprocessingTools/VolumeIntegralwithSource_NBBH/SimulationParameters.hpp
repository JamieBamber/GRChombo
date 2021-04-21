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

struct integration_params_t
{
    double min_integration_radius;
    double max_integration_radius;
    std::array<double, CH_SPACEDIM> integration_center;
    std::vector<int> integration_levels;
    int min_integration_level;
    double M;	// BH mass (assume equal mass BHs)
    double d;   // BH separation
};

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
	pp.get("output_rootdir", output_rootdir);
	pp.get("data_subdir", data_subdir);
	pp.get("suffix", suffix);

        // Files setup
        pp.get("end_number", end_number);
        pp.get("start_number", start_number);
        pp.get("plot_interval", plot_interval);
	pp.get("first_number", first_number); // the first file number
	
        // basic integration params
        dx.fill(coarsest_dx);
        origin.fill(coarsest_dx / 2.0);

	// integration parameters
	pp.load("integration_center", integration_params.integration_center,
                {0.5 * L, 0.5 * L, 0});
	pp.load("half_box", half_box);

	// BH parameters
	pp.load("min_integration_radius", integration_params.min_integration_radius);
        pp.load("max_integration_radius", integration_params.max_integration_radius);
        pp.load("integration_level", integration_params.integration_levels, 1,0);
	pp.load("bh_mass", integration_params.M);
	pp.load("bh_separation", integration_params.d);
	
        // Work out the minimum integration level
        auto min_integration_level_it =
            std::min_element(integration_params.integration_levels.begin(),
                             integration_params.integration_levels.end());
        integration_params.min_integration_level = *(min_integration_level_it);
    }

    bool half_box; // are we using a half box ?

  int start_number, end_number, input_plot_interval, first_number;
    std::array<double, CH_SPACEDIM> origin,
        dx; // location of coarsest origin and dx
    std::string data_subdir;
    std::string data_rootdir;
    std::string output_rootdir;
    std::string suffix;

   integration_params_t integration_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
