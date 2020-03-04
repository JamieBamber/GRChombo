#include "KerrBH_Rfunc.hpp"

extern "C" double Rfunc(double M, double mu, double real_omega, double imag_omega, double a, int l, int m, bool index, bool reality, double r){
	std::complex<double> omega(real_omega, imag_omega);
	KerrBH_Rfunc Rfunc(M, mu, omega, a, l, m);	
	double result = Rfunc.compute(r, index, reality);
	return result;
}
