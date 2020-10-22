/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes
#include "ChomboParameters.hpp"
#include "GRParmParse.hpp"

// Problem specific includes:
#include "KerrSchildFixedBG.hpp"
#include "Potential.hpp"
#include "ScalarRotatingCloud.hpp"
#include "KerrSchildSpheroidalExtraction.hpp"

class SimulationParameters : public ChomboParameters
{
  public:
    SimulationParameters(GRParmParse &pp) : ChomboParameters(pp)
    {
        // read the problem specific params
        readParams(pp);
    }

    void readParams(GRParmParse &pp)
    {
        // for nan check
        pp.load("nan_check", nan_check, 1);

        // Initial and SF data
        pp.load("scalar_mass", potential_params.scalar_mass);
        pp.load("scalar_amplitude", initial_params.amplitude); 
        pp.load("center", initial_params.center, center);
	pp.load("scalar_omega", initial_params.omega);
	pp.load("scalar_l", initial_params.l);
	pp.load("scalar_m", initial_params.m);
	pp.load("alignment", initial_params.alignment);
        pp.load("sigma", sigma);
	
        // Background boosted bh data
        pp.load("bh_mass", bg_params.mass);
	pp.load("bh_spin", bg_params.spin);
        bg_params.center = initial_params.center;

	// Flux Extraction params
	extraction_params.num_extraction_radii = 2;
	pp.load("num_points_phi", extraction_params.num_points_phi, 2);
        pp.load("num_points_theta", extraction_params.num_points_theta, 5);
	extraction_params.a = bg_params.mass*bg_params.spin;
	pp.load("outer_extraction_radius", outer_extraction_radius);
	double r_plus = bg_params.mass*(1 + sqrt(1 - bg_params.spin*bg_params.spin));
	std::vector<double> flux_radii = {r_plus, outer_extraction_radius};
	extraction_params.extraction_radii = flux_radii;
	pp.load("extraction_center", extraction_params.center, center);
	pp.load("write_extraction", extraction_params.write_extraction, false);
	pp.load("flux_data_dir", flux_data_dir);
	string data_subdir;
	pp.load("data_subdir", data_subdir);
	flux_file_name = flux_data_dir + data_subdir + "_mass_ang_mom_flux.csv";
    }

    // Problem specific parameters
    double sigma;
    int nan_check;
    double outer_extraction_radius;

    // Initial data for matter, metric and potential
    KerrSchildFixedBG::params_t bg_params;
    ScalarRotatingCloud::params_t initial_params;
    Potential::params_t potential_params;
    KSSpheroidalExtraction::params_t extraction_params;
    string flux_data_dir;
    string flux_file_name;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
