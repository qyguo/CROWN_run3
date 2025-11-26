#ifndef MUONSCARE_H
#define MUONSCARE_H

#include <string>
#include <memory>
#include "correction.h"
#include "Crystal.hxx"

class MuonScaRe {
public:
    MuonScaRe(const std::string &json_file);
    double pt_scale(bool is_data, double pt, double eta, double phi, int charge) const;
    double pt_scale_var(double pt, double eta, double phi, int charge, const std::string &updn) const;
    double pt_resol(double pt, double eta, float nTrackerLayers) const;
    double pt_resol_var(double pt_woresol, double pt_wresol, double eta, const std::string &updn) const;

private:
    std::shared_ptr<correction::CorrectionSet> cset;
    double get_rndm(double eta, float nL) const;
    double get_std(double pt, double eta, float nL) const;
    double get_k(double eta, const std::string &var) const;
};

#endif

