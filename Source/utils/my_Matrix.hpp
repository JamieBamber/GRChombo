/* 

C++ implementation of 2x2 matrix operations

*/

#ifndef MATRIX_HPP_
#define MATRIX_HPP_

#include "cmath.h"

template <class data_t, int width=2, int height=2> 
class Matrix {
	protected:
		// array to store values
		data_t values[height*width];
	public:
		int size = width*height;
		// constructors
		Matrix<T>(int height, int width);
        	Matrix<T>(std::vector<std::vector<T> > const &array);
        	Matrix<T>();
		// initialise values as nan
		void makeNaN(){
			for(int k; k < width*height; k++){
				values[k] = nan;
			}
		}
		
		// Define Matrix operation operators
		Matrix operator + (Matrix M2)
		{
			Matrix


#endif /* MATRIX_HPP_ */
