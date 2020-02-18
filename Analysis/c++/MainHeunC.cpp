
/* Comments from original author of MATLAB script. That is available here: https://github.com/motygin/confluent_Heun_functions */

// confluent Heun function, the first local solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
// at z=0 such that HeunC(0)=1 and
// HeunC'(0)=-q/gamma when gamma is not equal to 0
// HeunC'(z)/log(z) -> -q as z->0 when gamma = 0
//
// computed by a consequence of power expansions with improvements near points z=1 and z=\infty
//
// it is assumed that z does not belong to the branch-cut [1,\infty)
//
// Usage:
//  = HeunC(q,alpha,gamma,delta,epsilon,z)
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 26 January 2018
//

#include <complex>
#include <cmath>
#include <vector>
#include "Matrix.hpp"
#include "sgn.hpp"

#define eps 2.2204e-16

namespace HeunC {

struct HeunCvars {
std::complex<double>    val;
std::complex<double>    dval;
std::int                numb;
std::double             err;
}

struct HeunCparams {
std::complex<double>    p.q, p.alpha, p.gamma, p.delta, p.epsilon;
}

struct ConnectionVars
{
Matrix<std::complex<double>> C10;
double err;
int numb;
}

struct savedataVars
{
ConnectionVars Cvars;
HeunCparams p;
}

void MakeNan(HeunCvars result){
        result.val = nan;
        result.dval = nan;
        result.err = nan;
        result.numb = nan;
}

class HeunC {

   public:
	// options
	------------------------/*
        Heun_cont_coef:      for each power expansion of the analytic continuation procedure 
		 	     the coefficient is the relative (to the radius of convergence) distance from 
 		             the centre to the calculated point.

	Heun_klimit          maximum number of power series' terms.

	Heun_optserterms     number of power series' terms considered as in some sense optimal.

	Heun_asympt_klimit   maximum number of asymptotic series' terms.

	Heun_proxco, Heun_proxcoinf_rel      specifies relative proximity to singular point where special representation is used 

	Heun_memlimit	is the maximum number of sets of data (parameters of confluent Heun function and corresponding connection coefficients) which are kept in memory */
	const double Heun_cont_coef = 0.38;
	const int Heun_klimit = 1000;
	const int Heun_optserterms = 40;	
	const int Heun_asympt_klimit = 200;	
	const double Heun_proxco = 0.05, Heun_proxcoinf_rel = 1.0;

	// Constructor 
        HeunC() {} ;
	
	// main caluclation function
	HeunCvars compute(std::complex<double> alpha, std::complex<double> beta, std::complex<double> gamma, 
                          std::complex<double> delta, std::complex<double> eta, double z);
  
  private: 
        // component functions
        HeunCvars HeunC00(HeunCparams p, double z, bool woexp);
	HeunCvars HeunC00gen(HeunCparams p, double z);
	HeunCvars HeunC00log(HeunCparams p, double z);	

	HeunCvars HeunC0(HeunCparams p, double z, bool aux);	

	HeunCvars HeunCs0(HeunCparams p,double z);
	HeunCvars HeunCs00(HeunCparams p,double z);	
	HeunCvars HeunCs00gamma1(HeunCparams p,double z);

	HeunCvars HeunCfromZ0(HeunCparams p,double z,double Z0,std::complex<double> H0,std::complex<double> dH0)
	HeunCvars HeunCconnect(HeunCparams p,double z, double z0,std::complex<double> H0,std::complex<double> dH0,bool varargin=false, double& R, double R0);

	std::pair<HeunCvars, HeunCvars> HeunCfaraway(HeunCparams p,double z);
	


  end

end
