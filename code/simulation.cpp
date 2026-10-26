// Compilation:     g++ -std=c++20 simulation.cpp -o simulation.x -fsanitize=undefined -O3
// Excecution (Command Line Arguments):  ./simulation.x N v T
//      N : (Optional, default = 1110) Total force units
//      v : (Optional, default = 0.01) Fragmentation probability
//      T : (Optional, default = 110) Total iterations

#include <iostream>
#include <vector>
#include <random>
#include <map>
#include <stdexcept>
#include <fstream>
#include <string>
#include <chrono>

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


// Introduced the choose function as a int
int choose(const std::vector<double>& group, std::mt19937& generator) {
    // Use the discrete distribution function from c++
    std::discrete_distribution<std::size_t> discrete_dist(group.begin(), group.end());
    return discrete_dist(generator);
}


// Introduced the decide function as a bool
bool decide(const double& v, std::mt19937& generator) {
    // True if the number is less than the probability v
        // True ---> Fragmentates
        // False ---> Combines
    std::uniform_real_distribution<double> distribution(0.0 , 1.0);
    return distribution(generator) < v;
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
std::map<int, int> count_s(const std::vector<double>& group) {
    // Initialices the map: S_k --- Number of units with S_k
    std::map<int, int> frequencies;
    // Loop of the S_k 
    for (double num : group) {
        frequencies[static_cast<int>(num)]++; // magic
    }
    return frequencies;
}


// Introduced the count_alpha function as a double
double count_alpha(const std::map<int, int>& data) {
    if (data.size() < 2){return 0.0;} // Insufficient number of points to calculate the line
    //HERE:else {
    double accumulated = 0.0;

    // Variables for the linear regression
    double sum_X = 0.0;
    double sum_Y = 0.0;
    double sum_XY = 0.0;
    double sum_X2 = 0.0;
    int valid_points = 0;

    // Loop through the map in reverse order to calculate the accumulated probability
    for (auto it = data.rbegin(); it != data.rend(); ++it) {
        double S = it->first;
        double probability = it->second;

        // Sum to calculate P(X >= x)
        accumulated += probability;

        if (S > 1.0 && accumulated > 0.0) {
            double ln_S = std::log(S);               // X
            double ln_prob = std::log(accumulated);  // Y

            sum_X += ln_S;
            sum_Y += ln_prob;
            sum_XY += (ln_S * ln_prob);
            sum_X2 += (ln_S * ln_S);
            valid_points++;
        }
    }
    if (valid_points < 2){return 0.0;} // insufficient valid point to calculate the logs 

    // Mean Squares (linear regression)
    double numerator = (valid_points * sum_XY) - (sum_X * sum_Y);
    double denominator = (valid_points * sum_X2) - (sum_X * sum_X);
    if (denominator == 0.0){return 0.0;}
    
    double slope = numerator/denominator;
    
    //HERE:return slope + 1.0;
    return 1.0 - slope;
    //HERE:}
}


// Introduce the print_to_txt function as void
void print_to_text(int tt,const std::map<int,int>& data, const std::string& filename) {
    //Open (or create) the file 
    std::ofstream file(filename, std::ios::app);
    
    //Verify if the file opened correctly
    if (!file.is_open()) {
        std::cerr << "Error when opening the file " << filename << std::endl;
        return;
    }
    
    // Print the time and alpha value
    file << tt << "\t" << count_alpha(data) << "\t";

    //Conver the map and write each pair (Strength S , Unit Amount U)
    for (const auto&pair : data) {
        file << "(" << pair.first << ", " << pair.second << ")";
    }
    file << "\n";
    
    //Close the file
    file.close();
    //std::cout << "Data saved successfully at: " << filename << std::endl;
}


int main(int argc, char** argv) {
    // Start the timer!!!
    auto start = std::chrono::high_resolution_clock::now();

    std::cout << "\t--- WARS AND TERRORISM SIMULATION ---\nStarting the simulation...\n";
    
    // Default values
    int N = 1110; // Total force units // HERE: increase at least a mangitude order
    double v = 0.01; // Fragmentation probability
    int T = 110; // Total iterations - Change T, choose according to the process // HERE: increase T = 100000

    // Command Line Arguments
    if (argc == 4){
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
        try{
        T = std::stoi(argv[3]);
        } catch (const std::exception& e) {
            std::cerr << "Error: Invalid 'Total iterations' (T). Using default value.\n";
        }
    }

    // Prints the parameters on the terminal to check their values
    std::cout << "N = " << N << "\tv = " << v << "\tT = " << T << "\n\n";

    // Inicialites the seed and random number generator 
    unsigned int seed = 42;
    //static std::random_device rd;
    std::mt19937 gen(seed);

    // Generate the guerrilla vector of size N and values 1
    int tt = 0;
    std::vector<double> guerrilla(N, 1);
    std::string filename = "../results/master_data.txt";

    // Erase the data of the previous excecusion on the master 
    std::ofstream(filename, std::ios::trunc).close(); 
    print_to_text(tt, count_s(guerrilla), filename);

    // --- Starts the algorith ---
    // Initial iteration: Since at the begining every unit is "fine", we must combine in the first 
    tt = 1;
    int chosen_index_i = choose(guerrilla, gen); // Choose U_i (index of the vector)
    int chosen_index_j = choose(guerrilla, gen); // Choose U_j (index of the vector)
    // Choose another U_j if U_i = U_j
    while (chosen_index_i == chosen_index_j){
        chosen_index_j = choose(guerrilla, gen);
    }; 
    combine(guerrilla, chosen_index_i, chosen_index_j); // Combines the first two units
    print_to_text(tt, count_s(guerrilla), filename);
    
    // Time iteration over the period of time T:
    for (int tt = 2; tt <= T; ++tt) {
        // Choose U_i
        int chosen_index_i = choose(guerrilla, gen);

        // Check if U_i is "fine", i.e., S_i = 1
        if (guerrilla[chosen_index_i] == 1){
            // The only option is to combine:
            int chosen_index_j = choose(guerrilla, gen);
            while (chosen_index_i == chosen_index_j){
                chosen_index_j = choose(guerrilla, gen);
            }; 
            combine(guerrilla, chosen_index_i, chosen_index_j);
            
            // Loading bar and print
            loading(T, tt);
            if (T >= 1000000){ // If the total iterations are larger than 1 millon:
                if (tt % 1000 == 0){ // Print only 1000 by 1000
                    print_to_text(tt, count_s(guerrilla), filename);
                }
            }
            else {print_to_text(tt, count_s(guerrilla), filename);}
        }

        else {
            // Dinamic process: Fragmentation of combination
            if (decide(v, gen)){
                fragment(guerrilla, chosen_index_i);
            }
            else {
                int chosen_index_j = choose(guerrilla, gen);
                while (chosen_index_i == chosen_index_j){
                chosen_index_j = choose(guerrilla, gen);
                }; 
                combine(guerrilla, chosen_index_i, chosen_index_j);
            }
            
            loading(T, tt);
            if (tt % 1000 == 0){
                print_to_text(tt, count_s(guerrilla), filename);
            }
        }
    } 
    // Stop the timer!!!
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> simulation_time = end - start;

    std::cout << "\n\nSimulation completed successfully in " << simulation_time.count() << " s. \nThe results are saved in the 'results' folder." << "\n";
    
    return 0;
}