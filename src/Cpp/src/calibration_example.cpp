/*
    Macro for a calibration example
*/

#include <Riostream.h>

#include "../utils/fileManager.hpp"

#include <TFile.h>
#include <TGraphErrors.h>



void calibration(const char * outputFilePath, const int nPoints, const double * x, const double * y, const double * ex, const double * ey)
{
    TGraphErrors graph(nPoints, x, y, ex, ey);
    graph.Fit("pol1");

    TFile file(outputFilePath, "recreate");
    graph.Write();
    file.Close(); 
}

void doCalibration()
{
    FileManager f("data/input/calibration_test.txt");
    const char * outputFilePath = "data/output/calibration_test.root";

    calibration(outputFilePath, f.getNRows(), f["x"], f["y"], f["ex"], f["ey"]);
}