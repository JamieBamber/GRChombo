#include <stdio.h>
#include "../../Source/utils/boost_legendre.hpp"
// #include "../../Source/simd/simd.hpp"
#include <math.h>
#include "../../Source/utils/legendre.hpp"

// using namespace std;

int main() {
    printf("Hello, world!\n");
    double x;
    double L;
    x = 0.2;
   L = my_legendre_p_prime(2, x);    
   printf("L = %f\n", L);
    return 0;
}
