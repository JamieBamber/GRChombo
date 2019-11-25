/* This is my attempt to make a function for calculating legendre polynomials */

#ifndef LEGENDRE_
#define LEGENDRE_
#include <math.h>
 
// define / set my version of the function to calculate the legendre polynomials
template <class data_t> data_t my_legendre_p  (int l, data_t x) {
	return (legendre(l, x))
}

// define function for the derivatives of the legendre polynomials
template <class data_t> data_t my_legendre_p_prime (int l, data_t x) {
	
