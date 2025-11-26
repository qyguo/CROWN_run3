#ifndef Crystal_H
#define Crystal_H

#include <cmath>
#include <boost/math/special_functions/erf.hpp>

class Crystal {
public:
    Crystal(double mean, double sigma, double alpha, double n);
    double pdf(double x) const;
    double pdf(double x, double ks, double dm) const;
    double cdf(double x) const;
    double invcdf(double u) const;

private:
    void init();
    double m, s, a, n;
    double pi, sqrtPiOver2, sqrt2;
    double B, C, D, N, NA, Ns, NC, F, G, k, cdfMa, cdfPa;
};

#endif

