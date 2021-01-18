/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef DIAGNOSTICVARIABLES_HPP
#define DIAGNOSTICVARIABLES_HPP

// assign an enum to each variable
enum
{
 /*    c_rho,
    c_rho_azimuth,
    c_J_R,
    c_J_azimuth_R,*/

    NUM_DIAGNOSTIC_VARS
};

namespace DiagnosticVariables
{
static const std::array<std::string, NUM_DIAGNOSTIC_VARS> variable_names = {
									    // "rho",	"rho_azimuth",  "J_R",  "J_azimuth_R"
    
    };
}

#endif /* DIAGNOSTICVARIABLES_HPP */
