#if !defined(MAIN_HEUNC_HPP_)
#error "This file should only be included through MainHeunC.hpp"
#endif

#ifndef HEUNCFROMZ0_IMPL_HPP_
#define HEUNCFROMZ0_IMPL_HPP_

// confluent Heun function, a solution of the ep.quation
// HeunC""(z)+(p.gamma/z+p.delta/(z-1)+p.epsilon)*HeunC"(z)+(p.alpha*z-p.q)/(z*(z-1))*HeunC(z) = 0
// computed at z by power series about Z0 for the given values H(Z0)=H0, H"(Z0)=dH0 
//
// it is assumed that z, Z0 are not equal to 0, 1 and |z-Z0| < min{|Z0|,|Z0-1|}
//
// Usage:
// [val,dval,err,numb,result.warningmessage] = HeunCfromZ0(p.q,p.alpha,p.gamma,p.delta,p.epsilon,z,Z0,H0,dH0)
//
// Returned parameters:
// val is the value of the confluent Heun function at point z
// dval is the value of z-derivative of the Heun function at point z
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 09 January 2018
//
inline HeunCvars HeunCfromZ0(HeunCparams p,double z,double Z0,std::complex<double> H0,std::complex<double> dH0)
{
  HeunCvars result;

  double R_ = min(abs(Z0),abs(Z0-1));
  
  if (abs(z-Z0)>=R_) {
    throw std::invalid_argument("HeunCfromZ0: z is out of the convergence radius"); 
  }
  else if ((abs(z-1)<eps) || (abs(Z0-1)<eps)) {
   throw std::invalid_argument("HeunCfromZ0: z or Z0 is too close to the singular points"); 
  }
  else if (z==Z0) {
   result.val= H0; result.dval = dH0; 
   result.err= 0; result.numb = 0;
  } 
  else {
    double zeta = z-Z0;
    // iteration variables
    std::complex<double> ckm0, ckm1, ckm2, ckm3;
    std::complex<double> dm1, dm2, vm1, vm2;  
    std::complex<double> ddval;
    ckm3 = H0; 
    ckm2 = dH0*zeta; 

    // initialise with long recursion relation
    ckm1 = (ckm2*zeta*(2-1)*(p.epsilon*(Z0*Z0)+(p.gamma-p.epsilon+p.delta+2*(2-2))*Z0-p.gamma-2+2)+
        ckm3*pow(zeta,2)*((2*(2-2)*p.epsilon+p.alpha)*Z0-p.q+(2-2)*(p.gamma-p.epsilon+p.delta+2-3));

    result.val= ckm3 + ckm2 + ckm1; 
    vm1 = val; vm2 = nan;
    dm2 = dH0; dm1 = dH0 + 2*ckm1/zeta; 
    result.dval = dm1;
    ddval = 2*ckm1/pow(zeta,2); 
  
    int k = 3; 
    ckm0 = 1;
    
    while (k<=Heun_klimit) && ( ( vm2!=vm1 ) || ( dm2!=dm1 ) || (abs(ckm0)>eps) ) {
      // long recursion relation
      ckm0 = (ckm1*zeta*(k-1)*(p.epsilon*(Z0*Z0)+(p.gamma-p.epsilon+p.delta+2*(k-2))*Z0-p.gamma-k+2)+ 
             ckm2*pow(zeta,2)*((2*(k-2)*p.epsilon+p.alpha)*Z0-p.q+(k-2)*(p.gamma-p.epsilon+p.delta+k-3))+ 
             ckm3*pow(zeta,3)*((k-3)*p.epsilon+p.alpha)) / (Z0*(Z0-1)*(1-k)*k);
      result.val += ckm0; 
      result.dval = dm1 + k*ckm0/zeta;
      ddval += k*(k-1)*ckm0/pow(zeta,2);
      ckm3 = ckm2; 
      ckm2 = ckm1; 
      ckm1 = ckm0;
      vm2 = vm1; vm1 = result.val;
      dm2 = dm1; dm1 = result.dval;
      k++;
    }
    
    result.numb = k-1;

    if ( isinf(val) || isinf(dval) || isnan(val) || isnan(dval) ) {
      throw std::runtime_error("HeunCfromZ0: failed convergence of recurrence and summation"); 
    }
    else {
      std::complex<double> val2;
      double err1, err2;
      if (p.q-p.alpha*z != 0) {
        val2 = ( z*(z-1)*ddval+(p.gamma*(z-1)+p.delta*z+p.epsilon*z*(z-1))*result.dval ) / (p.q-p.alpha*z);
        err1 = abs(result.val-val2);
      }
      else {
        err1 = INFINITY;
      }
      if abs(p.q-p.alpha*z)<0.01 {
        err2 = abs(ckm0) * sp.qrt(result.numb) + abs(result.val) * eps * result.numb;
        result.err=  min(err1,err2);
      }
      else {
       result.err = err1;
      }
    }
  }
  return result; 
}

#endif /* HEUNCFROMZ0_IMPL_HPP_ */
