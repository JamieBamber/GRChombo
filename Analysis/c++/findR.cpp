% in HeunC*, HeunCs*, it is assumed that for |z|>2*R, asymptotic series 
% of type \sum_{n=0}^{\infty} b_n n!/z^n can be computed as superasymptotic
% with accuracy better than machine epsilon

void findR(double& R, int& N)
{
  if (R==0 || N==0) {
    double R_, R0;
    double logeps = std::log(eps);
    R_ = -logeps;
    int fact = 1;
    int n = 1;
  
    while (true)
    {
      n += 1;
      fact = fact * n;
      R0 = R_;
      R_ = (std::log(fact)-logeps)/n;
      if (R_ > R0)
        break;
      }
    }
  
    N = n-1;
    R = pow((fact/n/eps),(1.0/N));
  }
}
