#if !defined(HEUNC_HPP_)
#error "This file should only be included through HeunC.hpp"
#endif

#ifndef HEUNC0_IMPL_HPP_
#define HEUNC0_IMPL_HPP_

/* This computes the first local solution around z = 0
*/

// confluent Heun function, the first local solution of the ep.quation
// |z| should not exceed the convergency radius 1
//
// aux is an optional parameter, it only works for p.gamma = 0, -1, -2, ...
// if aux = "yes" then the function is computed as a combination with the second
// solution so as to satisfy
// HeunC00(p.q,p.alpha,p.gamma,p.delta,varp.epsilon;z)=
// exp(-\varp.epsilon z)[HeunC00(p.q-p.epsilon*p.gamma,p.alpha-varp.epsilon(p.gamma+p.delta),p.gamma,p.delta,-varp.epsilon;z)+
// + A * HeunCs00(p.q-p.epsilon*p.gamma,p.alpha-varp.epsilon(p.gamma+p.delta),p.gamma,p.delta,-varp.epsilon;z)]
//
// Returned parameters:
// val is the value of the Heun function
// dval is the value of z-derivative of the Heun function
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 February 2018
//

inline HeunCvars HeunC0(HeunCparams p, double z, bool aux = false){
  
  HeunCvars result;
  
  if (z>=1){
    throw std::invalid_argument("HeunC0: z belongs to the branch-cut [1,\infty)");
  }
  else {
    bool expgrow = false;
    HeunCparams p1 = p;
    if ! aux {
      expgrow = real(-p.epsilon*z)>0;
      if expgrow {
        p1.q = p.q - p.epsilon * gamma;
        p1.alpha = p.alpha - p.epsilon * (gamma+delta);
        p1.epsilon = -p.epsilon;
      }
    }

    if (abs(z)<Heun_cont_coef) {
      result = HeunC00(p1,aux);
    }
    else {
      double z0 = Heun_cont_coef*z/abs(z);
      HeunCvars result0 = HeunC00(p1,z,aux);
      HeunCvars result1 = HeunCconnect(p1,z,z0,result0.val,result0.dval, R);
      result.numb = result0.numb + result1.numb;
      result.err = result0.err + result1.err;
    }
    if expgrow {
      result.val = result.val * exp(p1.epsilon*z);
      result.dval = (p1.epsilon * result.val + result.dval) * exp(p1.epsilon*z);
      result.err = result.err * abs(exp(p1.epsilon*z));
    }
  }
  return result;
}

inline HeunCvars HeunC00(HeunCparams p, double z, bool woexp=false)
{
	// define the result 
	HeunCvars result;

	// check you are in the convergence range
	if (std::abs(z)>=1){
		throw std::invalid_argument("HeunC00: z is out of the convergence radius = 1");
	}
  	else{
    		bool p.gamma_is_negative_integer = (std::imag(p.gamma)==0) && std::abs(std::ceil(std::real(p.gamma)-5*eps)+std::abs(p.gamma))<5*eps;
		if p.gamma_is_negative_integer {
	     		result = HeunC00log(p, z);
	      		if woexp {
	          		co = findcoef4HeunCs(p);
	          		HeunCvars result_s = HeunCs00(p, z);
		          	result.val = result.val - co * result_s.val;
		          	result.dval = result.dval - co * result_s.dval;
		          	result.err = result.err + abs(co) * result_s.err;
		          	result.numb = result.numb + result_s.numb;
			}
		}
    		else{
      		result = HeunC00gen(p, z);
		}
	}
	return result;
}

