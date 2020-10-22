#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCJOIN_IMPL_HPP_
#define HEUNCJOIN_IMPL_HPP_

// for confluent Heun function, a solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
//
// HeunCjoin0inf finds connection coefficients C0, Cs, such that
// C0 * HeunC00(z) + Cs * HeunCs00(z) analytically continues to
// the first, power solution at infinity \exp(i\theta) infty
// (see HeunCinfA)
//
// HeunCjoin10 finds matrix C of connection coefficients, such that
// C(1,1) * HeunC1(z) + C(1,2) * HeunCs1(z) analytically continues to
// the first local solution at z=0 (HeunC0), and
// C(2,1) * HeunC1(z) + C(2,2) * HeunCs1(z) continues to the second
// local solution at z=0 (HeunCs0)
//
// Usage:
// [C10,err,numb,warningmessage] = HeunCjoin10(q,alpha,gamma,delta,epsilon)
//
// Returned parameters:
// C10 is the matrix of connection coefficients
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 March 2018
//

inline ConnectionVars HeunC::HeunCjoin0inf(HeunCparams p,bool aux)
{
  ConnectionVars result;
  bool consts_known = false;

  result = extrdatfromsav(p, savedata0inf, consts_known);

  if consts_known {
    result.numb = 0;
  }
  else {
    HeunCvars result, varsinf, varsJinf, varsJ0, varsJs;

    findR();

    R0 = R/(abs(eps)+abs(epsilon));

    infpt = -2 * R0;
    joinpt = -min(1,R0);

    varsinf = HeunCinfA(p,infpt);       // value at "infinity" point
    varsJinf = HeunCconnect(p,joinpt,infpt,result.val,result.dval); //

    varsJ0 = HeunC0(p,joinpt,aux); // first solution at join point near zero 
    varsJs = HeunCs0(p,joinpt);         // second solution at join point near zero

    result.err = varsinf.err + varsJinf.err + varsJ0.err + varsJs.err;
    result.numb = varsinf.numb + varsJinf.numbJ + varsJ0.numb + varsJs.numb;

    Matrix<std::complex<double>> m, b;
    m.Init(varsJ0.val,varsJs.val, varsJ0.dval,varsJs.dval);
    b.Init(varsJinf.val, 0, varsJinf.dval, 0);
    result.C10 = (m.inverse().dot(b));

    savedataVars s;
    s.p = p;
    s.Cvars = result;
    keepdattosav(s, savedata0inf);
  }
  return result;
}

inline ConnectionVars HeunC::HeunCjoin10(HeunCparams p)
{
  ConnectionVars result;
  
  bool consts_known = false;
  result = extrdatfromsav(p, savedata10, consts_known);
  
  if consts_known {
    result.numb = 0;
  }
  else {
    double joinpt = 0.5;
    HeunCvars vars0 = HeunC0(p,joinpt);
    HeunCvars vars0s = HeunCs0(p,joinpt);
    HeunCvars vars1 = HeunC1(p,joinpt);
    HeunCvars vars1s = HeunCs1(p,joinpt);

    result.err = vars0.err/(1+abs(vars0.val)) + vars0s.err/(1+abs(vars0s.val)) + vars1.err/(1+abs(vars1.val)) + vars1s.err/(1+abs(vars1s.val));
    result.numb = vars0.numb + vars0s.numb + vars1.numb + vars1s.numb;
  
    Matrix<std::complex<double>> m, b;
    m.Init(vars1.val,vars1s.val, vars1.dval,vars1s.dval);
    b.Init(vars0.val, vars0s.val, vars0.dval, vars0s.dval);
    result.C10 = (m.inverse().dot(b)).transpose();
    result.err += (m.dot((result.C10).transpose())-b).applyFunction(std::abs).sum(); 
    
    savedataVars s;
    s.p = p;
    s.Cvars = result;
    keepdattosav(s, savedata10);
  }
  return result;
}

HeunCvars HeunC::HeunC1(HeunCparams p, double z){
    HeunCvars result;
    HeunCparams p0;
    p0 = p;
    p0.q = p0.q - p.alpha;
    p0.alpha = -p.alpha;
    p0.epsilon = -p.epsilon; 
    result = HeunC0(p0,1-z);
    result.dval = -result.dval;
    return result;
}
   
HeunCvars HeunC::HeunCs1(HeunCparams p, double z){
    HeunCvars result; 
    HeunCparams p0; 
    p0 = p; 
    p0.q = p0.q - p.alpha; 
    p0.alpha = -p.alpha; 
    p0.epsilon = -p.epsilon; 
    result = HeunCs0(p0,1-z);
    result.dval = -result.dval;
    return result;
}

inline ConnectionVars HeunC::extrdatfromsav(HeunCparams p, std::vector<savedataVars> savedata, bool& consts_known){
  ConnectionVars result;
  result.err = nan; result.numb = 0; 
  savedataVars s;

  if savedata.size() !=0 {
    for(int k=1; k < savedata.size(); k++){
        s = savedata[k];
        if (s.p == p) {
        	result = s.Cvars;        
        	consts_known = "true";
        	break;
      	}
    }
  }
  return result;
}

inline void HeunC::keepdattosav(savedataVars s, std::vector<savedataVars>& savedata);
  if length(savedata)<=Heun_memlimit
  {
    savedata.pushback(s)
  }
  if length(savedata) > Heun_memlimit
  {
    savedata.erase(s.begin()); // remove first element
  }
  savedata.pushback(s); // store new element  
}

#endif /* HEUNCJOIN_IMPL_HPP_ */
