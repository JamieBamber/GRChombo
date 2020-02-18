// confluent Heun function, a solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
//
// asymptotic expansion at z=infinity,
// the second solution, including exponential factor
//
// Usage:
// [val,dval,err,numb,wrnmsg,valwoexp,dvalwoexp,errwoexp] = HeunCinfB(q,alpha,gamma,delta,epsilon,z)
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of the summed series terms
// wrnmsg is a warning message:
//   it is empty if computations are ok
//   otherwise it is a diagnostic message and the function returns val, dval = NaN
//
// the following values are also returned:
//
// valwoexp = val * exp(epsilon*z)
// dvalwoexp = dval * exp(epsilon*z)
// errwoexp = err * abs(exp(epsilon*z))
//
// Oleg V. Motygin, copyright 2017-2018, license: GNU GPL v3
//
// 20 December 2017
//

//function [val,dval,err,numb,wrnmsg,valwoexp,dvalwoexp,errwoexp] = HeunCinfB(q,alpha,gamma,delta,epsilon,z)

HeunCvars HeunCinfB(HeunCparams p, double z)
{  
  HeunCvars result0, result;
  HeunCparams p0 = p;
  p0.q = p.q - p.epsilon*p.gamma;
  p0.alpha = p.alpha - p.epsilon*(p.gamma + p.delta);
  p0.epsilon = -p.epsilon;

  result0 = HeunCinfA(p0,z);
  result = result0;  

  //valwoexp = val0;
  //dvalwoexp = -epsilon * val0 + dval0;
  //errwoexp = err0;
  
  result.val = exp(-p.epsilon*z) * result0.val;
  result.dval = exp(-p.epsilon*z) * (-p.epsilon * result0.val + result0.dval);
  result.err = abs(exp(-p.epsilon*z)) * result0.err;
  
  return result;
}

    
