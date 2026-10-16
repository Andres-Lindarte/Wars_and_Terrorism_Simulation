#include <iostream>
#include <vector>
#include <random>
#include <cmath>

int choose(std::vector<int> group, const int N) {
    int len = group.size();
    std::vector<double> normalized_group; 
    normalized_group.reserve(len);

    for(int ii=0; ii < len; ++ii){
        normalized_group[ii] = group[ii]/N;
    }

    unsigned int seed = 42;
    std::mt19937 gen(seed);
    std::uniform_real_distribution<double> distribution(0 , 1);
    double coin = distribution(gen);

}
