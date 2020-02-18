






// confluent Heun function, a solution of the equation
// HeunC''(z)+(p.gamma/z+p.delta/(z-1)+p.epsilon)*HeunC'(z)+(p.alpha*z-q)/(z*(z-1))*HeunC(z) = 0
// the second local solution at z=0 (see HeunCs00)
//
// computed by a consequence of power expansions
//
// it is assumed that z does not belong to the branch-cut [1,\infty)
//
// Usage:
// [val,dval,err,numb,wrnmsg,valwoexp,dvalwoexp,errwoexp] = HeunCs0(p,z)
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
// wrnmsg is a warning message:
//   it is empty if computations are ok
//   otherwise it is a diagnostic message and the function returns val*, dval* = NaN
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 February 2018
//

HeunCvars HeunCs0(HeunCparams p,double z){
  
  HeunCvars result;
  global Heun_cont_coef;
  
  if (Heun_cont_coef==0){
    HeunOpts();
  }

  if (z>=1){
    throw std::invalid_argument("HeunC0: z belongs to the branch-cut [1,\infty)");
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

