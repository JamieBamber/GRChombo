/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef KERRSCHILDFLUXEXTRACTION_HPP_
#define KERRSCHILDFLUXEXTRACTION_HPP_

#include "KerrSchildSpheroidalExtraction.hpp"
//!  The class allows extraction of the values of the flux components on
//!  Kerr Schild spheroidal shells at specified radii, and integration over those shells
/*!
   The class allows the user to extract data from the grid for the flux
   components over spheroidal shells at specified radii. The values may then be
   written to an output file, or integrated across the surfaces.
*/
class KSFluxExtraction : public KSSpheroidalExtraction
{
  public:
    //! The constructor
    KSFluxExtraction(KSSpheroidalExtraction::params_t &a_params, double a_dt,
                   double a_time, bool a_first_step, string a_file_name,
                   double a_restart_time = 0.0)
        : KSSpheroidalExtraction(a_params, a_dt, a_time, a_first_step,
                              a_restart_time), m_file_name(a_file_name)
    {
        std::vector<int> vars = {c_J_rKS, c_J_azimuth_rKS};
        add_vars(vars);
    }

    //! The old constructor which assumes it is called in specificPostTimeStep
    //! so the first time step is when m_time == m_dt
    KSFluxExtraction(KSSpheroidalExtraction::params_t a_params, double a_dt,
                   double a_time, string a_file_name, double a_restart_time = 0.0)
        : KSSpheroidalExtraction(a_params, a_dt, a_time, (a_dt == a_time),
                         a_restart_time), m_file_name(a_file_name)
    {
    }

    // the references of the vars as used in the integrator
    enum M_VARS {m_J_rKS, m_J_azimuth_rKS};

    //! Execute the query
    void execute_query(AMRInterpolator<Lagrange<4>> *a_interpolator)
    {
        // extract the values of the Flux scalars on the spheres
        pout() << "starting query" << endl;
	extract(a_interpolator);
	pout() << "done extraction from interpolator" << endl;

        // this would write out the values at every point on the sphere
        if (m_params.write_extraction)
        {
            write_extraction("Flux4ExtractionOut_");
        }

        // Setup to integrate J_rKS and J_azimuth_rKS
        std::vector<std::vector<double>> flux_integrals(2);
	pout() << "made flux integrals vector" << endl;
	pout() << "m_J_rKS = " << m_J_rKS << endl;
        add_var_integrand(m_J_rKS, flux_integrals[m_J_rKS], 
                                  IntegrationMethod::simpson);
        add_var_integrand(m_J_azimuth_rKS, flux_integrals[m_J_azimuth_rKS], 
                                  IntegrationMethod::simpson);
	pout() << "added the integrand variables" << endl;

        // do the integration over the surface
        integrate();
	pout() << "done integration" << endl;

        // write the integrals
	pout() << "starting writing the integrals" << endl;
        std::vector<std::string> labels(2);
        labels[m_J_rKS] = "J_rKS";
        labels[m_J_azimuth_rKS] = "J_azimuth_rKS";
        write_integrals(m_file_name, flux_integrals, labels);
    }

    // file name
    string m_file_name;
};

#endif /* KERRSCHILDFLUXEXTRACTION_HPP_ */
