#include <iostream>
#include <vector>
#include <random>
#include <cmath>

int choose(std::vector<int> group, const int N) {
    int len = group.size(); // Get the length of the group vector
    std::vector<double> normalized_group; 
    normalized_group.reserve(len); // Reserve space for the normalized group vector

    for(int ii=0; ii < len; ++ii){
        normalized_group[ii] = group[ii]/N;
    } // Normalize the group values by dividing each by N (the total force units)

    unsigned int seed = 42;
    std::mt19937 gen(seed);
    std::uniform_real_distribution<double> distribution(0 , 1);
    double coin = distribution(gen); // Generate a random number between 0 and 1

    // Choose all the indices of the group vector that have a normalized value greater than the random number
    std::vector<int> chosen_indices;
    for(int ii=0; ii < len; ++ii){
        if(normalized_group[ii] > coin){
            chosen_indices.push_back(ii);
        }
    }
    // Then choose one of the indices from the chosen_indices vector at random
    std::uniform_int_distribution<int> index_distribution(0, chosen_indices.size() - 1);
    int random_index = index_distribution(gen);

    return chosen_indices[random_index];
}

// INtroduced the decide function as a bool
bool decide(double v) {
    // Generador de números aleatorios estático para mantener el estado entre llamadas 
    static std::random_device rd; //Se crea la semilla y el generador estaticos para que solo se creen una vez en memoria
    static std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(0.0, 1.0); //GEneración de numeros aleatorios ente 0.0 y 1.0

    // Retorna true si el número aleatorio es menor que la probabilidad v
    return dist(gen) < v;
}





//Introduced the fragment function, as a void?
void fragment(std::vector<int> group, int index) {
    if (group[index] > 1) {
        int s_i = group[index];
        group[index] = 1;
        for (int k = 0; k < s_i - 1; ++k) {
            group.push_back(1);
        }
    }
}
//Introduced the combine function, as a void?
void combine(std::vector<int>, int index_i, int index_j) {
    group[index_i] += group[index_j];
    group[index_j] = group.back();
    group.pop_back();
}

//INtroduce the countS function as a int

int countS(const std::vector<int>& guerrilla, int s_buscado) { //Recibe el vector guerrilla por referencia cte para no duplicarlo en memoria y el S buscado
    int contador = 0; // Cuenta cuantas veces esta el S buscado
    for (int s_i : guerrilla) { 
        if (s_i == s_buscado) {
            contador++;
        }
    }
    return contador; //REtorna el total acumulador un entero
}

int main(int argc, char** argv) {
    int N = 100;
    double v = 0.001;
    int T = N //Change T, choose according to what?
    // Generate the guerrilla vector of size N and values 1
    std::vector<int> guerrilla(N, 1);

    int chosen_index = choose(guerrilla, N);
    std::cout << "Chosen index: " << chosen_index << std::endl;
//Time bucle with the first condition
    for (int t = 0; t < T, ++t) {
        if (guerrilla.size() <= 1) break;
//Choose function calling
        int index_i = choose(guerrila, N);
        //Flip the coin, but how? :(

    return 0;
}
