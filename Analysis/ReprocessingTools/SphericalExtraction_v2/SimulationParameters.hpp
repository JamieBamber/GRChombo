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

// numpy tools
#include "numpy_tools.hpp"

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
	// steup first step
	first_step = 1;

     	// get directories
        pp.get("data_rootdir", data_rootdir);
        pp.get("data_subdir", data_subdir);
        pp.get("output_rootdir", output_rootdir);

        // Files setup
        pp.get("plot_interval", plot_interval);
        pp.get("start_number", start_number);
        pp.get("end_number", end_number);
        
       	// basic extraction params
        dx.fill(coarsest_dx);
        origin.fill(coarsest_dx / 2.0);
        //pout() << "coarsest_dx = " << coarsest_dx << endl;

	pp.get("num_extraction_radii", extraction_params.num_extraction_radii);

	// -- make integration radius array
	if (pp.contains("min_integration_radius") && pp.contains("max_integration_radius")) {
		pp.load("linear_or_log", linear_or_log, true);
		pp.load("min_integration_radius", min_integration_radius);
		pp.load("max_integration_radius", max_integration_radius);
		if (linear_or_log) {
			extraction_params.extraction_radii = 
			NumpyTools::linspace(min_integration_radius, max_integration_radius, extraction_params.num_extraction_radii);
		} else {
			extraction_params.extraction_radii = 
                        NumpyTools::logspace(min_integration_radius, max_integration_radius, extraction_params.num_extraction_radii);
		}	
		pout() << "extraction_params.extraction_radii = " << std::endl;
			for(std::vector<double>::const_iterator i = extraction_params.extraction_radii.begin(); i != extraction_params.extraction_radii.end(); ++i){
				pout() << std::to_string(*i) << std::endl;
			}
		pout() << "end of radii list" << std::endl;
	}
	if (pp.contains("integration_radius"))
	{
            pp.load("integration_radius", extraction_params.extraction_radii, 1,
                    0.1);
        }
	
	// load suffix
	if (pp.contains("suffix"))
        {
		pp.get("suffix", suffix);
	} else {
		suffix = "";
	}

    }

  int plot_interval, start_number, end_number, first_number;
  //std::array<double, CH_SPACEDIM> origin,
  //     dx; // location of coarsest origin and dx
  string data_rootdir, data_subdir, suffix, output_rootdir;
  double min_integration_radius, max_integration_radius;
  bool linear_or_log, first_step;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
