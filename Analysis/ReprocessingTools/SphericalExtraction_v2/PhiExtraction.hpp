/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef PHIEXTRACTION_HPP_
#define PHIEXTRACTION_HPP_

#include "SphericalExtraction.hpp"

// pout()
// #include "parstream.H"

//!  The class allows extraction of the scalar field phi in
//!  spherical shells at specified radii, and integration over those shells
/*!
    The values at each theta, phi point may then be
    written to an output file, or integrated across the surfaces.
*/
class PhiExtraction : public SphericalExtraction
{
  private:
	string m_output_root_dir, m_data_subdir, m_suffix;
  public:
    //! The constructor
    PhiExtraction(SphericalExtraction::params_t &a_params, 
                        string a_output_root_dir, string a_data_subdir, string a_suffix, 
                    double a_dt,
                    double a_time, bool a_first_step,
                    double a_restart_time = 0.0)
        : SphericalExtraction(a_params, a_dt, a_time, a_first_step,
                               a_restart_time), 
                                m_output_root_dir(a_output_root_dir), m_data_subdir(a_data_subdir), m_suffix(a_suffix)
    {
	add_var(c_phi_Re, VariableType::evolution);
    }

//! The old constructor which assumes it is called in specificPostTimeStep
    //! so the first time step is when m_time == m_dt
    PhiExtraction(SphericalExtraction::params_t a_params, string a_output_root_dir, string a_data_subdir, string a_suffix,
                double a_dt, double a_time, double a_restart_time = 0.0)
        : PhiExtraction(a_params, a_output_root_dir, a_data_subdir, a_suffix, a_dt, a_time, (a_dt == a_time), 
                          a_restart_time)
    {
    }

//! Execute the query
    void execute_query(AMRInterpolator<Lagrange<4>> *a_interpolator)
    {
     	// extract the values of the phi field on the spheres
        extract(a_interpolator);

        if (m_params.write_extraction)
        {
            write_extraction("PhiExtractionOut_");
        }

	// now calculate and write the requested spherical harmonic modes
	// now calculate and write the requested spherical harmonic modes
        std::vector<std::pair<std::vector<double>, std::vector<double>>>
            mode_integrals(m_num_modes);

	// slightly pointless step
        const SphericalExtraction::complex_function_t phi_complex = [](std::vector<double> phi_re,
                                           double r, double, double) {
            // here the std::vector<double> passed will just have
            // the real phi as its only component
            return std::make_pair(phi_re[0], phi_re[0]);
        };	

	// add the modes that will be integrated
        for (int imode = 0; imode < m_num_modes; ++imode)
        {
            const auto &mode = m_modes[imode];
            constexpr int es = 0;
            add_mode_integrand(es, mode.first, mode.second,
                               phi_complex, mode_integrals[imode]);
        }

	// do the integration over the surface
        integrate();

	// write the integrals
        for (int imode = 0; imode < m_num_modes; ++imode)
        {
            const auto &mode = m_modes[imode];
            std::string integrals_filename = "Phi_integral_" + m_data_subdir + "_lm_" +
                                             std::to_string(mode.first) +
                                             std::to_string(mode.second) + m_suffix;
            std::vector<std::vector<double>> integrals_for_writing = {
                std::move(mode_integrals[imode].first)};
            std::vector<std::string> labels = {"phi integral"};
            write_integrals(integrals_filename, integrals_for_writing, labels);
        }
    }
};

#endif /* PHIEXTRACTION_HPP_ */
