/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef USERVARIABLES_HPP
#define USERVARIABLES_HPP

/// This enum gives the index of every variable stored in the grid
enum
{
    c_chi,
    c_phi,
    c_rho,
    c_S_azimuth,
    c_S_r,
    c_Weyl4_Re,
    c_Weyl4_Im,

    NUM_VARS
};

namespace UserVariables
{
static constexpr char const *variable_names[NUM_VARS] = {
    "chi",

    "phi",

    "rho",	"S_azimuth",	"S_r",

    "Weyl4_Re", "Weyl4_Im"};
}

#endif /* USERVARIABLES_HPP */
