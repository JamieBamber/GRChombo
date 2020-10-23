/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef DIAGNOSTICVARIABLES_HPP
#define DIAGNOSTICVARIABLES_HPP

// assign an enum to each variable
enum
{
    c_phi,
    c_Pi,

    c_rho,
    c_rho_azimuth,
    c_J_R,
    c_J_azimuth_R,

    c_Ham,

    c_Mom1,
    c_Mom2,
    c_Mom3,

    c_Weyl4_Re,
    c_Weyl4_Im,

    NUM_DIAGNOSTIC_VARS
};

namespace DiagnosticVariables
{
static const std::array<std::string, NUM_DIAGNOSTIC_VARS> variable_names = {
    "phi",	"Pi",

    "rho",	"rho_azimuth",  "J_R",  "J_azimuth_R",

    "Ham",

    "Mom1",     "Mom2",    "Mom3",

    "Weyl4_Re", "Weyl4_Im"};
}

#endif /* DIAGNOSTICVARIABLES_HPP */
