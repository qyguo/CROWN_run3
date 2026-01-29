#include "../include/MuonScaRe.hxx"
#include "../include/Crystal.hxx"
#include "TRandom3.h"
#include <cmath>
#include <iostream>

MuonScaRe::MuonScaRe(const std::string &json_file) {
    cset = correction::CorrectionSet::from_file(json_file);
}

double MuonScaRe::get_rndm(double eta, float nL) const {
    auto corr = cset->at("cb_params");
    double mean = corr->evaluate({std::fabs(eta), nL, 0});
    double sigma = corr->evaluate({std::fabs(eta), nL, 1});
    double n = corr->evaluate({std::fabs(eta), nL, 2});
    double alpha = corr->evaluate({std::fabs(eta), nL, 3});
    Crystal cb(mean, sigma, alpha, n);
    TRandom3 rnd(0);
    return cb.invcdf(rnd.Rndm());
}

double MuonScaRe::get_std(double pt, double eta, float nL) const {
    auto corr = cset->at("poly_params");
    double p0 = corr->evaluate({std::fabs(eta), nL, 0});
    double p1 = corr->evaluate({std::fabs(eta), nL, 1});
    double p2 = corr->evaluate({std::fabs(eta), nL, 2});
    return std::max(0.0, p0 + p1*pt + p2*pt*pt);
}

double MuonScaRe::get_k(double eta, const std::string &var) const {
    double k_data = cset->at("k_data")->evaluate({std::fabs(eta), var});
    double k_mc   = cset->at("k_mc")->evaluate({std::fabs(eta), var});
    return (k_mc < k_data) ? std::sqrt(k_data*k_data - k_mc*k_mc) : 0.0;
}

double MuonScaRe::pt_scale(bool is_data, double pt, double eta, double phi, int charge) const {
    std::string dtmc = is_data ? "data" : "mc";
    double a = cset->at("a_" + dtmc)->evaluate({eta, phi, "nom"});
    double m = cset->at("m_" + dtmc)->evaluate({eta, phi, "nom"});
    return 1.0 / (m / pt + charge * a);
}

double MuonScaRe::pt_scale_var(double pt, double eta, double phi, int charge, const std::string &updn) const {
    double stat_a = cset->at("a_mc")->evaluate({eta, phi, "stat"});
    double stat_m = cset->at("m_mc")->evaluate({eta, phi, "stat"});
    double stat_rho = cset->at("m_mc")->evaluate({eta, phi, "rho_stat"});
    double unc = pt * pt * std::sqrt(
        stat_m*stat_m / (pt*pt) +
        stat_a*stat_a +
        2 * charge * stat_rho * stat_m / pt * stat_a
    );
    return (updn == "up") ? pt + unc : pt - unc;
}

double MuonScaRe::pt_resol(double pt, double eta, float nL) const {
    double rndm = get_rndm(eta, nL);
    double std = get_std(pt, eta, nL);
    double k = get_k(eta, "nom");
    double ptc = pt * (1 + k * std * rndm);
    return std::isnan(ptc) ? pt : ptc;
}

double MuonScaRe::pt_resol_var(double pt_woresol, double pt_wresol, double eta, const std::string &updn) const {
    double k = get_k(eta, "nom");
    if (k == 0) return pt_wresol;
    double k_unc = cset->at("k_mc")->evaluate({std::fabs(eta), "stat"});
    double std_x_rndm = (pt_wresol / pt_woresol - 1) / k;
    if (updn == "up") return pt_woresol * (1 + (k + k_unc) * std_x_rndm);
    if (updn == "dn") return pt_woresol * (1 + (k - k_unc) * std_x_rndm);
    std::cerr << "ERROR: updn must be 'up' or 'dn'" << std::endl;
    return pt_wresol;
}

