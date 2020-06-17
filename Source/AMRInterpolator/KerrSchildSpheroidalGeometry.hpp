/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef KERRSCHILDKSSpheroidalGEOMETRY_HPP_
#define KERRSCHILDKSSpheroidalGEOMETRY_HPP_

#include <array>
#include <cmath>

//! This SurfaceGeometry template class provides spheroidal shell geometry
//! implementation for the SurfaceExtraction class, 
//! for Kerr Schild coordinates and r_KS = const surfaces. 
//! The symmetry axis isfixed to be in the z direction
//!
//! It is modified from the SpheroidalGeometry class
//!
//! u = theta, v = phi
class KSSpheroidalGeometry
{
  private:
    const std::array<double, CH_SPACEDIM> m_center;
    const double m_a; // dimensionfull black hole spin J/M

  public:
    KSSpheroidalGeometry(const std::array<double, CH_SPACEDIM> &a_center,
                       const double a_a)
        : m_center(a_center), m_a(a_a)
    {
    }

    //! denote the theta, phi variables as u, v

    //! returns the grid spacing in theta
    inline double du(int a_num_points_t) const
    {
        return M_PI / (double)(a_num_points_t - 1);
    }

    //! returns the grid spacing in phi
    inline double dv(int a_num_points_phi) const
    {
        return 2.0 * M_PI / ((double)a_num_points_phi);
    }

    //! returns the theta coordinate associated to the theta/u index
    inline double u(int a_it, int a_num_points_theta) const
    {
        return a_it * du(a_num_points_theta);
    }

    //! returns the phi coordinate associated to the phi/v index
    inline double v(int a_iphi, int a_num_points_phi) const
    {
        return a_iphi * dv(a_num_points_phi);
    }

    inline bool is_u_periodic() const { return false; }
    inline bool is_v_periodic() const { return true; }

    //! returns the Cartesian coordinate in direction a_dir with specified
    //! r_KS magnitude, t and phi.
    inline double get_grid_coord(int a_dir, double a_r, double a_theta,
                                 double a_phi) const
    {
        switch (a_dir)
        {
        case (0):
            return m_center[0] + sin(a_theta)*( a_r*cos(a_phi) + m_a*sin(a_phi));
        case (1):
            return m_center[1] + sin(a_theta)*( a_r*sin(a_phi) - m_a*cos(a_phi));
        case (2):
            return m_center[2] + a_r*cos(a_theta);
        default:
            MayDay::Error("KSSpheroidalGeometry: Direction not supported");
        }
    }

    //! returns the area element for radius r at the point
    //! (a_theta, a_phi)
    inline double area_element(double a_r, double a_theta,
                               double a_phi) const
    {
	double r2 = a_r*a_r;
        double ds_dtheta_dphi = sqrt((m_a*m_a + r2)*(r2 + m_a*m_a*cos(a_theta)*cos(a_theta)))*sin(a_theta);
        return ds_dtheta_dphi;
    }

    inline std::string param_name() const { return "r"; }

    inline std::string u_name() const { return "theta"; }

    inline std::string v_name() const { return "phi"; }
};

#endif /* KERRSCHILDKSSpheroidalGEOMETRY_HPP_ */
