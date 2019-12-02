//  (C) Copyright John Maddock 2006.
//  Use, modification and distribution are subject to the
//  Boost Software License, Version 1.0. (See accompanying file
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_MATH_SPECIAL_LEGENDRE_HPP
#define BOOST_MATH_SPECIAL_LEGENDRE_HPP

#ifdef _MSC_VER
#pragma once
#endif

#include <utility>
#include <vector>
#include <boost/math/special_functions/math_fwd.hpp>
#include <boost/math/special_functions/factorials.hpp>
#include <boost/math/tools/roots.hpp>
#include <boost/math/tools/config.hpp>

namespace boost{
namespace math{

// Recurrance relation for legendre P and Q polynomials:
template <class T1, class T2, class T3>
inline typename tools::promote_args<T1, T2, T3>::type
   legendre_next(unsigned l, T1 x, T2 Pl, T3 Plm1)
{
   typedef typename tools::promote_args<T1, T2, T3>::type result_type;
   return ((2 * l + 1) * result_type(x) * result_type(Pl) - l * result_type(Plm1)) / (l + 1);
}

namespace detail{

// Implement Legendre P and Q polynomials via recurrance:
template <class T, class Policy>
T legendre_imp(unsigned l, T x, const Policy& pol, bool second = false)
{
   static const char* function = "boost::math::legrendre_p<%1%>(unsigned, %1%)";
   T p0, p1;
   if(second)
   {
      // A solution of the second kind (Q):
      p0 = (boost::math::log1p(x, pol) - boost::math::log1p(-x, pol)) / 2;
      p1 = x * p0 - 1;
   }
   else
   {
      // A solution of the first kind (P):
      p0 = 1;
      p1 = x;
   }
   if(l == 0)
      return p0;

   unsigned n = 1;

   while(n < l)
   {
      std::swap(p0, p1);
      p1 = boost::math::legendre_next(n, x, p0, p1);
      ++n;
   }
   return p1;
}

template <class T, class Policy>
T legendre_p_prime_imp(unsigned l, T x, const Policy& pol, T* Pn 
#ifdef BOOST_NO_CXX11_NULLPTR
   = 0
#else
   = nullptr
#endif
)
{
   static const char* function = "boost::math::legrendre_p_prime<%1%>(unsigned, %1%)";

   if (l == 0)
    {
        if (Pn)
        {
           *Pn = 1;
        }
        return 0;
    }
    T p0 = 1;
    T p1 = x;
    T p_prime;
    bool odd = l & 1;
    // If the order is odd, we sum all the even polynomials:
    if (odd)
    {
        p_prime = p0;
    }
    else // Otherwise we sum the odd polynomials * (2n+1)
    {
        p_prime = 3*p1;
    }

    unsigned n = 1;
    while(n < l - 1)
    {
       std::swap(p0, p1);
       p1 = boost::math::legendre_next(n, x, p0, p1);
       ++n;
       if (odd)
       {
          p_prime += (2*n+1)*p1;
          odd = false;
       }
       else
       {
           odd = true;
       }
    }
    // This allows us to evaluate the derivative and the function for the same cost.
    if (Pn)
    {
        std::swap(p0, p1);
        *Pn = boost::math::legendre_next(n, x, p0, p1);
    }
    return p_prime;
}

} // namespace detail

template <class T, class Policy>
inline typename boost::enable_if_c<policies::is_policy<Policy>::value, typename tools::promote_args<T>::type>::type
   legendre_p(int l, T x, const Policy& pol)
{
   typedef typename tools::promote_args<T>::type result_type;
   typedef typename policies::evaluation<result_type, Policy>::type value_type;
   static const char* function = "boost::math::legendre_p<%1%>(unsigned, %1%)";
   if(l < 0)
      return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_imp(-l-1, static_cast<value_type>(x), pol, 
false), function);
   return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_imp(l, static_cast<value_type>(x), pol, false), 
function);
}


template <class T, class Policy>
inline typename boost::enable_if_c<policies::is_policy<Policy>::value, typename tools::promote_args<T>::type>::type
   legendre_p_prime(int l, T x, const Policy& pol)
{
   typedef typename tools::promote_args<T>::type result_type;
   typedef typename policies::evaluation<result_type, Policy>::type value_type;
   static const char* function = "boost::math::legendre_p_prime<%1%>(unsigned, %1%)";
   if(l < 0)
      return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_p_prime_imp(-l-1, static_cast<value_type>(x), 
pol), function);
   return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_p_prime_imp(l, static_cast<value_type>(x), pol), 
function);
}

template <class T>
inline typename tools::promote_args<T>::type
   legendre_p(int l, T x)
{
   return boost::math::legendre_p(l, x, policies::policy<>());
}

template <class T>
inline typename tools::promote_args<T>::type
   legendre_p_prime(int l, T x)
{
   return boost::math::legendre_p_prime(l, x, policies::policy<>());
}

template <class T, class Policy>
inline typename boost::enable_if_c<policies::is_policy<Policy>::value, typename tools::promote_args<T>::type>::type
   legendre_q(unsigned l, T x, const Policy& pol)
{
   typedef typename tools::promote_args<T>::type result_type;
   typedef typename policies::evaluation<result_type, Policy>::type value_type;
   return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_imp(l, static_cast<value_type>(x), pol, true), 
"boost::math::legendre_q<%1%>(unsigned, %1%)");
}

template <class T>
inline typename tools::promote_args<T>::type
   legendre_q(unsigned l, T x)
{
   return boost::math::legendre_q(l, x, policies::policy<>());
}

template <class T, class Policy>
inline typename tools::promote_args<T>::type
   legendre_p(int l, int m, T x, const Policy& pol)
{
   typedef typename tools::promote_args<T>::type result_type;
   typedef typename policies::evaluation<result_type, Policy>::type value_type;
   return policies::checked_narrowing_cast<result_type, Policy>(detail::legendre_p_imp(l, m, static_cast<value_type>(x), pol), 
"bost::math::legendre_p<%1%>(int, int, %1%)");
}

template <class T>
inline typename tools::promote_args<T>::type
   legendre_p(int l, int m, T x)
{
   return boost::math::legendre_p(l, m, x, policies::policy<>());
}

} // namespace math
} // namespace boost

#endif // BOOST_MATH_SPECIAL_LEGENDRE_HPP
