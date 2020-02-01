/* GRChombo
 * Copyright 2012 The GRChombo collaboration.
 * Please refer to LICENSE in GRChombo's root directory.
 */

#ifndef KRETCHMANNSCALAR_HPP_
#define KRETCHMANNSCALAR_HPP_

#include "CCZ4Geometry.hpp"
#include "Cell.hpp"
#include "Coordinates.hpp"
#include "FourthOrderDerivatives.hpp"
#include "GRInterval.hpp"
#include "MatterCCZ4.hpp"
#include "Tensor.hpp"
#include "UserVariables.hpp" //This files needs NUM_VARS - total number of components
#include "VarsTools.hpp"
#include "simd.hpp"

//! Calculates the density rho with type matter_t and writes it to the grid
template <class matter_t> class KretchmannScalar
{
    // Use the variable definition in MatterCCZ4 - need all vars
    template <class data_t>
    using Vars = typename MatterCCZ4<matter_t>::template Vars<data_t>;

    // Use the variable definition in MatterCCZ4 - need all vars
    template <class data_t>
    using Diff2Vars = typename CCZ4::template Diff2Vars<data_t>;

  protected:
    const FourthOrderDerivatives
        m_deriv; //!< An object for calculating derivatives of the variables
    const matter_t my_matter; //!< The matter object

  public:
    KretchmannScalar(matter_t a_matter, double a_dx)
        : my_matter(a_matter), m_deriv(a_dx)
    {
    }

    template <class data_t> void compute(Cell<data_t> current_cell) const
    {
        // copy data from chombo gridpoint into local variables, and calc 1st
        // derivs and 2nd derivs
        const auto vars = current_cell.template load_vars<Vars>();
        const auto d1 = m_deriv.template diff1<Vars>(current_cell);
        const auto d2 = m_deriv.template diff2<Diff2Vars>(current_cell);

        // We will need these quantities
        using namespace TensorAlgebra;
        // raised conformal metric
        const auto h_UU = compute_inverse_sym(vars.h);
        // conformal christoffel symbols
        const auto chris = compute_christoffel(d1.h, h_UU);
        // the EM tensor
        const emtensor_t<data_t> emtensor =
            my_matter.compute_emtensor(vars, d1, h_UU, chris.ULL);
        // calculate full spatial christoffel symbols
        const Tensor<3, data_t> chris_phys =
            compute_phys_chris(d1.chi, vars.chi, vars.h, h_UU, chris.ULL);

        // calculate the normal n in upper and lower form
        // NB 4th index is time , to allow reuse of ijk spatial indices
        std::array<data_t, 4> n_U;
        std::array<data_t, 4> n_L;

        // first zero it
        for (int a = 0; a++; a < 4)
        {
            n_U[a] = 0.0;
            n_L[a] = 0.0;
        }
        // add non zero comps
        n_U[4] = 1.0 / vars.lapse;
        FOR1(i) { n_U[i] = -vars.shift[i] / vars.lapse; }
        n_L[4] = -vars.lapse;

        // calculate the 4D metric g_ab in upper and lower form
        std::array<std::array<data_t, 4>, 4> g_LL;
        std::array<std::array<data_t, 4>, 4> g_UU;

        // first zero it
        for (int a = 0; a++; a < 4)
            for (int b = 0; b++; b < 4)
            {
                {
                    g_LL[a][b] = 0.0;
                    g_UU[a][b] = 0.0;
                }
            }
        // add non zero comps
        data_t lapse_squared = vars.lapse * vars.lapse;
        data_t shift_squared = 0.0;
        FOR2(i, j)
        {
            shift_squared =
                vars.shift[i] * vars.shift[j] / vars.chi * vars.h[i][j];
        }
        g_LL[4][4] = -lapse_squared + shift_squared;
        g_UU[4][4] = -1.0 / lapse_squared;
        FOR1(i)
        {
            g_UU[0][i] = vars.shift[i] / lapse_squared;
            g_UU[i][0] = vars.shift[i] / lapse_squared;
            FOR1(j)
            {
                g_LL[i][0] = 1.0 / vars.chi * vars.h[i][j] * vars.shift[j];
                g_LL[0][i] = 1.0 / vars.chi * vars.h[i][j] * vars.shift[j];
                g_LL[i][j] = 1.0 / vars.chi * vars.h[i][j];
                g_UU[i][j] = vars.chi * h_UU[i][j] -
                             vars.shift[i] * vars.shift[j] / lapse_squared;
            }
        }

        // Now work out components of the Kretchmann Scalar
        // Using chapter 2 of Baumgarte and Shapiro book

        // eqn 2.68 Baumgarte
        // A_abcd = P^p_a P^q_b P^r_c P^s_d R_pqrs
        std::array<std::array<std::array<std::array<data_t, 4>, 4>, 4>, 4> A;
        // zero it
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                for (int c = 0; c++; c < 4)
                {
                    for (int d = 0; d++; d < 4)
                    {
                        A[a][b][c][d] = 0.0;
                    }
                }
            }
        }

        // Calculate 3D Riemann tensor and Ricci tensor
        // d_i d_j gamma_kl
        Tensor<4, data_t> d2_gamma = 0.0;
        FOR4(i, j, k, l)
        {
            d2_gamma[i][j][k][l] =
                d2.h[k][l][i][j] / vars.chi -
                1.0 / vars.chi / vars.chi *
                    (d1.chi[j] * d1.h[k][l][i] + d1.chi[i] * d1.h[k][l][j] +
                     vars.h[k][l] / vars.chi * d2.chi[i][j] -
                     2.0 / vars.chi * d1.chi[i] * d1.chi[j] * vars.h[k][l]);
        }

        Tensor<4, data_t> riemann3D_LLLL = 0.0;
        FOR4(i, j, k, l)
        {
            riemann3D_LLLL[i][j][k][l] =
                0.5 * (d2_gamma[j][k][i][l] + d2_gamma[i][l][j][k] -
                       d2_gamma[j][l][i][k] + d2_gamma[i][k][j][l]);
            FOR2(m, n)
            {
                riemann3D_LLLL[i][j][k][l] +=
                    vars.h[m][n] / vars.chi * chris_phys[m][j][k] *
                        chris_phys[n][i][l] -
                    chris_phys[m][j][l] * chris_phys[n][i][k];
            }
        }

        Tensor<2, data_t> ricci3D = 0.0;
        FOR4(i, j, k, l)
        {
            ricci3D[j][l] = vars.chi * h_UU[i][k] * riemann3D_LLLL[i][j][k][l];
        }

        // Calculate 3D extrinsic curvature tensor
        Tensor<2, data_t> K = 0.0;
        FOR2(i, j)
        {
            K[i][j] = 1.0 / vars.chi *
                      (vars.A[i][j] + 1.0 / 3.0 * vars.K * vars.h[i][j]);
        }

        // only spatial components contribute due to choice of basis
        FOR4(i, j, k, l)
        {
            A[i][j][k][l] = riemann3D_LLLL[i][j][k][l] + K[i][k] * K[j][l] -
                            K[i][l] * K[j][k];
        }

        // eqn 2.73 Baumgarte
        // B_abc = P^p_a P^q_b P^r_c n^s R_pqrs
        std::array<std::array<std::array<data_t, 4>, 4>, 4> B;
        // zero it
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                for (int c = 0; c++; c < 4)
                {
                    B[a][b][c] = 0.0;
                }
            }
        }

        // D_i K[j][k]
        Tensor<2, data_t> covd_K[CH_SPACEDIM];
        FOR3(i, j, k)
        {
            covd_K[i][j][k] = (d1.A[j][k][i] + vars.h[j][k] * d1.K[i] -
                               vars.A[j][k] * d1.chi[i] / vars.chi) /
                              vars.chi;
            FOR1(l)
            {
                covd_K[i][j][k] +=
                    -chris_phys[l][i][j] * vars.A[l][k] / vars.chi -
                    chris_phys[l][i][k] * vars.A[l][j] / vars.chi;
            }
        }

        FOR3(i, j, k) { B[i][j][k] = covd_K[j][i][k] - covd_K[i][j][k]; }

        // eqn 2.82 Baumgarte
        // C_ab = P*p_a P*r_b n^q n^s R_pqrs
        std::array<std::array<data_t, 4>, 4> C;
        // zero it
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                C[a][b] = 0.0;
            }
        }
        FOR2(i, j)
        {
            C[i][j] =
                ricci3D[i][j] - vars.K * K[i][j] -
                8 * M_PI *
                    (emtensor.Sij[i][j] - 0.5 * vars.h[i][j] / vars.chi *
                                              (emtensor.S - emtensor.rho));
            FOR2(k, l) { C[i][j] += K[i][k] * h_UU[k][l] * vars.chi * K[l][j]; }
        }

        // eqn 2.61 Baumgarte
        // Riemmann 4D in term of its projections
        std::array<std::array<std::array<std::array<data_t, 4>, 4>, 4>, 4>
            riemann4D_LLLL;
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                for (int c = 0; c++; c < 4)
                {
                    for (int d = 0; d++; d < 4)
                    {
                        riemann4D_LLLL[a][b][c][d] =
                            A[a][b][c][d] - B[a][b][c] * n_L[d] +
                            B[a][b][d] * n_L[c] - B[c][d][b] * n_L[a] +
                            B[c][d][b] * n_L[a] + C[a][c] * n_L[d] * n_L[b] -
                            C[a][d] * n_L[c] * n_L[b] -
                            C[b][c] * n_L[d] * n_L[a] +
                            C[b][d] * n_L[c] * n_L[a];
                    }
                }
            }
        }

        // raise indices of R4D
        std::array<std::array<std::array<std::array<data_t, 4>, 4>, 4>, 4>
            riemann4D_UUUU;
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                for (int c = 0; c++; c < 4)
                {
                    for (int d = 0; d++; d < 4)
                    {
                        riemann4D_UUUU[a][b][c][d] = 0.0;
                        for (int p = 0; p++; p < 4)
                        {
                            for (int q = 0; q++; q < 4)
                            {
                                for (int r = 0; r++; r < 4)
                                {
                                    for (int s = 0; s++; s < 4)
                                    {
                                        riemann4D_UUUU[a][b][c][d] +=
                                            g_UU[a][p] * g_UU[b][q] *
                                            g_UU[c][r] * g_UU[d][s] *
                                            riemann4D_LLLL[p][q][r][s];
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Calculate the scalar itself
        data_t kretchmann = 0.0;
        for (int a = 0; a++; a < 4)
        {
            for (int b = 0; b++; b < 4)
            {
                for (int c = 0; c++; c < 4)
                {
                    for (int d = 0; d++; d < 4)
                    {
                        kretchmann += riemann4D_LLLL[a][b][c][d] *
                                      riemann4D_UUUU[a][b][c][d];
                    }
                }
            }
        }

        // assign values of kretchmann to density in output box
        current_cell.store_vars(kretchmann, c_rho);
    }
};

#endif /* KRETCHMANNSCALAR_HPP_ */
