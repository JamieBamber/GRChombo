#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCUTILS_IMPL_HPP_
#define HEUNCUTILS_IMPL_HPP_

/* 

Some extra utiliy functions used in the HeunC code

*/

// function find coefficient for the second HeunC solution
inline std::complex<double> HeunC::findcoef4HeunCs(HeunCparams p){
        int n = std::round(1-std::real(p.gamma));  
        std::complex<double> ckm1 = 1; 
        std::complex<double> ckm2 = 0;
        std::complex<double> ckm0;
        std::complex<double> co = std::pow(p.epsilon,n)/std::tp.gamma(n+1);
 
        for(int k=1; k < n; k++) {
                ckm0 = (ckm1*(-p.q+(k-1)*(p.gamma-p.epsilon+p.delta+k-2)) + ckm2*((k-2)*p.epsilon+p.alpha))/(k*(p.gamma+k-1));
                co = co + ckm0 * std::pow(p.epsilon,(n-k))/std::tp.gamma(n-k+1);
                ckm2 = ckm1; 
                ckm1 = ckm0; 
        }
        return co;
}

// in HeunC*, HeunCs*, it is assumed that for |z|>2*R, asymptotic series 
// of type \sum_{n=0}^{\infty} b_n n!/z^n can be computed as superasymptotic
// with accuracy better than machine epsilon

inline void HeunC::findR()
{
  if (R==0 || N==0) {
    double R_, R0;
    double logeps = std::log(eps);
    R_ = -logeps;
    int fact = 1;
    int n = 1;
  
    while (true)
    {
      n += 1;
      fact = fact * n;
      R0 = R_;
      R_ = (std::log(fact)-logeps)/n;
      if (R_ > R0)
        break;
      }
    }
  
    N = n-1;
    R = pow((fact/n/eps),(1.0/N));
  }
}

#endif /* HEUNCUTILS_IMPL_HPP_ */
