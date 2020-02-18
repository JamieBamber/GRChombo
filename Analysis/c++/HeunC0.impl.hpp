#if !defined(MAIN_HEUNC_HPP_)
#error "This file should only be included through MainHeunC.hpp"
#endif

#ifndef HEUNC0_IMPL_HPP_
#define HEUNC0_IMPL_HPP_

/*
Depends on:

HeunC00
HeunCconnect

*/
// confluent Heun function, the first local solution of the equation
// computed by a consequence of power expansions
//
// it is assumed that z does not belong to the branch-cut [1,\infty)
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 February 2018
//
HeunCvars HeunC0(HeunCparams p, double z, bool aux = false){
  
  HeunCvars result;
  
  if (z>=1){
    throw std::invalid_argument("HeunC0: z belongs to the branch-cut [1,\infty)");
  }
  else {
    bool expgrow = false;
    HeunCparams p1 = p;
    if ! aux {
      expgrow = real(-p.epsilon*z)>0;
      if expgrow {
        p1.q = p.q - p.epsilon * gamma;
        p1.alpha = p.alpha - p.epsilon * (gamma+delta);
        p1.epsilon = -p.epsilon;
      }
    }

    if (abs(z)<Heun_cont_coef) {
      result = HeunC00(p1,aux);
    }
    else {
      double z0 = Heun_cont_coef*z/abs(z);
      HeunCvars result0 = HeunC00(p1,z,aux);
      HeunCvars result1 = HeunCconnect(p1,z,z0,result0.val,result0.dval, R);
      result.numb = result0.numb + result1.numb;
      result.err = result0.err + result1.err;
    }
    if expgrow {
      result.val = result.val * exp(p1.epsilon*z);
      result.dval = (p1.epsilon * result.val + result.dval) * exp(p1.epsilon*z);
      result.err = result.err * abs(exp(p1.epsilon*z));
    }
  }
  return result;
}

#endif /* HEUNC0_IMPL_HPP_ */
