/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes
#include "GRParmParse.hpp"
#include "ChomboParameters.hpp"

// pout()
#include "parstream.H" 

// specific includes
#include "KerrSchildSpheroidalExtraction.hpp"

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
	pp.get("flux_data_dir", flux_data_dir);
	pp.get("data_subdir", data_subdir);

        // Files setup
        pp.get("plot_interval", plot_interval);
	pp.get("start_number", start_number);
	pp.get("end_number", end_number);
        pp.get("plot_interval", plot_interval);

        // basic extraction params
        dx.fill(coarsest_dx);
        origin.fill(coarsest_dx / 2.0);

	// extraction parameters
	pp.load("num_points_phi", extraction_params.num_points_phi, 32);
        pp.load("num_points_theta", extraction_params.num_points_theta, 33);
	pp.load("extraction_center", extraction_params.extraction_center,
                {0.5 * L, 0.5 * L, 0});

	// BH parameters
	double bh_spin, bh_mass;
        pp.load("bh_spin", bh_spin);
        pp.load("bh_mass", bh_mass);
        extraction_params.a = bh_mass * bh_spin;

	// Extraction parameters
	double outer_extraction_radius;
	pp.load("outer_extraction_radius", outer_extraction_radius);
        double r_plus = bh_mass*(1 + sqrt(1 - bh_spin*bh_spin));
        std::vector<double> flux_radii = {r_plus, outer_extraction_radius};
        extraction_params.extraction_radii = flux_radii;	
	pp.load("write_extraction", extraction_params.write_extraction, false);
	// Check for multiple extraction radii, otherwise load single
        // radius/level (for backwards compatibility).
	if (pp.contains("extraction_levels"))
        {
            pp.load("extraction_levels", extraction_params.extraction_levels,
                    extraction_params.num_extraction_radii);
        }
        else
        {
            pp.load("extraction_level", extraction_params.extraction_levels, 1,
                    0);
        }
	flux_file_name = flux_data_dir + data_subdir + "_flux_v1.dat";
    }

    int plot_interval, start_number, end_number;
    std::array<double, CH_SPACEDIM> origin,
        dx; // location of coarsest origin and dx
    std::string data_subdir;
    std::string data_rootdir;
    std::string flux_data_dir;
    std::string flux_file_name;
    KSSpheroidalExtraction::params_t extraction_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
