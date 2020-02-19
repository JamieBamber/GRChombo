#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCFARAWAY_IMPL_HPP_
#define HEUNCFARAWAY_IMPL_HPP_

/*
Depends on:

HeunCconnect
HeunCjoin0infA
HeunCjoin0infB
HeunCinfA
HeunCinfB

*/
// confluent Heun function, a solution of the equation
// HeunC""(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC"(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
//
// computation for  sufficiently large |z|, by analytic continuation from infinity, and for z near 1
//
// computes both the first at z=0 local solution (see HeunC00) and the second at z=0 local solution (see HeunCs0)
//
// It is assumed that epsilon \neq 0 !
//
// Usage:
// [val1,dval1,result1.err,result2.val,result2.dval,result2.err,numb,result1.warningmessage,val1woexp,dval1woexp,result1.errwoexp,result2.valwoexp,result2.dvalwoexp,result2.errwoexp] = HeunCfaraway(q,alpha,gamma,delta,epsilon,z)
//
// Returned parameters:
// val1 is the value of the Heun function, growing from the first local solution at z=0
// dval1 is the value of z-derivative of the Heun function
// result1.err is the estimated error
// result2.val is the value of the Heun function, growing from the second local solution at z=0
// result2.dval is the value of z-derivative of the Heun function
// result2.err is the estimated error
// numb is the number of power series terms needed for the evaluation
// result1.warningmessage is a warning message:
//   it is empty if computations are ok
//   otherwise it is a diagnostic message and the function returns val*, dval* = NaN
//
// val1woexp = val1 * exp(epsilon*z)
// dval1woexp = dval1 * exp(epsilon*z)
// result1.errwoexp = result1.err * abs(exp(epsilon*z))
//
// result2.valwoexp = result2.val * exp(epsilon*z)
// result2.dvalwoexp = result2.dval * exp(epsilon*z)
// result2.errwoexp = result2.err * abs(exp(epsilon*z))
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 26 March 2018
//

//
// power series solution for z near 1
inline std::pair<HeunCvars, HeunCvars> HeunC::HeunCnear1(HeunCparams p,double z)
{
  HeunCvars vars1, vars2;
  MakeNan(vars1);
  MakeNan(vars2);

  ConnectionVars m_vars = HeunCjoin10(p);
  
  HeunCvars vars1f = HeunC1(q,alpha,gamma,delta,epsilon,z);
  HeunCvars vars1s = HeunCs1(q,alpha,gamma,delta,epsilon,z);

  vars1.numb = m_vars.numb + vars1f.numb + vars1s.numb;
  vars2.numb = vars1.numb;
    
  vars1.val = m_vars.C10[0, 0]*vars1f.val + m_vars.C10[0, 1]*vars1s.val;
  vars1.dval = m_vars.C10[0, 0]*vars1f.dval + m_vars.C10[0, 1]*vars1s.dval;
  vars1.err = std::abs(m_vars.C10[0, 0]*vars1f.err) + std::abs(m_vars.C10[0, 1]*vars1s.err) + m_vars.err;

  vars2.val = m_vars.C10[1, 0]*vars1f.val + m_vars.C10[1, 1]*vars1s.val;
  vars2.dval = m_vars.C10[1, 0]*vars1f.dval + m_vars.C10[1, 1]*vars1s.dval;
  vars2.err = std::abs(m_vars.C10[1, 0]*vars1f.err) + std::abs(m_vars.C10[1, 1]*vars1s.err) + m_vars.err;

  std::pair output(vars1, vars2);
  return output;
}

// for large |z|
inline std::pair<HeunCvars, HeunCvars> HeunC::HeunCfaraway(HeunCparams p,double z)
{
  HeunCvars result1, result2;

  if (z>=1) {
    throw std::invalid_argument("HeunCfaraway: z belongs to the branch-cut [1,infty)");
  }
  else {
    std::complex<double> aSt = 1i/epsilon;
    if (MyMath::sgn(std::imag(aSt)) < 0{
      aSt = -aSt;
    }

    HeunCparams pB = p;
    pB.q = p.q-p.epsilon*p.gamma;
    pB.alpha = p.alpha-p.epsilon*(p.gamma+p.delta);
    pB.epsilon = -p.epsilon;

    ConnectionVars CA = HeunCjoin0infA(p);
    ConnectionVars CB = HeunCjoin0infA(pB);

    findR();

    double infpt = -max(1,R/(abs(eps)+abs(epsilon)));

    if abs(z)>abs(infpt) {
      
      HeunCvars varsA = HeunCinfA(p,z);
      HeunCvars varsB = HeunCinfA(pB,z);
    
      result1.numb = CA.numb + CB.numb + varsA.numb + varsB.numb;
      result1.err = CA.err + CB.err + varsA.err + varsB.err;
      result2.numb = result1.numb;    
      result2.err = result1.err;
    } 
    else { 
      HeunCvars varsinfA = HeunCinfA(p,z);
      HeunCvars varsA = HeunCconnect(p,z,infpt,varsinfA.val,varsinfA.dval, R);

      HeunCvars varsinfB = HeunCinfA(pB,z);
      HeunCvars varsB = HeunCconnect(pB,z,infpt,varsinfA.val,varsinfA.dval, R);
    
      result1.numb = varsinfA.numb + varsinfB.numb + varsA.numb + varsB.numb;
      result1.err = varsinfA.err + varsinfB.err + varsA.err + varsB.err;
      result2.err = result1.err;
    }
    Matrix<std::complex<double>> m;
    m.Init(CA[0][0],CA[1][0],CB[0][0],CB[1][0]);
    double co = m.cond();

    result1.val = m[0][0] * varsA.val + m[0][1] * exp(-p.epsilon*z) * vasB.val;
    result1.dval = m[0][0] * varsA.dval + m[0][1] * exp(-p.epsilon*z) * (-p.epsilon * vasB.val + varsB.dval);
    result1.err = co * (abs(m[0][0]) * varsA.err + abs(m[0][1]) * abs(exp(-p.epsilon*z)) * varsB.err);
    
    result2.val = m[1][0] * varsA.val + m[1][1] * exp(-p.epsilon*z) * vasB.val;
    result2.dval = m[1][0] * varsA.dval + m[1][1] * exp(-p.epsilon*z) * (-p.epsilon * vasB.val + varsB.dval);
    result2.err = co * (abs(m[1][0]) * varsA.err + abs(m[1][1]) * abs(exp(-p.epsilon*z)) * varsB.err);
    
    std::pair output(result1, result2);
    return output;
    }
  }
}

#endif /* HEUNCFARAWAY_IMPL_HPP */
