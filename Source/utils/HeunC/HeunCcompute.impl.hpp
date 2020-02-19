#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCCOMPUTE_IMPL_HPP_
#define HEUNCCOMPUTE_IMPL_HPP_

/*
Depends on:

HeunCfaraway
HeunC0
HeunCnear1

*/
// confluent Heun function, the first local solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
// at z=0 such that HeunC(0)=1 and
// HeunC'(0)=-q/gamma when gamma is not equal to 0
// HeunC'(z)/log(z) -> -q as z->0 when gamma = 0
//
// computed by a consequence of power expansions with improvements near points z=1 and z=infty
//
// it is assumed that z does not belong to the branch-cut [1,infty)
//
// Usage:
// [val,dval,err,numb,wrnmsg,valwoexp,dvalwoexp,errwoexp] = HeunC(q,alpha,gamma,delta,epsilon,z)
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 26 January 2018
//

inline HeunCvars compute(std::complex<double> alpha_, std::complex<double> beta_, std::complex<double> gamma_, 
                          std::complex<double> delta_, std::complex<double> eta_, double z);
{
  HeunCvars result;
 
  HeunCparams p;
  p.q = 0.5*(alpha_*(1 + beta_) - beta_*(1+gamma_) - 2*eta_ - gamma_);
  p.alpha = 0.5*alpha_*(2 + beta_ + gamma_) + delta_;
  p.gamma = beta_ + 1;
  p.delta = gamma_ + 1;
  p.epsilon = alpha_;

  if (z>=1){
    throw std::invalid_argument("HeunC0: z belongs to the branch-cut [1,infty)");
  }
  else {
    findR();
    
    if (abs(z-1)<Heun_proxco){
      std::pair<HeunCvars, HeunCvars> vars_vars1 = HeunCnear1(p,z);
      result = vars_vars1.first();
    }
    else if (abs(epsilon)>1/2)&&(abs(q)<2.5)&&(abs(z)>Heun_proxcoinf_rel*R/(abs(eps)+abs(epsilon))) {
      std::pair<HeunCvars, HeunCvars> vars1_vars = HeunCfaraway(p,z);
      result = vars1_vars.second();
    }
    else {
      result = HeunC0(p,z);
    }
    return result; 
  }
}

inline HeunCvars compute_s(std::complex<double> alpha_, std::complex<double> beta_, std::complex<double> gamma_, 
                          std::complex<double> delta_, std::complex<double> eta_, double z);
{
  HeunCvars result;
 
  HeunCparams p;
  p.q = 0.5*(alpha_*(1 + beta_) - beta_*(1+gamma_) - 2*eta_ - gamma_);
  p.alpha = 0.5*alpha_*(2 + beta_ + gamma_) + delta_;
  p.gamma = beta_ + 1;
  p.delta = gamma_ + 1;
  p.epsilon = alpha_;

  if (z>=1) {
    throw std::invalid_argument("HeunCfaraway: z belongs to the branch-cut [1,infty)");
  }
  else {
    findR(R, N);

    if (abs(z-1)<Heun_proxco){
      std::pair<HeunCvars, HeunCvars> vars_vars1 = HeunCnear1(p,z);
      result = vars_vars1.first();
    }
    else if (abs(epsilon)>1/2)&&(abs(q)<2.5)&&(abs(z)>Heun_proxcoinf_rel*R/(abs(eps)+abs(epsilon))) {
      std::pair<HeunCvars, HeunCvars> vars1_vars = HeunCfaraway(p,z);
      result = vars1_vars.second();
    }
    else {
      result = HeunCs0(p,z);
    }
    return result;
  }
}

#endif /* HEUNCCOMPUTE_IMPL_HPP_ */
