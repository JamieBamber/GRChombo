// confluent Heun function, a solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
// the second local solution at z=0 (see HeunCs00)
//
// computed by a consequence of power expansions with improvement near poits z=1 and z=\infty
//
// it is assumed that z does not belong to the branch-cuts (-\infty,0] and [1,\infty)
//
// Usage:
// [val,dval,err,numb,wrnmsg,valwoexp,dvalwoexp,errwoexp] = HeunCs(p,z)
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
// valwoexp = val * exp(epsilon*z)
// dvalwoexp = dval * exp(epsilon*z)
// errwoexp = err * abs(exp(epsilon*z))
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 26 January 2018
//
HeunCvars HeunCs(HeunCparams p, double z)
{ 
  HeunCvars result;
  global Heun_proxco Heun_proxcoinf_rel;  

  if isempty(Heun_proxco) || isempty(Heun_proxcoinf_rel){
    HeunOpts();
  }

  if (z>=1) {
    throw std::invalid_argument("HeunCfaraway: z belongs to the branch-cut [1,\infty)");
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


