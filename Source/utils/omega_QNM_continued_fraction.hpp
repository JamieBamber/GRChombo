/* C++ implementation to calculate the quasinormal mode frequencies from the Teukolsky equation using the 
continued fraction method */

#ifndef OMEGA_QNM_CONTINUED_FRACTION_HPP_
#define OMEGA_QNM_CONTINUED_FRACTION_HPP_

#include <cmath>
#include <complex>
#include <vector>
#include <iostream>

/*struct omega_output {
	std::complex<double> val;
	int n_step;
	double f_val;
};*/

class QNM_cf {	
public:
	double M;
        double mu;
        double a; 
        double r_plus, r_minus;
        int l, m, s;

	//constructor
        QNM_cf(const double M_, const double mu_, const double a_, const int l_, const int m_, const int s_)
        : ComplexI(0.0, 1.0)
        {
                if (std::abs(m_)>l_){
                        std::cout << "m = " << m_ << std::endl;
                        std::cout << "l = " << l_ << std::endl;
			throw std::invalid_argument("|m| must be less than or equal to l");
                }
                M = M_;
                mu = mu_;
                a = a_;
                l = std::abs(l_);
                m = m_;
                s = s_;
                r_plus = M*(1 + std::sqrt(1 - a*a));
                r_minus = M*(1 - std::sqrt(1 - a*a));
	}

	std::complex<double> F(int N, std::complex<double> omega){
		// use Steed's algorithm to compute the continued fraction
		std::complex<double> rho_km1 = 0;
		std::complex<double> t0 = x_n(0,omega);
		std::complex<double> C = t0;
		std::complex<double> t_km1 = t0;
		std::complex<double> a_k, t_k;
		for (int n=1; n<N; n++){
			a_k = x_n(n,omega);
			std::complex<double> rho_k = a_k*(1+rho_km1)/(1-a_k*(1+rho_km1));
			t_k = rho_k*t_km1;
			C = C + t_k;
			t_km1 = t_k;
			rho_km1 = rho_k;
		}
		std::complex<double> result = beta(0,omega)*(1-C);
		return result;
	}

	void compute_omega(int N, double omega0_Re, double omega0_Im, double epsilon, int n_max, 
				double *omega_Re, double *omega_Im, int *n_step, double *f_val){
		// Use the Newton-Raphson method to compute the root of F(omega)
		double omega_est_Re = omega0_Re;
		double omega_est_Im = omega0_Im;
		std::complex<double> omega_est(omega_est_Re, omega_est_Im);
		double f = std::abs(F(N, omega_est));
		double dfRe_dxRe, dfRe_dxIm, dfIm_dxRe, dfIm_dxIm, det, domega_Re, domega_Im;
		std::complex<double> Fval, Fhval, FhIval;
		double h = 0.00000001;
		int n_count = 0;
		while ((f > epsilon) && (n_count < n_max)){
			std::complex<double> omega_est(omega_est_Re, omega_est_Im);
			Fval = F(N, omega_est);
			Fhval = F(N, omega_est+h);
			FhIval = F(N, omega_est+h*ComplexI);
			dfRe_dxRe = std::real(Fhval-Fval)/h;
			dfRe_dxIm = std::real(FhIval-Fval)/h;
			dfIm_dxRe = std::imag(Fhval-Fval)/h;
			dfIm_dxIm = std::imag(FhIval-Fval)/h;
			det = dfRe_dxRe*dfIm_dxIm - dfRe_dxIm*dfIm_dxRe;
			domega_Re = -(std::real(Fval)*dfIm_dxIm-std::imag(Fval)*dfRe_dxIm)/det;
			domega_Im = -(-std::real(Fval)*dfIm_dxRe+std::imag(Fval)*dfRe_dxRe)/det;			
			omega_est_Re = omega_est_Re + domega_Re;
			omega_est_Im = omega_est_Im + domega_Im;
			f = std::abs(F(N, omega_est));
			n_count = n_count + 1;
		}
		*omega_Re = omega_est_Re;
		*omega_Im = omega_est_Im;
		*f_val = f;
		*n_step = n_count;
	}

private:
	// complex i
        const std::complex<double> ComplexI;    
	const double b = std::sqrt(1 - a*a);

