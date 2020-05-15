/* C++ implementation of the radial part of the general solutions to the spin=0 Teucolsky equation
*/

#ifndef KERRBH_RFUNC_HPP_
#define KERRBH_RFUNC_HPP_

#include <cmath>
#include "HeunC.hpp"

struct Rfunc_with_deriv {
	double Rfunc;
	double d_Rfunc_dt;
	double d_Rfunc_dr;
};

class KerrBH_Rfunc {
public:
	double M;
	double mu;
	double omega;
	double a; 
	double r_plus, r_minus;
	int l, m;
	std::complex<double> alpha, beta, gamma, delta, eta;
	
	//constructor
	KerrBH_Rfunc(const double M_, const double mu_, const double omega_, double a_, int l_, int m_)
	: ComplexI(0.0, 1.0)
	{
		if (std::abs(m_)>l_){
			throw std::invalid_argument("|m| must be less than or equal to l");
		}
		M = M_;
		mu = mu_;
		omega = omega_;
		a = a_;
		l = std::abs(l_);
		m = m_;
		r_plus = M*(1 + std::sqrt(1 - a*a));
        	r_minus = M*(1 - std::sqrt(1 - a*a)); 
        	double d = std::sqrt(1 - a*a);
        	double lambda = Lambda_func(l,m,(a*a)*(std::pow(omega,2) - mu*mu));
        	double A = (std::pow((m*a),2) - 4*a*omega*m*r_plus + 4*std::pow((omega*r_plus),2) + d*d)/d*d;
        	double B = (-std::pow((m*a),2) + 4*a*M*omega*m + 4*(2*d - 1)*std::pow((omega*r_plus),2) - 2*std::pow((mu*d*r_plus),2)
                        	-2*(d*d)*(std::pow((omega*a*M),2) + lambda) - d*d)/(2*d*d);
        	double C = (std::pow((m*a),2) - 4*a*omega*m*r_minus + 4*std::pow((omega*r_minus),2) + d*d)/(d*d);
        	double D = (std::pow((m*a),2) - 4*a*M*omega*m + 4*(2*d + 1)*std::pow((omega*r_minus),2) + 2*std::pow((mu*d*r_minus),2) 
                        	+2*(d*d)*(std::pow((omega*a*M),2) + lambda) + d*d)/(2*d*d);
        	alpha = 4*d*M*std::sqrt(static_cast<std::complex<double>>(mu*mu - std::pow(omega,2)));
        	beta = std::sqrt(static_cast<std::complex<double>>(1 - A));
        	gamma = std::sqrt(static_cast<std::complex<double>>(1 - C));
        	delta = -(B + D);
        	eta = 0.5 + 2*B;
	}

	double compute(double r, double t, bool ingoing, bool KS_or_BL){
		int sgn;
		if (ingoing==true){
			sgn = 1;
		} else if (ingoing==false){
			sgn = -1;
		}
		const double small = 0.0001;
		const std::complex<double> H0 = HC.compute(-sgn*alpha, sgn*beta, gamma, delta, eta, -small).val;
		double z = (r_plus - r)/(r_plus - r_minus);
		std::complex<double> H = HC.compute(sgn*alpha, sgn*beta, gamma, delta, eta, z).val/H0;
		std::complex<double> Rfunc = std::polar(1.0, -omega*t) * std::exp(sgn*0.5*alpha*z)*std::pow(-(z-1),0.5*(gamma))
						*std::pow(-z,0.5*(sgn*beta))*H;		
		// Kerr Schild correction
                if (KS_or_BL) {
			double r_factor;
                        if (r_minus > 0) {
                                r_factor = ((2*M)/(r_plus - r_minus)) * ( r_plus * std::log(r/r_plus - 1) - r_minus * std::log(r/r_minus - 1));
                        } else {
                                r_factor = ((2*M)/(r_plus - r_minus)) * ( r_plus * std::log(r/r_plus - 1) );
                        }
                        std::complex<double> KS_correction = std::polar(1.0, omega*r_factor);
                        Rfunc = Rfunc * KS_correction;
                }
		return std::real(Rfunc);
	}

	Rfunc_with_deriv compute_with_deriv(double r, double t, bool ingoing, bool KS_or_BL){
		// assuming R(r, t) = exp(- i omega t) * HeunC solution
		double z = (r_plus - r)/(r_plus - r_minus);
		std::complex<double> Delta = static_cast<std::complex<double>>((r - r_plus)*(r - r_minus));
		int sgn;
		if (ingoing==true){
			sgn = 1;
		} else if (ingoing==false){
			sgn = -1;
		}
		const double small = 0.0001;
		const std::complex<double> H0 = HC.compute(sgn*alpha, sgn*beta, gamma, delta, eta, -small).val;
		std::complex<double> prefactor = std::exp(0.5*alpha*z)*std::pow(-(z-1),0.5*(gamma))
                                                *std::pow(-z,0.5*(sgn*beta));
		HeunCspace::HeunCvars HC_result = HC.compute(sgn*alpha, sgn*beta, gamma, delta, eta, z);
		std::complex<double> Rfunc = std::polar(1.0, -omega*t) * prefactor * HC_result.val/H0;
		std::complex<double> d_Rfunc_dt = -omega * ComplexI * Rfunc;
		std::complex<double> d_Rfunc_dr = (-1/(r_plus - r_minus))*prefactor*( (0.5*sgn*alpha + 0.5*gamma/(z-1) + 0.5*sgn*beta/z)*HC_result.val/H0 
							+ HC_result.dval/H0);
		// Kerr Schild correction
                if (KS_or_BL) {
			double r_factor;
                        if (r_minus > 0) {
                                r_factor = ((2*M)/(r_plus - r_minus)) * ( r_plus * std::log(r/r_plus - 1) - r_minus * std::log(r/r_minus - 1));
                        } else {
                                r_factor = ((2*M)/(r_plus - r_minus)) * ( r_plus * std::log(r/r_plus - 1) );
                        }
                        std::complex<double> KS_correction = std::polar(1.0, omega*r_factor);
                        Rfunc = Rfunc * KS_correction;
			d_Rfunc_dt = d_Rfunc_dt * KS_correction;
			d_Rfunc_dr = d_Rfunc_dr * KS_correction + ComplexI * omega * (2*M*r/Delta) * Rfunc;
                }
		// output struct 
		Rfunc_with_deriv output;
		output.Rfunc = std::real(Rfunc);
		output.d_Rfunc_dt = std::real(d_Rfunc_dt);
		output.d_Rfunc_dr = std::real(d_Rfunc_dr);
		return output;
	}

private:		
	// complex i
	const std::complex<double> ComplexI;	
	HeunCspace::HeunC HC;

	double h(int l, int m){
		double h_ = (l*l - m*m)*l/(2*(l*l - 0.25));
        	return h_;
	}	
	double Lambda_func(int l,int m,double c2=0){
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
};

#endif /* KERRBH_RFUNC_HPP_ */
