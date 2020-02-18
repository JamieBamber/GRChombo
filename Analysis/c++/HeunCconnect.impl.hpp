#if !defined(MAIN_HEUNC_HPP_)
#error "This file should only be included through MainHeunC.hpp"
#endif

#ifndef HEUNCCONNECT_IMPL_HPP_
#define HEUNCONNECT_IMPL_HPP_

//
// R0 is an optional parameter, step size's guess
//
// R is the size of the last used step
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 09 January 2018
//

#include <utility>

HeunCvars HeunCconnect(HeunCparams p,double z, double z0,std::complex<double> H0,std::complex<double> dH0,bool varargin=false, double& R, double R0=0)
{
  HeunCvars result;
  result.warningmessage = '';

  if (z==0)||(z==1)||(z0==0)||(z0==1)){
    result.warningmessage = "HeunCconnect: assumed that z, z0 are not equal to 0, 1, and Im(z)*Im(z0)>0; ';
    result.val = nan; result.dval = nan; result.err = nan; result.numb = nan;
  }
  else {

    global Heun_cont_coef Heun_optserterms;
  
    if isempty(Heun_cont_coef) || isempty(Heun_optserterms){
      HeunOpts();
    }
    
    int positivity = 2*(z >= z0) - 1;
    bool insearch = true, failure = false;
    double Rmax;    

    if varargin {
	Rmax = R0;
    } 
    else {
      Rmax = 12/(1+std::abs(epsilon));
    }

    double R = min(Rmax,min(std::abs(z0),std::abs(z0-1)*Heun_cont_coef);

    // first set of iteration variables
    bool Rtuned = false;
    int iter = 1;
    double z_ = z; //iteration version of z
    double z1;    

    while !Rtuned {
      if (std::abs(z_-z0) <= R) {
        z1 = z_;
      }
      else {
        z1 = z0 + R * positivity;
      }
      
      z_ = z1;
      result = HeunCfromZ0(p,z_,z0,H0,dH0);

      if (result.warningmessage != "") {
        result.warningmessage = "HeunCconnect: problem invoking HeunCfromZ0()";
        failure = true;
        break;      
      }
	
      Rtuned = (result.err < 5*eps) && (result.numb < Heun_optserterms) || (iter>5) || (result.numb<=8);
      
      if !Rtuned {
        R = R / std::max(result.err/(5*eps), result.numb/Heun_optserterms);
      }

      insearch = !(Rtuned && (z_==z1));
      iter = iter+1; 
    }

    //second set of iteration variables
    double errsum;
    int numbsum;
    std::complex<double> H0_, dH0_; //iteration versions of H0, dH0
    double z0_; //iteration version of z0

    z0_ = z1;
    errsum = result.err; 
    numbsum = result.numb; 
    HeunCvars result_; // iteration version of result
    H0_ = result.val; dH0_ = result.dval;
    
    while insearch && !failure {

      R = min(R,min(abs(z0_),abs(z0_-1))*Heun_cont_coef);
      if abs(z_-z0_) <= R {
        z1 = z_; insearch = false;
      }
      else {
        z1 = z0_ + R * positivity;
      }
      
      result_ = HeunCfromZ0(p,z_,z0_,H0_,dH0_);
      H0_ = result_.val;
      dH0_ = result_.dval;

      if result_.warningmessage != "" {
        result.warningmessage = "HeunCconnect: problem invoking HeunCfromZ0";
        failure = true;
        break;
      }
           
      errsum += result_.err;
      numbsum += result_.numb;

      if insearch {
        R = Heun_optserterms * R / (result_.numb + eps);
      }
      
      z0_ = z1;
        
    }
  
    result.numb = numbsum; 
  
    if failure {
      result.val = nan; result.dval = nan; result.err = nan;
    }
    else {
      result.val = H0_; result.dval = dH0_; result.err = errsum;
    }
    
  }
  return result;
}

# endif /* HEUNCCONNECT_IMPL_HPP */
