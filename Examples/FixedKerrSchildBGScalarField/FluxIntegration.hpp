/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef FLUXINTEGRATION_HPP_
#define FLUXINTEGRATION_HPP_

#include "AMRInterpolator.hpp"
#include "InterpolationQuery.hpp"
#include "SimulationParametersBase.hpp"
#include "SmallDataIO.hpp" // for writing data
#include "UserVariables.hpp" // Needs c_Weyl_Re etc <----- Weyl already computed

// pout()
#include "parstream.H"

//!  The class allows extraction of the scalar field phi in
//!  spherical shells at specified radii, and integration over those shells
/*!
    The values at each theta, phi point may then be
    written to an output file, or integrated across the surfaces.
*/

struct flux_integration_params_t
{
    std::vector<double> integration_radii;
    int num_points_phi;
    int num_points_theta;
    std::vector<int> integration_levels;
    bool write_extraction;
    int min_integration_level;
}
class FluxIntegration
{
  private:
    //! Params for integration
    const flux_integration_params_t m_params;
    const double m_bh_a; // black hole spin J/M
    const double m_dt;
    const double m_time;
    const bool m_first_step;
    const double m_restart_time;
    const int m_num_points; // number of points per integration radius
    const double m_dphi;
    const double m_dtheta;
    const std::string m_file_name; // subdirectory containing the data
    const std::string m_output_dir; // directory to save the data

  public:
    //! The constructor
    FluxIntegration(integration_params_t a_params, double a_dt, double a_time,
                   bool a_first_step, std::string a_file_name, std::string a_output_dir, double a_restart_time = 0.0)
        : m_params(a_params), m_dt(a_dt), m_time(a_time),
          m_first_step(a_first_step), m_file_name(a_file_name), m_output_dir(a_output_dir), m_restart_time(a_restart_time),
          m_num_points(m_params.num_points_phi * m_params.num_points_theta),
          m_dphi(2.0 * M_PI / m_params.num_points_phi),
          m_dtheta(0.5 * M_PI / m_params.num_points_theta)
    {
    }

    //! The old constructor which assumes it is called in specificPostTimeStep
    //! so the first time step is when m_time == m_dt
    FluxIntegration(integration_params_t a_params, double a_dt, double a_time,
                   std::string a_file_name, std::string a_output_dir, double a_restart_time = 0.0)
        : FluxIntegration(a_params, a_dt, a_time, (a_dt == a_time),
                         a_file_name, a_output_dir, a_restart_time)
    {
    }

    //! Destructor
    ~FluxIntegration() {}

    //! Execute the query
    void execute_query(int var_index, AMRInterpolator<Lagrange<4>> *a_interpolator) const;

  private:
    //! integrate over a r_KS spherical shell for each
    //! integration radius
    std::vector<double>
    integrate_surface(const std::vector<double> a_re_part) const;

    //! Write out calculated values of integral for each integration radius
    void write_integral(const std::vector<double> a_integral,
                        std::string a_filename) const;
};

#include "FluxIntegration.impl.hpp"

#endif /* FLUXINTEGRATION_HPP_ */
