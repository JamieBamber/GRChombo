/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef USERVARIABLES_HPP
#define USERVARIABLES_HPP

// plot_vars = chi phi Pi rho rho_azimuth J_R J_azimuth_R

// assign an enum to each variable
enum
{
    c_chi,
    c_phi, // matter field added
    c_Pi,  //(minus) conjugate momentum
    c_rho,
    c_rho_azimuth,
    c_J_R,
    c_J_azimuth_R,
    NUM_VARS
};

namespace UserVariables
{
static constexpr char const *variable_names[NUM_VARS] = {"chi", "phi", "Pi",
                                                         "rho", "rho_azimuth", 
							"J_R", "J_azimuth_R"};
}

#endif /* USERVARIABLES_HPP */