        double h(int l, int m){
                double h_ = (l*l - m*m)*l/(2*(l*l - 0.25));
                return h_;
        }       
        std::complex<double> Lambda_func(std::complex<double> omega){
		std::complex<double> c2 = a*a*(std::pow(omega,2) - mu*mu);
                if (c2==0){
                        return l*(l+1);
                }
                if (c2!=0){
                        double h0, h1, h2, h3, h_1, h_2, f_0, f_2, f_4, f_6; 
                        h0 = h(l, m);
                        h1 = h(l+1, m);
                        h2 = h(l+2, m);
                        h3 = h(l+3, m);
                        h_1 = h(l-1, m);
                        h_2 = h(l-2, m);
                        f_0 = l*(l+1);
                        f_2 += h1 - h0 - 1;
                        f_4 += - (l+2)*h1*h2/(2*(l+1)*(2*l+3)) + h1*h1/(2*(l+1)) +
                                h0*h1/(2*l*(l + 1)) - h0*h0/(2*l) + (l-1)*h_1*h0/(2*l*(2*l-1));
                        f_6 = (h1*h2/(4*(l+1)*std::pow((2*l+3),2)))*((l+3)*h3/3 + ((l+2)/(l+1))*
                                ((l+2)*h2 - (7*l+10)*h1 + (3*l*l + 2*l - 3)*h0/l));
                        f_6 +=  std::pow(h1,3)/(2*(l+1)*(l+1)) - std::pow(h0,3)/(2*l*l)
                                +(h0*h1/(4*(l*l)*(l+1)*(l+1)))*((2*l*l + 4*l + 3)*h0 - (2*l*l + 1)*h1
                                - (l*l - 1)*(3*l*l + 4*l - 2)*h_1/std::pow((2*l-1),2));
                        f_6 += (h_1*h0/4*l*l*std::pow((2*l-1),2))*((l-1)*(7*l-3)*h0
                                - ((l-1)*(l-1))*h_1 - l*(l-2)*h_2/3);
                        //
                        return f_0 + f_2*c2 + f_4*(c2*c2) + f_6*(c2*c2*c2);
                }
        }

	// Using Dolan https://arxiv.org/pdf/0705.2880.pdf and Leaver https://www.edleaver.com/Misc/EdLeaver/Publications/AnalyticRepresentationForQuasinormalModesOfKerrBlackHoles.pdf

	std::complex<double> alpha(int n, std::complex<double> omega){
		std::complex<double> c0 = 1 - s - ComplexI*omega*2*M - (2*ComplexI/b)*(omega*M - a*m/2);
		std::complex<double> result = n*n + (c0+1)*n + c0;
		return result;
	}

	std::complex<double> beta(int n, std::complex<double> omega){
		std::complex<double> q = -std::sqrt(mu*mu - omega*omega);
		std::complex<double> c1 = -4 + 4*ComplexI*M*(omega-ComplexI*q*(1+b))+(4*ComplexI/b)*(omega*M - a*m/2)
                                        -2*mu*mu*M/q;
                std::complex<double> c3 = 2*ComplexI*M*M*std::pow(omega-ComplexI*q,3)/q+2*std::pow(M*(omega-ComplexI*q),2)*b
					+std::pow(M*q*a,2)+2*ComplexI*M*q*a*m-s-1-Lambda_func(omega)+s*(s+1)
					-M*std::pow(omega-ComplexI*q,2)/q + 2*M*q*b
					+ (2*ComplexI/b)*(M*std::pow(omega-ComplexI*q,2)/q+1)*(omega*M - a*m/2);
		std::complex<double> result = -2*n*n+(c1+2)*n + c3;
		return result;
	}

	std::complex<double> gamma(int n, std::complex<double> omega){
		std::complex<double> q = -std::sqrt(mu*mu - omega*omega);
		std::complex<double> c2 = s+3-ComplexI*2*M*omega-2*M*(q*q-omega*omega)/q-(2*ComplexI/b)*(M*omega-a*m/2);
		std::complex<double> c4 = M*M*std::pow(omega-ComplexI*q,4)/(q*q)+2*M*M*ComplexI*omega*std::pow(omega-ComplexI*q,2)/q
					-(2*ComplexI/b)*(M*std::pow(omega-ComplexI*q,2)/q)*(omega*M - a*m/2)-2*s*M*ComplexI*omega;
		std::complex<double> result = n*n+(c2-3)*n + c4;
		return result;
	}

	std::complex<double> x_n(int n, std::complex<double> omega){
		std::complex<double> result = alpha(n, omega)*gamma(n+1,omega)/(beta(n,omega)*beta(n+1,omega));
		return result;
	}
};

#endif /* OMEGA_QNM_CONTINUED_FRACTION_HPP_ */

