/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef USERVARIABLES_HPP
#define USERVARIABLES_HPP

// plot_vars = phi Pi chi rho rho_azimuth J_rKS J_azimuth_rKS J_R J_azimuth_R

// assign an enum to each variable
enum
{
    c_phi, // matter field added
    c_Pi,  //(minus) conjugate momentum
    c_chi,
    c_rho,
    c_rho_azimuth,
    c_J_rKS,
    c_J_azimuth_rKS,
    c_J_R,
    c_J_azimuth_R,
    NUM_VARS
};

namespace UserVariables
{
static constexpr char const *variable_names[NUM_VARS] = {"phi", "Pi", "chi",
                                                         "rho", "rho_azimuth", 
							 "J_rKS", "J_azimuth_rKS", 
							"J_R", "J_azimuth_R"};
}

#endif /* USERVARIABLES_HPP */
