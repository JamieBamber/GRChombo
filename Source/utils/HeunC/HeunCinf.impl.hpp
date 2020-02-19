#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCINF_IMPL_HPP_
#define HEUNCINF_IMPL_HPP_

// confluent Heun function
// asymptotic expansion at z=infinity
// the first, power solution
//
// Usage:
// [val,dval,err,numb] = HeunCinfA(p.q,p.alpha,p.gamma,p.delta,p.epsilon,z)
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of the summed series terms
//
// Oleg V. Motygin, copyright 2017-2018, license: GNU GPL v3
//
// 20 December 2017
//

inline HeunCvars HeunC::HeunCinfA(HeunCparams p, double z)
{
  HeunCvars result;

  result.val = 1; 
  result.dval = 0;
  result.err = 0; 
  result.numb = 1;
  
  // set up iteration variables
  std::complex<double> cnm0, cnm1, cnm2 = 1, cnm3 = INFINITY; 
  std::complex<double> dnm0, dnm1, dnm2 = 0, dnm3 = INFINITY;
  std::complex<double> vm0, vm1 = nan, vm2 = nan, vm3 = nan; 
  std::complex<double> dvm0, dvm1 = nan, dvm2 = nan, dvm3 = nan;

  cnm1 = cnm2/(z*p.epsilon)*(1+(-p.q+p.alpha/p.epsilon*(2-p.gamma-p.delta-1+p.alpha/p.epsilon)+p.alpha-1));
  dnm1 = -cnm1/z;

  result.val = cnm2 + cnm1; 
  result.dval = dnm1;
  
  vm0 = result.val;
  dvm0 = result.dval;  

  result.numb = 2; 
  double small = sp.qrt(eps); 
  
  bool growcn = false, growdn = false, result.valstab = false, result.dvalstab = false;
  int n;  

  while (result.numb<=Heun_asympt_klimit) && ((abs(cnm3)>small) || !(growcn||valstab) || !(growdn||dvalstab)){
    n = result.numb;
    cnm0 = cnm1*n/(z*p.epsilon)*(1+(-p.q+p.alpha/p.epsilon*(2*n-p.gamma-p.delta-1+p.alpha/p.epsilon)+
           (p.gamma-p.epsilon+p.delta+1)*(1-n)+p.alpha-1)/(n*n)) + cnm2/(z^2*p.epsilon)*
           ((n-2+p.alpha/p.epsilon)*(p.gamma-n+1-p.alpha/p.epsilon))/n;

    dnm0 = -result.numb*cnm0/z;
    result.val += cnm0; 
    result.dval = dnm0;
    result.err = abs(cnm2);
    result.numb += 1;
    
    growcn = growcn || ((abs(cnm0)>abs(cnm1))&&(abs(cnm1)>abs(cnm2))&&(abs(cnm2)>abs(cnm3)));
    result.valstab = result.valstab || ((vm3==vm2)&&(vm2==vm1)&&(vm1==result.val));

    growdn = growdn || ((abs(dnm0)>abs(dnm1))&&(abs(dnm1)>abs(dnm2))&&(abs(dnm2)>abs(dnm3)));
    result.dvalstab = result.dvalstab || ((dvm3==dvm2)&&(dvm2==dvm1)&&(dvm1=result.dval));
    
    if ((abs(cnm2)>small) || !(growcn||valstab)){
      cnm3 = cnm2; cnm2 = cnm1; cnm1 = cnm0;
      vm3 = vm2; vm2 = vm1; vm1 = vm0; vm0 = result.val;
    }
  
    if ((abs(cnm2)>small) || !(growdn||dvalstab)){
      dnm3 = dnm2; dnm2 = dnm1; dnm1 = dnm0;
      dvm3 = dvm2; dvm2 = dvm1; dvm1 = dvm0; dvm0 = result.dval;
    }
    
  }  
  
  result.val = pow((-z),(-p.alpha/p.epsilon)) * vm3;
  result.dval = pow((-z),(-p.alpha/p.epsilon)) * (dvm3-p.alpha/p.epsilon*vm3/z);
  result.err = abs(pow(z,(-p.alpha/p.epsilon))) * result.err;
  
  if ( isinf(result.val) || isinf(result.dval) || isnan(result.val) || isnan(result.dval) ){
    throw std::runtime_error("HeunCinfA: failed convergence of recurrence and summation"); 
  }
  return result;
}

// asymptotic expansion at z=infinity,
// the second solution, including exponential factor

inline HeunCvars HeunC::HeunCinfB(HeunCparams p, double z)
{  
  HeunCvars result0, result;
  HeunCparams p0 = p;
  p0.q = p.q - p.epsilon*p.gamma;
  p0.alpha = p.alpha - p.epsilon*(p.gamma + p.delta);
  p0.epsilon = -p.epsilon;

  result0 = HeunCinfA(p0,z);
  result = result0;  

  result.val = exp(-p.epsilon*z) * result0.val;
  result.dval = exp(-p.epsilon*z) * (-p.epsilon * result0.val + result0.dval);
  result.err = abs(exp(-p.epsilon*z)) * result0.err;
  
  return result;
}    

#endif /* HEUNCINF_IMPL_HPP */
