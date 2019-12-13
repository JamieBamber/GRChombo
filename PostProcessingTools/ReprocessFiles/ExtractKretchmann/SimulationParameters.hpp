/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef SIMULATIONPARAMETERS_HPP_
#define SIMULATIONPARAMETERS_HPP_

// General includes
#include "ChomboParameters.hpp"
#include "GRParmParse.hpp"
#include "OscillotonPotential.hpp"

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
        // Grid setup
        pp.get("num_files", num_files);
        pp.get("start_file", start_file);
        pp.get("checkpoint_interval", checkpoint_interval);

        // extraction params
        dx.fill(coarsest_dx);
        origin.fill(coarsest_dx / 2.0);

        // scalar stuff
        pp.load("scalar_mass", potential_params.scalar_mass);
        pp.load("f_axion", potential_params.f_axion, 0.0);
    }

    int num_files, start_file, checkpoint_interval;
    std::array<double, CH_SPACEDIM> origin,
        dx; // location of coarsest origin and dx
    OscillotonPotential::params_t potential_params;
};

#endif /* SIMULATIONPARAMETERS_HPP_ */