// confluent Heun function expansion for |z| < 1, gamma is not equal to 0, -1, -2, ...
inline HeunCvars HeunC00gen(HeunCparams p, double z)
{
	HeunCvars result;

	if (z==0) {
    		result.val = 1;
		result.dval = -p.q/p.gamma;
    		result.err = 0;
		numb = 1;
  	}
  	else {
    		// recursion relation variables
    		std::complex<double> ckm2 = 1; 
		std::complex<double> ckm1 = -z*p.q/p.gamma;
    		std::complex<double> val = ckm2+ckm1; 
		std::complex<double> vm1 = result.val; 
		std::complex<double> vm2 = NaN;
    		result.dval = -p.q/p.gamma; 
		std::complex<double> dm1 = dval; 
		std::complex<double> dm2 = NaN;
    		std::complex<double> ddval = 0; 
    		std::int k = 2; 
		std::complex<double> ckm0 = 1;
		// perform recursion
    		while ( (k<=Heun_klimit) && ( (vm2 != vm1) || (dm2 != dm1) || (std::abs(ckm0)>eps) ) ) {
			ckm0 = (ckm1*z*(-p.q+(k-1)*(p.gamma-p.epsilon+p.delta+k-2)) + ckm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*(p.gamma+k-1));
		      	result.val = result.val + ckm0; 
			result.dval = dm1 + k*ckm0/z;
      			ddval = ddval + k*(k-1)*ckm0/(z*z);
      			ckm2 = ckm1; 
			ckm1 = ckm0;
      			vm2 = vm1; 
			vm1 = val;
      			dm2 = dm1; 
			dm1 = dval;
      			k = k+1;
		}
    		result.numb = k-1;

		if ( std::isinf(result.val) || std::isinf(result.dval) || std::isnan(result.val) || std::isnan(result.dval) ) {
			throw std::runtime_error("HeunC00: failed convergence of recurrence and summation"); 
      		}
    		else {
			std::double err1;
			std::complex<double> val2;
			if (p.q-p.alpha*z != 0) {
        			val2 = ( z*(z-1)*ddval+(p.gamma*(z-1)+p.delta*z+p.epsilon*z*(z-1))*result.dval ) / (p.q-p.alpha*z);
        			err1 = abs(result.val-val2);
      			}
			else {
        			err1 = INFINITY;
      			}
      			if (std::abs(p.q-p.alpha*z)<0.01) {
				std::double err2;
        			err2 = abs(ckm0) * sp.qrt(result.numb) + eps * numb * abs(result.val);
        			result.err =  min(err1,err2);
      			}
			else {		
        			result.err = err1;
      			}
		}
  	}
	return result;
}

