#include "../include/Crystal.hxx"

Crystal::Crystal(double mean, double sigma, double alpha, double n)
    : m(mean), s(sigma), a(alpha), n(n), pi(3.14159), sqrtPiOver2(std::sqrt(pi/2.0)), sqrt2(std::sqrt(2.0)) {
    init();
}

void Crystal::init() {
    double fa = std::fabs(a);
    double ex = std::exp(-fa*fa/2);
    double A = std::pow(n/fa, n) * ex;
    double C1 = n/fa/(n-1) * ex;
    double D1 = 2 * sqrtPiOver2 * erf(fa/sqrt2);
    B = n/fa - fa;
    C = (D1 + 2*C1)/C1;
    D = (D1 + 2*C1)/2;
    N = 1.0 / s / (D1 + 2*C1);
    k = 1.0 / (n-1);
    NA = N * A;
    Ns = N * s;
    NC = Ns * C1;
    F = 1 - fa*fa/n;
    G = s*n/fa;
    cdfMa = cdf(m - a*s);
    cdfPa = cdf(m + a*s);
}

double Crystal::pdf(double x) const {
    double d = (x - m)/s;
    if (d < -a) return NA * std::pow(B - d, -n);
    if (d > a)  return NA * std::pow(B + d, -n);
    return N * std::exp(-d*d/2);
}

double Crystal::pdf(double x, double ks, double dm) const {
    double d = (x - m - dm)/(s * ks);
    if (d < -a) return NA / ks * std::pow(B - d, -n);
    if (d > a)  return NA / ks * std::pow(B + d, -n);
    return N / ks * std::exp(-d*d/2);
}

double Crystal::cdf(double x) const {
    double d = (x - m)/s;
    if (d < -a) return NC / std::pow(F - s*d/G, n-1);
    if (d > a)  return NC * (C - std::pow(F + s*d/G, 1 - n));
    return Ns * (D - sqrtPiOver2 * erf(-d/sqrt2));
}

double Crystal::invcdf(double u) const {
    if (u < cdfMa) return m + G * (F - std::pow(NC/u, k));
    if (u > cdfPa) return m - G * (F - std::pow(C - u/NC, -k));
    return m - sqrt2 * s * boost::math::erf_inv((D - u/Ns) / sqrtPiOver2);
}

