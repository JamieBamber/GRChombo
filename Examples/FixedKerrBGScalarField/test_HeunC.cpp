#include <iostream>
#include <cstdio>
#include "HeunC.hpp"

using namespace std;

int main() {
    printf("Hello, world!\n");
    
    //Make HeunC object
    HeunCspace::HeunC HC;
    double r, S;
    r = 200;
    std::complex<double> H;
    H = HC.compute(0, -0.5, -0.5, 0, 1.0/8, 1-r).val;
    S = sqrt(r);
    cout << "r = " << r <<  " sqrt(r) = " << S << " HeunC = " << H << endl;
    cout << "________________________________" << endl;
    return 0;
}