// confluent Heun function, p.gamma = 0, -1, -2, ...
inline HeunCvars HeunC00log(HeunCparams p, double z) {
	HeunCvars result;
  	
	if (z==0) {
    		result.val = 1; 
    		result.err = 0; 
		result.numb = 1;
    		if (std::abs(p.gamma)<eps) {
     			result.dval = INFINITY;
    		}
		else {
      		result.dval = -p.q/p.gamma;
    		}
  	}
	else {
    		std::int N = std::round(1-std::real(p.gamma));
  		
		// recursion relation variables
    		std::complex<double> L1 = 1, dL1 = 0, ddL1 = 0;
		std::complex<double> L2 = 0, dL2 = 0, ddL2 = 0;
		std::complex<double> L3, dL3, ddL3; 
		std::complex<double> ckm0 = 1, ckm1 = 1, ckm2 = 0;
		std::complex<double> dm1, dm2, skm0, skm1, skm2 = 0;
		std::complex<double> dsm1, dsm2;

		for(int k=1; k<N; k++) {
			ckm0 = (ckm1*z*(-p.q+(k-1)*(p.gamma-p.epsilon+p.delta+k-2)) + ckm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*(p.gamma+k-1));
	      		L1 = L1+ckm0; 
			dL1 = dL1+k*ckm0/z; 
			ddL1 = ddL1+k*(k-1)*ckm0/(z*z);
	      		ckm2 = ckm1; 
			ckm1 = ckm0; 
	    	}
	       
                std::complex<double> sN = (ckm1*z*(p.q+p.gamma*(p.delta-p.epsilon-1)) + ckm2*(z*z)*(p.epsilon*(p.gamma+1)-p.alpha))/(p.gamma-1);

		dm1 = dL2; 
		dm2 = NaN;
	    	ckm1 = 0; 
		ckm2 = ckm0; 
	    	L3 = sN; 
		skm1 = sN;
	    	dL3 = N*sN/z; 
		ddL3 = N*(N-1)*sN/(z*z); 
	    	dsm1 = dL3; 
		dsm2 = NaN; 
		skm0 = NaN;
	    
	    	int k = N+1;

	    	while ( (k<=Heun_klimit) && ( (dsm2!=dsm1) || (std::abs(skm0)>eps) || (dm2!=dm1) || (std::abs(ckm0)>eps) ) ) {
	      		skm0 = (skm1*z*(-p.q+(k-1)*(p.gamma-p.epsilon+p.delta+k-2)) + skm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*(p.gamma+k-1));
	      		ckm0 = (ckm1*z*(-p.q+(k-1)*(p.gamma-p.epsilon+p.delta+k-2)) + ckm2*(z*z)*((k-2)*p.epsilon+p.alpha))/(k*(p.gamma+k-1)) +
				(-skm0*(p.gamma+2*k-1)+skm1*z*(p.gamma-p.epsilon+p.delta+2*k-3)+skm2*(z*z)*p.epsilon)/(k*(p.gamma+k-1));
	      		L2 = L2+ckm0; 
			dL2 = dm1+k*ckm0/z; 
			ddL2 = ddL2+k*(k-1)*ckm0/(z*z);
			ckm2 = ckm1; 
			ckm1 = ckm0;
			dm2 = dm1; 
			dm1 = dL2;

	      		L3 = L3+skm0; dL3 = dsm1+k*skm0/z; ddL3 = ddL3+k*(k-1)*skm0/(z*z);
	      		skm2 = skm1; skm1 = skm0;
	      		dsm2 = dsm1; dsm1 = dL3;
	      		k++;
		}
	    	result.numb = k-1;
	   	result.val = L1 + L2 + std::log(z) * L3;
	    	result.dval = dL1 + dL2 + std::log(z) * dL3 + L3/z;
	    	ddval = ddL1 + ddL2 - L3/(z*z) + 2*dL3/z + log(z) * ddL3;

	    	if (std::isinf(result.val) ||std::isinf(result.dval) ||std::isnan(result.val) ||std::isnan(result.dval) ) {
                        throw std::runtime_error("HeunC00log: failed convergence of recurrence and summation"); 
                }
	    	else {
			std::complex<double> val2, val3;
	      		std::double err1, err2;
			if (p.q-p.alpha*z !=0) {	    
	       			val2 = ( z*(z-1)*ddval+(p.gamma*(z-1)+p.delta*z+p.epsilon*z*(z-1))*dval ) / (p.q-p.alpha*z);
	        		val3 = ((dL3*p.epsilon+ddL3)*(z*z)*log(z)+(dL3*(p.gamma-p.epsilon+p.delta)-ddL3)*z*log(z)-dL3*p.gamma*log(z)+
	          			(p.epsilon*(dL2+dL1)+ddL2+ddL1)*(z*z)+((dL1+dL2)*(p.gamma-p.epsilon+p.delta)+L3*p.epsilon-ddL2-ddL1+2*dL3)*z+
	          			L3*(1-p.gamma)/z-(dL1+dL2)*p.gamma+L3*(p.gamma+p.delta-p.epsilon)-2*dL3-L3) / (p.q-p.alpha*z);
	      
	        		err1 = min(std::abs(result.val-val2),std::abs(result.val-val3));
			}
	      		else {
	        		err1 = INFINITY;
	      		}
	      		if (std::abs(p.q-p.alpha*z)<0.01)||(err1<eps) {
	        		err2 = abs(L1)*eps*N + abs(ckm0)*sp.qrt(result.numb-N+1) + abs(L2)*eps*(result.numb-N+1) +
	               			abs(log(z)) * ( abs(skm0)*sp.qrt(result.numb-N+1) + abs(L3)*eps*(result.numb-N+1) );
	        		result.err =  min(err1,err2);
	      		}
			else {
	        		result.err = err1;
	      		}
		}
	}
	return result;
}

#endif /* HEUNC0_IMPL_HPP_ */
