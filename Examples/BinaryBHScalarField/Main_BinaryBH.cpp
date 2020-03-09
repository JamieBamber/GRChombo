/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#include "CH_Timer.H"
#include "parstream.H" //Gives us pout()
#include <chrono>
#include <iostream>

#include "DefaultLevelFactory.hpp"
#include "BHAMR.hpp"
#include "GRParmParse.hpp"
#include "SetupFunctions.hpp"
#include "SimulationParameters.hpp"

// Problem specific includes:
#include "BinaryBHLevel.hpp"

int runGRChombo(int argc, char *argv[])
{
    // Load the parameter file and construct the SimulationParameter class
    // To add more parameters edit the SimulationParameters file.
    char *in_file = argv[1];
    GRParmParse pp(argc - 2, argv + 2, NULL, in_file);
    SimulationParameters sim_params(pp);

    pout() << "Loaded simulation parameters" << endl;

    // The line below selects the problem that is simulated
    // (To simulate a different problem, define a new child of AMRLevel
    // and an associated LevelFactory)
<<<<<<< HEAD
    BHAMR gr_amr;

    pout() << "BHAMR gr_amr line: initialised BHAMR object" << endl;
=======
    GRAMR gr_amr;

    pout() << "GRAMR gr_amr line: initialised GRAMR object" << endl;
>>>>>>> 96e6a663f72a6c60ad4e04cc5f1d7852e3e5e65e

    DefaultLevelFactory<BinaryBHLevel> binary_bh_level_fact(gr_amr, sim_params);

    pout() << "Initialised DefaultLevelFactory<BinaryBHLevel> object" << endl;

    setupAMRObject(gr_amr, binary_bh_level_fact);

    pout() << "Setup AMRObject" << endl;

    // call this after amr object setup so grids known
    // and need it to stay in scope throughout run
    AMRInterpolator<Lagrange<4>> interpolator(
        gr_amr, sim_params.origin, sim_params.dx, sim_params.verbosity);
    gr_amr.set_interpolator(&interpolator);

    pout() << "set interpolator" << endl;

    using Clock = std::chrono::steady_clock;
    using Minutes = std::chrono::duration<double, std::ratio<60, 1>>;

    std::chrono::time_point<Clock> start_time = Clock::now();

    pout() << "About to start running simulation: " << endl;

    gr_amr.run(sim_params.stop_time, sim_params.max_steps);

    auto now = Clock::now();
    auto duration = std::chrono::duration_cast<Minutes>(now - start_time);
    pout() << "Total simulation time (mins): " << duration.count() << ".\n";

    gr_amr.conclude();

    CH_TIMER_REPORT(); // Report results when running with Chombo timers.

    return 0;
}

int main(int argc, char *argv[])
{
    mainSetup(argc, argv);

    int status = runGRChombo(argc, argv);

    if (status == 0)
        pout() << "GRChombo finished." << std::endl;
    else
        pout() << "GRChombo failed with return code " << status << std::endl;

    mainFinalize();
    return status;
}
