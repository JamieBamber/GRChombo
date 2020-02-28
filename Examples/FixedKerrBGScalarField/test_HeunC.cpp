#include <iostream>
#include <cstdio>
#include "KerrBH_Rfunc.hpp"

using namespace std;

int main() {
    printf("Hello, world!\n");
    
    //Make Rfunc solution object
    // KerrBH_Rfunc Rfunc(M, mu, omega, a, l, m);
    //KerrBH_Rfunc Rfunc(1, 0.4, 0.4, 0, 0, 0);
    HeunCspace::HeunC HC;
    std::complex<double> beta(0, +4*0.4);

    double r0 = 2;
    double max_r = 300.0;
    double min_r = r0 + 0.01;
    int start = log((min_r-r0)/r0);
    int stop = log((max_r-r0)/r0);
    double r;    
    int N = 200;
    double Phi;
    for(int k=0; k<N+1; k++){
	    r = r0 + pow((min_r - r0),static_cast<double>(N - k)/N)*pow((max_r - r0),static_cast<double>(k)/N);
	    Phi = Rfunc.compute(r, false);
            cout << "r = " << r <<  "	Phi = " << Phi << endl;
    }
    cout << "________________________________" << endl;

    //int fact = 3;
    //cout << std::log(static_cast<double>(fact)) << std::endl;

    return 0;
}
