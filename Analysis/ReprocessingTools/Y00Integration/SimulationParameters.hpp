/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes
#include "GRParmParse.hpp"
#include "ChomboParameters.hpp"

// numpy tools
#include "numpy_tools.hpp"

// pout()
#include "parstream.H" 

struct integration_params_t
{
    int num_integration_radii;
    double min_integration_radius;
    double max_integration_radius;
    std::vector<double> integration_radii;
    std::array<double, CH_SPACEDIM> integration_center;
    int num_points_phi;
    int num_points_theta;
    double theta_min, theta_max; // min and max theta values in units of pi/2
    std::vector<int> integration_levels;
    bool write_extraction;
    bool linear_or_log;
    std::string suffix = "";
    int min_integration_level;
    int variable_index; // index of the variable to integrate in the array of User Variables
};

class SimulationParameters : public ChomboParameters
{
  public:
    // For the Interpolator test we don't need many parameters
    SimulationParameters(GRParmParse &pp) : ChomboParameters(pp)
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

        // Files setup
        pp.get("end_number", end_number);
        pp.get("start_number", start_number);
        pp.get("plot_interval", plot_interval);

        // basic integration params
        dx.fill(coarsest_dx);
        origin.fill(coarsest_dx / 2.0);

	// integration parameters
	pp.load("variable_index", integration_params.variable_index);
	pp.load("num_points_phi", integration_params.num_points_phi, 2);
        pp.load("num_points_theta", integration_params.num_points_theta, 4);
	pp.load("theta_min", integration_params.theta_min);
        pp.load("theta_max", integration_params.theta_max);
	pp.load("integration_center", integration_params.integration_center,
                {0.5 * L, 0.5 * L, 0});

	// radii parameters
        pp.load("num_integration_radii", integration_params.num_integration_radii,
                1);
        if (pp.contains("integration_levels"))
        {
            pp.load("integration_levels", integration_params.integration_levels,
                    integration_params.num_integration_radii);
        }
	else
	{
            pp.load("integration_level", integration_params.integration_levels, 1,
                    0);
        }
	// -- explicit integration radii
	if (pp.contains("integration_radii")) // Check for multiple integration radii, otherwise load single radius/level (for backwards compatibility).
        {
            pp.load("integration_radii", integration_params.integration_radii,
                    integration_params.num_integration_radii);
        }
	// -- make integration radius array
	if (pp.contains("min_integration_radius") && pp.contains("max_integration_radius")) {
		pp.load("linear_or_log", integration_params.linear_or_log, true);
		pp.load("min_integration_radius", integration_params.min_integration_radius);
		pp.load("max_integration_radius", integration_params.max_integration_radius);
		if (integration_params.linear_or_log) {
			integration_params.integration_radii = 
			NumpyTools::linspace(integration_params.min_integration_radius, integration_params.max_integration_radius, integration_params.num_integration_radii);
		} else {
			integration_params.integration_radii = 
                        NumpyTools::logspace(integration_params.min_integration_radius, integration_params.max_integration_radius, integration_params.num_integration_radii);
			pout() << "integration_params.integration_radii = " << std::endl;
			for(std::vector<double>::const_iterator i = integration_params.integration_radii.begin(); i != integration_params.integration_radii.end(); ++i){
				pout() << std::to_string(*i) << std::endl;
			}
			pout() << "end of radii list" << std::endl;
		}	
	}
	if (pp.contains("integration_radius"))
	{
            pp.load("integration_radius", integration_params.integration_radii, 1,
                    0.1);
        }
	
	// load suffix
        if (pp.contains("suffix"))
        {
                pp.get("suffix", integration_params.suffix);
        } else {
                integration_params.suffix = "";
        }

	pp.load("write_extraction", integration_params.write_extraction, false);

        // Work out the minimum integration level
        auto min_integration_level_it =
            std::min_element(integration_params.integration_levels.begin(),
                             integration_params.integration_levels.end());
        integration_params.min_integration_level = *(min_integration_level_it);
    }

    int start_number, end_number, plot_interval;
    std::array<double, CH_SPACEDIM> origin,
        dx; // location of coarsest origin and dx
    std::string data_subdir;
    std::string data_rootdir;
    std::string output_rootdir;

    bool linear_or_log;

   integration_params_t integration_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
