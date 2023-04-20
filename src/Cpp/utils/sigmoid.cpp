#include <cmath>

/**
 * @brief Sigmoid function with the form y = y0 + a / (1 + e^(-(x - x0)/b))
 * 
 * @param x x = x[0]
 * @param par x0 = par[0]; y0 = par[1]; a = par[2]; b = par[3]
 * @return double 
 */
double sigmoid(double *x, double *par)
{
    return par[1] + par[2] / (1 + exp(- (x[0] - par[0]) / par[3]));
}