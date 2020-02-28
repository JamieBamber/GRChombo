#include "KerrBH_Rfunc.hpp"

extern "C" double Rfunc(double M, double mu, double omega, double a, int l, int m, bool index, bool reality, double r){
	KerrBH_Rfunc Rfunc(M, mu, omega, a, l, m);	
	double result = Rfunc.compute(r, index, reality);
	return result;
}
