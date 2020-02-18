// for confluent Heun function, a solution of the equation
// HeunC''(z)+(gamma/z+delta/(z-1)+epsilon)*HeunC'(z)+(alpha*z-q)/(z*(z-1))*HeunC(z) = 0
//
// HeunCjoin0infA finds connection coefficients C0, Cs, such that
// C0 * HeunC00(z) + Cs * HeunCs00(z) analytically continues to
// the first, power solution at infinity \exp(i\theta) \infty
// (see HeunCinfA)
//
// Usage:
// [C0,Cs,err,numb,wrnmsg] = HeunCjoin0infA(q,alpha,gamma,delta,epsilon,theta)
//
// Returned parameters:
// C0, Cs are the connection coefficients
// err is the estimated error
// numb is the number of power series terms needed for the evaluation
// wrnmsg is a warning message:
//   it is empty if computations are ok
//   otherwise it is a diagnostic message and the function returns C0, Cs = NaN
//
// Oleg V. Motygin, copyright 2018, license: GNU GPL v3
//
// 15 February 2018
//

struct ConnectionVars
{
Matrix<std::complex<double>> C10;
double err;
int numb;
}

// use elements [0][0] and [1][0] to be C0 and Cs

ConnectionVars HeunCjoin0infA(HeunCparams p,bool aux)
{
  ConnectionVars result;
  bool consts_known = false;

  result = extrdatfromsav(p, savdata0infA, consts_known);

  if consts_known {
    result.numb = 0;
  }
  else {

    HeunCvars result, varsinf, varsJinf, varsJ0, varsJs;

    std::pair<double, int> RN = findR(saveR, saveN);
    double R = RN.first();
    int N = RN.second();

    R0 = R/(abs(eps)+abs(epsilon));

    infpt = -2 * R0;
    joinpt = -min(1,R0);

    varsinf = HeunCinfA(p,infpt);	// value at "infinity" point
    varsJinf = HeunCconnect(p,joinpt,infpt,result.val,result.dval); //

    varsJ0 = HeunC0(p,joinpt,aux); // first solution at join point near zero 
    varsJs = HeunCs0(p,joinpt);	        // second solution at join point near zero

    result.err = varsinf.err + varsJinf.err + varsJ0.err + varsJs.err;
    result.numb = varsinf.numb + varsJinf.numbJ + varsJ0.numb + varsJs.numb;

    Matrix<std::complex<double>> m, b;
    m.Init(varsJ0.val,varsJs.val, varsJ0.dval,varsJs.dval);
    b.Init(varsJinf.val, 0, varsJinf.dval, 0);
    result.C10 = (m.inverse().dot(b));

    savedataVars s;
    s.p = p;
    s.Cvars = result;
    keepdattosav(s, savdata10);
  }

}

