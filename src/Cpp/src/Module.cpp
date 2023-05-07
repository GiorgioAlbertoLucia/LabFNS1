#include "Module.hpp"

Module::Module(unsigned nbytes, unsigned nchannels):
    fBits(nbytes), fChannels(nchannels)
{
    fDataUnsigned = {1,2,3}; 
    fDataDouble = {2.,6.};
}

Module::~Module()
{
}