/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef USERVARIABLES_HPP
#define USERVARIABLES_HPP

#include "DiagnosticVariables.hpp"
#include <array>
#include <string>

// assign an enum to each variable
enum
{
    c_phi_Re, // matter field added
    c_chi,    // the conformal factor of the metric, not evolved

    c_rho,    // the energy density of the SF                                                                                                                   
    c_rhoJ,   // the energy density of the SF                                                                                                                   
    c_Edot,   // the energy density of the SF                                                                                                                   
    c_Jdot,   // the energy density of the SF
    NUM_VARS
};

namespace UserVariables
{
static const std::array<std::string, NUM_VARS> variable_names = {
								 "phi_Re", "chi", "rho", "rhoJ", "Edot", "Jdot"};
}

#include "UserVariables.inc.hpp"

#endif /* USERVARIABLES_HPP */
