#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <unordered_map>
#include <stdexcept>
#include <fstream>
#include <string>
#include <format>

// Introduce the loading function as a void
void loading(const int T, int & t) {
    double interval = T/10; // Progress in 10% blocks (could be changed)
    static int pre_k = -1; // Save the last printed progress
    int k = static_cast<int>(std::round(t / interval)); 

    if (k > pre_k) { // Only prints if there is a change
        pre_k = k;  

        std::cout << "\r\t\t\t  [";  
        for (int i = 0; i < k; i++) std::cout << "XX"; 
        for (int i = k; i < 10; i++) std::cout << "--"; 
        std::cout << "] " << k * 10 << "%" << std::flush; 
    }
}


// Introduced the random_number function as double
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
    unsigned int seed = 42;
    // static std::random_device rd; // Create on time in memory
    std::mt19937 gen(seed);
    // Validation if chosen_indices is empty
    if (chosen_indices.empty()) {
        std::uniform_int_distribution<int> fallback_distribution(0, len - 1);
        return fallback_distribution(gen);
    }
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
void fragment(std::vector<double>& group, int& index) {
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
void combine(std::vector<double>& group, int index_i, int index_j) {
    // Sum the force units of the attack unit i and j
    group[index_i] += group[index_j];
    // Moves the last force unit value to the index j
    group[index_j] = group.back();
    // Eliminates the last attack unit 
    group.pop_back(); // Modified group
}


// Introduced the count_s function as a map 
std::unordered_map<int, int> count_s(const std::vector<double>& group) {
    // Initialices the map: S_k --- Number of units with S_k
    std::unordered_map<int, int> frequencies;
    // Loop of the S_k 
    for (double num : group) {
        frequencies[static_cast<int>(num)]++; // magic
    }
    return frequencies;
}


// Introduced the count_alpha function as a double
double count_alpha(const std::unordered_map<int, int>& data) {
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
        double NUMERATOR = (valid_points * sum_XY) - (sum_X * sum_Y);
        double denominator = (valid_points * sum_X2) - (sum_X * sum_X);
        if (denominator == 0.0){return 0.0;}
        
        double slope = NUMERATOR/denominator;
        
        return slope + 1.0;
    }
}


// Introduce the print_to_txt function as void
void print_to_text(int tt,const std::unordered_map<int,int>& data, const std::string& filename) {
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
    //std::cout << "Data saved successfully at: " << filename << std::endl;
}


int main(int argc, char** argv) {

    std::cout << "Starting the simulation..." << std::endl;
    // Default values
    int N = 1110; // Total force units
    double v = 0.001; // Fragmentation probability
    int T = 110; //Change T, choose according to the process

    // Command Line Arguments
    if (argc > 2){
        try{
        N = std::stoi(argv[1]);
        } catch (const std::exception& e) {
            std::cerr << "Error: Invalid 'Total force units' (N). Using default value.\n";
        }
        try{
        v = std::stod(argv[2]);
        } catch (const std::exception& e) {
            std::cerr << "Error: Invalid 'Fragmentation probability' (v). Using default value.\n";
        }
    }

    // Generate the guerrilla vector of size N and values 1
    int tt = 0;
    std::vector<double> guerrilla(N, 1);
    print_to_text(tt, count_s(guerrilla),"../results/" +  std::to_string(tt) + "_data.txt");

    // --- Starts the algorith ---
    // Initial iteration: Since at the begining every unit is "fine", we must combine in the first 
    tt = 1;
    int chosen_index_i = choose(guerrilla, N); // Choose U_i (index of the vector)
    int chosen_index_j = choose(guerrilla, N); // Choose U_j (index of the vector)
    combine(guerrilla, chosen_index_i, chosen_index_j); // Combines the first two units
    print_to_text(tt, count_s(guerrilla),"../results/" +   std::to_string(tt) + "_data.txt");


    // Time iteration over the period of time T:
    for (int tt = 2; tt < T; ++tt) {
        // Choose U_i
        int chosen_index_i = choose(guerrilla, N);

        // Check if U_i is "fine", i.e., S_i = 1
        if (guerrilla[chosen_index_i] == 1){
            // The only option is to combine:
            int chose_index_j = choose(guerrilla, N);
            combine(guerrilla, chosen_index_i, chosen_index_j);
            
            loading(T, tt);
            print_to_text(tt, count_s(guerrilla),"../results/" + std::to_string(tt) + "_data.txt");
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
            
            loading(T, tt);
            print_to_text(tt, count_s(guerrilla),"../results/" + std::to_string(tt) + "_data.txt");
        }
    }
    std::cout << "\nSimulation completed successfully, the results are saved in the 'results' folder." << std::endl;
    return 0;
}
