/* C++ implementation of the radial part of the general solutions to the spin=0 Teucolsky equation
*/

#ifndef HEUNC_RFUNC_HPP_
#define HEUNC_RFUNC_HPP_

#include <cmath>
#include "HeunC.hpp"

class HeunC_Rfunc {
public:
	double M;
	double mu;
	double omega;
	double a; 
	double r_plus, r_minus;
	int l, m, s;
	std::complex<double> alpha, beta, gamma, delta, eta;
	
	//constructor
	HeunC_Rfunc(const double M_, const double mu_, const double omega_, double a_, int l_, int m_, int s_)
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
		s = s_;
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
        	beta = std::sqrt(static_cast<std::complex<double>>(1 - A)) - s;
        	gamma = std::sqrt(static_cast<std::complex<double>>(1 - C)) - s;
        	delta = -(B + D) - s * alpha;
        	eta = 0.5 + 2*B + 0.5 * s*s + 2*ComplexI*s*omega*r_plus;
		std::cout << "alpha = " << alpha << std::endl;
		std::cout << "beta = " << beta << std::endl;
		std::cout << "gamma = " << gamma << std::endl;
		std::cout << "delta = " << delta << std::endl;
		std::cout << "eta = " << eta << std::endl;
	}

	double compute(double r, bool ingoing){
		int sgn;
		if (ingoing==true){
			sgn = 1;
		} else if (ingoing==false){
			sgn = -1;
		}
		const double small = 0.0001;
		// const std::complex<double> H0 = HC.compute(-sgn*alpha, sgn*beta, gamma, delta, eta, -small).val;
		double z = (r_plus - r)/(r_plus - r_minus);
		std::complex<double> H = HC.compute(-sgn*alpha, sgn*beta, gamma, delta, eta, z).val;
		return std::real(H);
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
