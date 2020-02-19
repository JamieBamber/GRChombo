#include <iostream>
#include <cstdio>
#include "HeunC.hpp"

using namespace std;

int main() {
    std::cout << "Hello, world!\n";
    
    //Make HeunC object
    HeunCspace::HeunC HC;
    double r;
    std::complex<double> H;
    for(int k=0; k<100; k++){
	r = 0.5*k;
        H = HC.compute(0, -0.5, -0.5, 0, 1.0/8, 1-r).val;
        S = sqrt(r);
	cout << "r = " << r <<  " sqrt(r) = " << S << " HeunC = " << H << endl;
    }
    return 0;
}
