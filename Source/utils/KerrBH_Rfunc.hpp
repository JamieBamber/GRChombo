/* C++ implementation of the radial part of the general solutions to the spin=0 Teucolsky equation
*/

#ifndef KERRBH_RFUNC_HPP_
#define KERRBH_RFUNC_HPP_

#include <cmath>
#include "HeunC.hpp"

class KerrBH_Rfunc {

public:
	double M;
	double mu;
	std::complex<double> omega;
	double a; 
	double r_plus, r_minus;
	int l, m;
	std::complex<double> alpha, beta, gamma, delta, eta;
	
	//constructor
	KerrBH_Rfunc(const double M_, const double mu_, const std::complex<double> omega_, double a_, int l_, int m_){
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
        	std::complex<double> lambda = Lambda_func(l,m,(a*a)*(std::pow(omega,2) - mu*mu));
        	std::complex<double> A = (std::pow((m*a),2) - 4*a*omega*m*r_plus + 4*std::pow((omega*r_plus),2) + d*d)/d*d;
        	std::complex<double> B = (-std::pow((m*a),2) + 4*a*M*omega*m + 4*(2*d - 1)*std::pow((omega*r_plus),2) - 2*std::pow((mu*d*r_plus),2)
                        	-2*(d*d)*(std::pow((omega*a*M),2) + lambda) - d*d)/(2*d*d);
        	std::complex<double> C = (std::pow((m*a),2) - 4*a*omega*m*r_minus + 4*std::pow((omega*r_minus),2) + d*d)/(d*d);
        	std::complex<double> D = (std::pow((m*a),2) - 4*a*M*omega*m + 4*(2*d + 1)*std::pow((omega*r_minus),2) + 2*std::pow((mu*d*r_minus),2) 
                        	+2*(d*d)*(std::pow((omega*a*M),2) + lambda) + d*d)/(2*d*d);
        	alpha = 4*d*M*std::sqrt(static_cast<std::complex<double>>(mu*mu - std::pow(omega,2)));
        	beta = std::sqrt(static_cast<std::complex<double>>(1 - A));
        	gamma = std::sqrt(static_cast<std::complex<double>>(1 - C));
        	delta = -(B + D);
        	eta = 0.5 + 2*B;
	}

	double compute(double r, bool index, bool real_or_imag){
		double z = (r_plus - r)/(r_plus - r_minus);
		std::complex<double> rootDelta = std::sqrt(static_cast<std::complex<double>>((r - r_plus)*(r - r_minus))); 
		int sgn;
		if (index==true){
			sgn = 1;
		} else if (index==false){
			sgn = -1;
		}
		std::complex<double> Rfunc = (M/rootDelta)*std::exp(sgn*0.5*alpha*z)*pow((z-1),0.5*(1+gamma))
						*pow(z,0.5*(1-sgn*beta))*HC.compute(sgn*alpha, -sgn*beta, gamma, delta, eta, z).val;		
		if (real_or_imag==true){
			return std::real(Rfunc);
		} else if (real_or_imag==false){
			return std::imag(Rfunc);
		}
	}

private:		
	HeunCspace::HeunC HC;

	double h(int l, int m){
		double h_ = (l*l - m*m)*l/(2*(l*l - 0.25));
        	return h_;
	}
	
	std::complex<double> Lambda_func(int l,int m,std::complex<double> c2=0){
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
