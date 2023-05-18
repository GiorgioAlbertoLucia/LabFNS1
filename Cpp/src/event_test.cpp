#include <Riostream.h>
#include <vector>

#include "Event.hpp"
#include "../utils/newDumper.hpp"
#include "Module.hpp"

void event_test()
{
    NewDumper dumpy("data/input/example_pedestal.dat");
    std::vector<unsigned> vectortype = {32, 32, 32, 16};
    std::vector<unsigned> nchan = {16, 16, 16, 8};

    Event b(1, "Cpp/configs/config_Events2.yml", dumpy);
}