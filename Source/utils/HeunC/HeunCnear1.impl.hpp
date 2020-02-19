#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNCNEAR1_IMPL_HPP_
#define HEUNCNEAR1_IMPL_HPP_

// confluent Heun function
//
// computation near z=1, by analytic continuation from the point
//
// assumed that z is not equal to 0
//
// computes both the first local solution (see HeunC00),
// and the second local solution (see HeunCs0)
//
// Usage:
// [val1,dval1,err1,val2,dval2,err2,numb,wrnmsg,val1woexp,dval1woexp,err1woexp,val2woexp,dval2woexp,err2woexp] = HeunCnear1(q,alpha,gamma,delta,epsilon,z)
//
// Returned parameters:
// val1 is the value of the Heun function, growing from the first local solution at z=0
// dval1 is the value of z-derivative of the Heun function
// err1 is the estimated error
// val2 is the value of the Heun function, growing from the second local solution at z=0
// dval2 is the value of z-derivative of the Heun function
// err2 is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 March 2018
//

inline std::pair<HeunCvars, HeunCvars> HeunCnear1(HeunCparams p,double z)
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

#endif /*  HEUNCNEAR1_IMPL_HPP_ */
