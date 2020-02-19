#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCS0_IMPL_HPP_
#define HEUNCS0_IMPL_HPP_

// confluent Heun function,
// the second local solution
// with branch-cut (1,+\infinity)
// HeunCs(z) = z^(1-p.gamma)*h(z), where h(0)=1, 
// h'(0)=(-q+(1-p.gamma)*(p.delta-p.epsilon))/(2-p.gamma) for p.gamma not equal to 1, 2
// h'(z)/log(z) -> -q+(1-p.gamma)*(p.delta-p.epsilon) as z\to0 for p.gamma=2
// and
// HeunCs(z) \sim log(z) - q * z * log(z) +   as z\to0 for p.gamma=1
//
//
// Usage:
// [val,result.dval,err,numb,wrnmsg] = HeunCs00(q,p.alpha,p.gamma,p.delta,p.epsilon,z)
//
// Returned parameters:
// val is the value of the confluent Heun function
// dval is the value of z-derivative of the confluent Heun function
// err is the estimatedresult.error
// numb is the total result.number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 09 January 2018
//

// the second local solution at z=0 (see HeunCs00)
//
// computed by a consequence of power expansions
inline HeunCvars HeunCs0(HeunCparams p,double z){
  
  HeunCvars result;

  if (z>=1){
    throw std::invalid_argument("HeunC0: z belongs to the branch-cut [1,infty)");
  }
  else {
    bool expgrow = std::real(-p.epsilon*z)>0;
    HeunCparams p1 = p;
    if expgrow {
      p1.q = p.q - p.epsilon * p.gamma;
      p1.alpha = p.alpha - p.epsilon * (p.gamma+p.delta);
      p1.epsilon = -p.epsilon;
    } 
    
    if (abs(z)<Heun_cont_coef){
      result = HeunCs00(p,z);
    }
    else {
      double z0 = Heun_cont_coef*z/abs(z);
      HeunCvars result0 = HeunCs00(p1,z0);
      HeunCvars result1 = HeunCconnect(p,z,z0,result0.val,result0.dval,R);
      result.numb = result0.numb + result1.numb;
      result.err = result0.err + result1.err;
    }
    if expgrow {
      result.val = result.val * exp(p.epsilon*z);
      result.dval = (p.epsilon*result.val + result.dval) * exp(p.epsilon*z);
      result.err = result.err * abs(exp(p.epsilon*z));
    }
    return result;
  }
}

// solution at z ~ 0
// |z| should not exceed the convergency radius 1
inline HeunCvars HeunCs00(HeunCparams p,double z)
{
  HeunCvars result;
  if (std::abs(z)>=1){
	throw std::invalid_argument("HeunCs00: z is outside the |z|<1 radius of convergence");
  }

  else {
    if (std::abs(p.gamma-1)<eps){
      if ( z==0 ){
       result.val= INFINITY; result.dval = INFINITY;
       result.err = nan; result.numb = 1;
      }
      else {
        result = HeunCs00gamma1(p,z);
      }
  
    else {
      HeunCparams p1;
      p1 = p;
      p1.q = p.q + (p.gamma-1)*(p.delta-p.epsilon);
      p1.alpha = p.alpha+p.epsilon*(1-p.gamma);
      p1.gamma = 2-p.gamma;
      HeunCvars H0 = HeunC00(p1,z);
      result.val= pow(z,(1-p.gamma)*H0.val);
      result.dval = (1-p.gamma)*pow(z,(-p.gamma)*H0.val) + pow(z,(1-p.gamma)*H0.dval);
      if ( isinf(result.val) || isinf(result.dval) ){
         result.err = nan;
      }
      else {
         result.err = std::abs(pow(z,(1-p.gamma))*H0.err);
      }
    }
    return result; 
  }
}

// confluent Heun function, second local solution at z=0, p.gamma = 1
//
inline HeunCvars HeunCs00gamma1(HeunCparams p,double z)
{  
  HeunCvars result;

  // declare iteration variables
  std::complex<double> L1 = 0, dL1 = 0, ddL1 = 0, dm1 = 0, dm2 = nan, ckm0 = nan, ckm1 = 0, ckm2 = 0; 
  std::complex<double> L2 = 1, dL2 = 0, ddL2 = 0, skm2 = 0, skm1 = 1, dsm1 = 0, dsm2 = nan, skm0 = nan;
  std::complex<double> ddval;
  int k = 1;

  while ( (k<=Heun_klimit) && ( (dsm2!=dsm1) || (std::abs(skm0)>eps) || (dm2!=dm1) || (std::abs(ckm0)>eps) ) ){

    skm0 = (skm1*z*(-q+(k-1)*(-p.epsilon+p.delta+k-1)) + skm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*k);

    ckm0 = (ckm1*z*(-q+(k-1)*(-p.epsilon+p.delta+k-1)) + ckm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*k)+
	   (skm0*2 + skm1*z*(p.epsilon/k-p.delta/k-2+2/k))/k + skm2*(z*z)*p.epsilon/(k*k);

    L1 = L1+ckm0; dL1 = dm1+k*ckm0/z; ddL1 = ddL1+k*(k-1)*ckm0/(z*z);
    ckm2 = ckm1; ckm1 = ckm0;
    dm2 = dm1; dm1 = dL1;
    
    L2 = L2+skm0; dL2 = dsm1+k*skm0/z; ddL2 = ddL2+k*(k-1)*skm0/(z*z);
    skm2 = skm1; skm1 = skm0;
    dsm2 = dsm1; dsm1 = dL2;
    k += 1;
  }

  result.numb = k-1;
  result.val = L1 + std::log(z) * L2;
  result.dval = dL1 + std::log(z) * dL2 + L2/z;
  ddval = ddL1 - L2/(z*z) + 2*dL2/z + std::log(z) * ddL2;

  if ( isinf(result.val) || isinf(result.dval) || isnan(result.val) || isnan(result.dval) ){
     throw std::runtime_error("HeunCs00gamma1: failed convergence of recurrence and summation"); 
  }
  else {
    std::complex<double> val2, val3;
    double err1;
    if (p.q-p.alpha*z!=0){
  
      val2 = ( z*(z-1)*ddval+(z-1+p.delta*z+p.epsilon*z*(z-1))*result.dval) / (p.q-p.alpha*z);
    
      val3 = ((dL2*p.epsilon+ddL2)*(z*z)*log(z)+(dL2*(-p.epsilon+p.delta+1)-ddL2)*z*log(z)-dL2*log(z)+ 
             (dL1*p.epsilon+ddL1)*(z*z)+(dL1*(-p.epsilon+p.delta+1)+L2*p.epsilon-ddL1+2*dL2)*z-L2*p.epsilon+ 
             L2*p.delta-2*dL2-dL1) / (p.q-p.alpha*z);
             
     err1 = min(std::abs(result.val-val2),std::abs(result.val-val3));   
    else {
     err1 = INFINITY;
    }
    if (std::abs(p.q-p.alpha*z)<0.01)||(err1<eps){
     double err2 = std::abs(ckm0)*sqrt(result.numb) + std::abs(L1)*eps*result.numb + 
             std::abs(log(z)) * ( std::abs(skm0)*sqrt(result.numb) + std::abs(L2)*eps*result.numb );           
     result.err = err2+min(err1,err2);
    }
    else {
     result.err =result.err1;
    }
    return result;
  }
}

#endif /* HEUNCS0_IMPL_HPP_ */
