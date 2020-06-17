/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef KERRSCHILDSPHEROIDALEXTRACTION_HPP_
#define KERRSCHILDSPHEROIDALEXTRACTION_HPP_

#include "KerrSchildSpheroidalGeometry.hpp"
#include "SurfaceExtraction.hpp"

//! A child class of SurfaceExtraction for extraction on spheroidal shells
class KSSpheroidalExtraction : public SurfaceExtraction<KSSpheroidalGeometry>
{
  public:
    struct params_t : SurfaceExtraction::params_t
    {
        int &num_extraction_radii = num_surfaces;
        std::vector<double> &extraction_radii = surface_param_values;
        int &num_points_theta = num_points_u;
        int &num_points_phi = num_points_v;
        std::array<double, CH_SPACEDIM> center; //!< the center of the spheroidal
                                                //!< shells
        std::array<double, CH_SPACEDIM> &extraction_center = center;
        double a; //!< the dimensionfull black hole spin

        // constructor
        params_t() = default;

        // copy constructor defined due to references pointing to the wrong
        // things with the default copy constructor
        params_t(const params_t &params)
            : center(params.center), a(params.a),
              SurfaceExtraction::params_t(params)
        {
        }
    };

//    const std::array<double, CH_SPACEDIM> m_center;
//    const double m_a

    KSSpheroidalExtraction(const params_t &a_params, double a_dt, double a_time,
                        bool a_first_step, double a_restart_time = 0.0)
        : SurfaceExtraction(KSSpheroidalGeometry(a_params.center,
                                               a_params.a),
                            a_params, a_dt, a_time,
                            a_first_step, a_restart_time)
//          m_center(a_params.center), m_a(a_params.a)
    {
    }

    KSSpheroidalExtraction(const params_t &a_params,
                        const std::vector<std::pair<int, Derivative>> &a_vars,
                        double a_dt, double a_time, bool a_first_step,
                        double a_restart_time = 0.0)
        : KSSpheroidalExtraction(a_params, a_dt, a_time, a_first_step,
                              a_restart_time)
    {
        add_vars(a_vars);
    }

    KSSpheroidalExtraction(const params_t &a_params,
                        const std::vector<int> &a_vars, double a_dt,
                        double a_time, bool a_first_step,
                        double a_restart_time = 0.0)
        : KSSpheroidalExtraction(a_params, a_dt, a_time, a_first_step,
                              a_restart_time)
    {
        add_vars(a_vars);
    }

    // Add specific methods?

};

#endif /* KERRSCHILDSPHEROIDALEXTRACTION_HPP_ */
