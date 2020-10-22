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
		std::complex<double> zfactor;
		// Kerr Schild correction
                if (KS_or_BL) {
			zfactor = std::polar(1.0, -2*m*std::atan2(a, r))*std::pow(-(z-1),gamma)*std::pow(-z,0.5*(sgn-1)*beta);
		} else {
			zfactor = std::pow(-(z-1),0.5*gamma)*std::pow(-z,0.5*sgn*beta);
		}
		std::complex<double> Rfunc = std::polar(1.0, -omega*t)*std::exp(sgn*0.5*alpha*z)*zfactor*H;		
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
		std::complex<double> zfactor;
		std::complex<double> dzfactor_z;
		HeunCspace::HeunCvars HC_result = HC.compute(sgn*alpha, sgn*beta, gamma, delta, eta, z);
		// Kerr Schild correction
                if (KS_or_BL) {
			zfactor = std::polar(1.0, -2*m*std::atan2(a, r))*std::pow(-(z-1),gamma)*std::pow(-z,0.5*(sgn-1)*beta);
			dzfactor_z = (r_minus - r_plus)*2*ComplexI*m*a*M/(r*r + (a*M)*(a*M)) + gamma/(z-1) + 0.5*(sgn-1)*beta/z;
		} else {
			zfactor = std::pow(-(z-1),0.5*gamma)*std::pow(-z,0.5*sgn*beta);
			dzfactor_z = 0.5*gamma/(z-1) + 0.5*sgn*beta/z;
		}
		
		std::complex<double> prefactor = std::polar(1.0, -omega*t) * std::exp(0.5*alpha*z);
		std::complex<double> Rfunc = prefactor * zfactor * HC_result.val/H0;
		std::complex<double> d_Rfunc_dt = -omega * ComplexI * Rfunc;
		std::complex<double> d_Rfunc_dr = (-1.0/(r_plus - r_minus))*prefactor*zfactor*( (0.5*sgn*alpha + dzfactor_z)*HC_result.val/H0 
							+ HC_result.dval/H0);
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
