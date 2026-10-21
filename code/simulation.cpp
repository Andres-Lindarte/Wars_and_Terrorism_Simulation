#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <unordered_map>
#include <stdexcept>
#include <fstream>
#include <format>

// Introduce the random_number function as double
double random_number() {
    unsigned int seed = 42;
    // static std::random_device rd; // Create on time in memory
    std::mt19937 gen(seed);
    // Generates a random number between 0 and 1
    std::uniform_real_distribution<double> distribution(0.0 , 1.0);
    return distribution(gen);
}


// Introduced the choose function as a int
int choose(std::vector<double>& group, const int& N) {
    int len = group.size(); // Get the length of the group vector
    std::vector<double> normalized_group; 
    normalized_group.reserve(len); // Reserve space for the normalized group vector

    for(int ii=0; ii < len; ++ii){
        normalized_group.push_back(static_cast<double>(group[ii])/N);
    } // Normalize the group values by dividing each by N (the total force units)

    double coin = random_number(); // Generates a random number between 0 and 1

    // Choose all the indices of the group vector that have a normalized value greater than the random number
    std::vector<int> chosen_indices;
    for(int ii=0; ii < len; ++ii){
        if(normalized_group[ii] > coin){
            chosen_indices.push_back(ii);
        }
    }
        // THIS PART COULD BE DELETED
    // Then choose one of the indices from the chosen_indices vector at random
    std::uniform_int_distribution<int> index_distribution(0, chosen_indices.size() - 1);
    int random_index = index_distribution(gen);

    return chosen_indices[random_index];
}


// Introduced the decide function as a bool
bool decide(const double& v) {
    // True if the number is less than the probability v
        // True ---> Fragmentates
        // False ---> Combines
    return random_number() < v;
}


// Introduced the fragment function, as a void, since it does something 
void fragment(std::vector<int>& group, int& index) {
    // Set the force unit S_i ---> number of "fine" attack units
    int s_i = group[index];
    // Change S_i to 1
    group[index] = 1;
    // Create new attack units of force 1
    for (int k = 0; k < s_i - 1; ++k) {
        // Modified group
        group.push_back(1);
    }
}


// Introduced the combine function, as a void
void combine(std::vector<int>& group, int index_i, int index_j) {
    // Sum the force units of the attack unit i and j
    group[index_i] += group[index_j];
    // Moves the last force unit value to the index j
    group[index_j] = group.back();
    // Eliminates the last attack unit 
    group.pop_back(); // Modified group
}


// Introduced the count_s function as a map 
std::unordered_map<int, int> count_s(const std::vector<int>& group) {
    // Initialices the map: S_k --- Number of units with S_k
    std::unordered_map<int, int> frequencies;
    // Loop of the S_k 
    for (int num : group) {
        frequencies[num]++; // magic
    }
    return frequencies;
}


// Introduced the count_alpha function as a double
double count_alpha(std::unordered_map<int, int>& data) {
    if (data.size() < 2){return 0.0;} // Insufficient number of points to calculate the line
    else {
        double accumulated = 0.0;

        // Variables for the linear regression
        double sum_X = 0.0;
        double sum_Y = 0.0;
        double sum_XY = 0.0;
        double sum_X2 = 0.0;
        int valid_points = 0;

        // Sweep of the map (ascending order)
        for (const auto& pair : data) {
            // The key 
            double S = pair.first;
            // The value
            double probability = pair.second;

            // Sum the probability to the accomulated one
            accumulated += probability;

            if (S > 0.0 && accumulated > 0.0) {
                // Calculates the logs
                double ln_S = std::log(S);               // X
                double ln_prob = std::log(accumulated);  // Y

                // Summatories for the linear regression
                sum_X += ln_S;
                sum_Y += ln_prob;
                sum_XY += (ln_S * ln_prob);
                sum_X2 += (ln_S * ln_S);
                valid_points++;
            }
        }
        if (valid_points < 2){return 0.0;} // insufficient valid point to calculate the logs 

        // Mean Squares (linear regression)
        double must combine in the first e denominator = (valid_points * sum_X2) - (sum_X * sum_X);
        if (denominator == 0.0){return 0.0;}
        
        double slope = numerator/denominator;
        
        return slope + 1.0;
    }
}

void print_to_text(int tt, const std::unordered_map<int,int>& data, const std::string& filename) {
    //Open (or create) the file 
    std::ofstream file(filename);
    
    //Verify if the file opened correctly
    if (!file.is_open()) {
        std::cerr << "Error when opening the file " << filename << std::endl;
        return;
    }

    // Print the time and alpha value
    file << "t = " << tt << "   " << "a = " << count_alpha(data) << "\n";

    //Conver the map and write each pair (Strength S , Unit Amount U)
    for (const auto&pair : data) {
        file << pair.first << "," << pair.second << "\n";
    }
    
    //Close the file
    file.close();
    std::cout << "Data saved successfully at: " << filename << std::endl;
}


int main(int argc, char** argv) {
    int N = 100; // Total force units
    double v = 0.001; // Fragmentation probability
    int T = 10; //Change T, choose according to the process

    // Generate the guerrilla vector of size N and values 1
    int tt = 0;
    std::vector<double> guerrilla(N, 1);
    print_to_text(count_s(guerrilla), std::format("{}_data.txt", tt));

    // --- Starts the algorith ---
    // Initial iteration: Since at the begining every unit is "fine", we must combine in the first 
    int tt = 1;
    int chosen_index_i = choose(guerrilla, N); // Choose U_i (index of the vector)
    int chosen_index_j = choose(guerrilla, N); // Choose U_j (index of the vector)
    combine(guerrilla, chosen_index_i, chosen_index_j); // Combines the first two units
    print_to_text(count_s(guerrilla), std::format("{}_data.txt", tt));


    // Time iteration over the period of time T:
    for (int tt = 2; tt < T; ++tt) {
        // Choose U_i
        int chosen_index_i = choose(guerrilla, N);

        // Check if U_i is "fine", i.e., S_i = 1
        if (guerrilla[chosen_index_i] == 1){
            // The only option is to combine:
            int chose_index_j = choose(guerrilla, N);
            combine(guerrilla, chosen_index_i, chosen_index_j);
            
            print_to_text(count_s(guerrilla), std::format("{}_data.txt", tt));
        }

        else {
            // Dinamic process: Fragmentation of combination
            if (decide(v)){
                fragment(guerrilla, chosen_index_i);
            }
            else {
                int chose_index_j = choose(guerrilla, N);
                combine(guerrilla, chosen_index_i, chosen_index_j);
            }

            print_to_text(count_s(guerrilla), std::format("{}_data.txt", tt));
        }
    }
    return 0;
}
