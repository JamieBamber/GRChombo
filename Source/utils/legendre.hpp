/* This is my attempt to make a function for calculating legendre polynomials */

#ifndef LEGENDRE_
#define LEGENDRE_
#include "math.h"
#include "simd.hpp" 

// define / set my version of the function to calculate the legendre polynomials
template <class data_t> data_t my_legendre_p  (int l, data_t x) {
	if (l == 0) 
		return 1;
	if (l == 1)
		return x;
	if (l == 2)
		return (3*x*x - 1)/2.0;
	if (l == 3)
		return (5*pow(x,3) - 3*x)/2.0;
	if (l == 4)
		return (35*pow(x,4) - 30*x*x + 3)/8.0;
	if (l == 5)
		return (63*pow(x,5) - 70*pow(x,3) + 15*x)/8.0;
	if (l == 6)
		return (231*pow(x,6) - 315*pow(x,4) + 105*x*x - 5)/16.0;
	return 1;
}

// define function for the derivatives of the legendre polynomials
template <class data_t> data_t my_legendre_p_prime (int l, data_t x) {
	if (l == 0)  
                return 0;
        if (l == 1)
                return 1;
        if (l == 2)
                return 3*x;
        if (l == 3)
                return (15*pow(x,2) - 3)/2.0;
        if (l == 4)
                return (35*pow(x,3) - 15*x)/2.0;
        if (l == 5)
                return (325*pow(x,4) - 210*pow(x,2) + 15)/8.0;
        if (l == 6)
                return (6*231*pow(x,5) - 4*315*pow(x,3) + 2*105*x)/16.0;
	return 0;
}

#endif // ** LEGENDRE_ ** //	
