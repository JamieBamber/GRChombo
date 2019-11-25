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
#include "IsotropicKerrFixedBG.hpp"
#include "Potential.hpp"
#include "ScalarRotatingCloud.hpp"

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
	double field_amplitude =				// Set the field amplitude such that for an input amplitude of 1
        initial_params.amplitude *				// 1/2 * mu^2 * phi^2 = e^-10
        sqrt(1e-10 / (0.5 * potential_params.scalar_mass *	//
                      potential_params.scalar_mass));		//
        pp.load("scalar_amplitude", field_amplitude);       	//
        pp.load("scalar_width", initial_params.width);		
        pp.load("scalar_center", initial_params.center, center);
	pp.load("scalar_omega", initial_params.omega);
	pp.load("scalar_l", initial_params.l);
	pp.load("scalar_m", initial_params.m);
        pp.load("sigma", sigma);

        // Background boosted bh data
        pp.load("bh_mass", bg_params.mass);
	pp.load("bh_spin", bg_params.spin);
        //pp.load("bh_center", bg_params.center, center);
    }

    // Problem specific parameters
    double sigma;
    int nan_check;

    // Initial data for matter, metric and potential
    IsotropicKerrFixedBG::params_t bg_params;
    ScalarRotatingCloud::params_t initial_params;
    Potential::params_t potential_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
