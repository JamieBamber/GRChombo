/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef Y00INTEGRATION_HPP_
#define Y00INTEGRATION_HPP_

#include "AMRInterpolator.hpp"
#include "InterpolationQuery.hpp"
#include "Lagrange.hpp"
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
class Y00Integration
{
  private:
    //! Params for integration
    const integration_params_t m_params;
    const double m_dt;
    const double m_time;
    const bool m_first_step;
    const double m_restart_time;
    const int m_num_points; // number of points per integration radius
    const double m_dphi;
    const double m_dtheta;
    const double m_start_number, m_end_number;
    const std::string m_data_subdir; // subdirectory containing the data

  public:
    //! The constructor
    Y00Integration(integration_params_t a_params, double a_dt, double a_time,
                   bool a_first_step, std::string a_data_subdir, int a_start_number, int a_end_number,
		   double a_restart_time = 0.0)
        : m_params(a_params), m_dt(a_dt), m_time(a_time),
          m_first_step(a_first_step), m_data_subdir(a_data_subdir), m_restart_time(a_restart_time),
	  m_start_number(a_start_number), m_end_number(a_end_number),
          m_num_points(m_params.num_points_phi * m_params.num_points_theta),
          m_dphi(2.0 * M_PI / m_params.num_points_phi),
          m_dtheta(0.5 * M_PI / m_params.num_points_theta)
    {
    }

    //! The old constructor which assumes it is called in specificPostTimeStep
    //! so the first time step is when m_time == m_dt
    Y00Integration(integration_params_t a_params, double a_dt, double a_time,
                   std::string a_data_subdir, int a_start_number, int a_end_number, 
		   double a_restart_time = 0.0)
        : Y00Integration(a_params, a_dt, a_time, (a_dt == a_time),
                         a_data_subdir, a_start_number, a_end_number, a_restart_time)
    {
    }

    //! Destructor
    ~Y00Integration() {}

    //! Execute the query
    void execute_query(AMRInterpolator<Lagrange<4>> *a_interpolator) const;

  private:
    //! integrate over a spherical shell with given harmonics for each
    //! integration radius and normalise by multiplying by radius
    std::vector<double>
    integrate_surface(const std::vector<double> a_re_part) const;

    //! Write out calculated values of integral for each integration radius
    void write_integral(const std::vector<double> a_integral,
                        std::string a_filename) const;

    //! Write out the result of the integration in phi and theta at each timestep
    //! for each integration radius
    void write_extraction(std::string a_file_prefix, int var,
                          const std::vector<double> a_re_part) const;
};

#include "Y00Integration.impl.hpp"

#endif /* Y00INTEGRATION_HPP_ */
