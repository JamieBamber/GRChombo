/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef USERVARIABLES_HPP
#define USERVARIABLES_HPP

// assign an enum to each variable
enum
{
    c_phi, // matter field added
    c_Pi,  //(minus) conjugate momentum
    c_chi,
    c_rho,
    c_J_azimuth, 
    c_J_r,
    c_J_azimuth_r,
    NUM_VARS
};

namespace UserVariables
{
static constexpr char const *variable_names[NUM_VARS] = {"phi", "Pi", "chi",
                                                         "rho", "J_azimuth", "J_r", "J_azimuth_r"};
}

#endif /* USERVARIABLES_HPP */
