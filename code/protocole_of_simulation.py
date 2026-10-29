import subprocess
import sys
import numpy as np

# Names
cpp_file = "simulation.cpp"
executable = "./simulation.x"
plot_script = "Grafica_2.py"
data_file = "master_data.txt"

# Different values for the simulation
v_values = ["0.01", "0.069", "0.1"]
T_values = ["10000", "25000", "50000"]
seed_values = ["42", "69", "911"]

def compile():
    print(f"Compilating {cpp_file}...")
    try:
        subprocess.run(["g++", "-std=c++20", cpp_file, "-o", "simulation.x", "-O3"], check=True)
        print("Successfully compiled.\n")
    except subprocess.CalledProcessError:
        print("Error during the compilation of the C++ program.")
        sys.exit(1)

def execute_simulations():
    print("\t### SIMULATION PROTOCOLE STARTED: ###")
    for v in v_values:
        for T in T_values:
            alphas_seeds = []
            for s in seed_values:
                try:
                    subprocess.run([executable, "10000", v, T, s], check=True)

                    with open(data_file, "r") as f:
                        lines = [line.strip() for line in f if line.strip()]

                        if lines:
                            last_line_columns = lines[-1].split()
                            alpha_val = float(last_line_columns[1])
                            alphas_seeds.append(alpha_val)
                        
                except subprocess.CalledProcessError:
                    print(f"Error at excecuting the simulation with v={v}, T={T}, seed={s}.")
                    sys.exit(1)
                except (IndexError, ValueError) as e:
                    print(f"Error leyendo el valor de alpha en {data_file}: {e}")
                    sys.exit(1)
            #Calulation of the mean and standard deviation
            mu = np.mean(alphas_seeds)
            sigma = np.std(alphas_seeds, ddof=1)
            print(f"Resultado para v={v}, T={T}: Alpha = {mu:.4f} ± {sigma:.4f}")
    
    print("\t### SIMULATION PROTOCOLE FINISHED SUCCESSFULLY ###")


def plot():
    print(f"Excecution {plot_script}...")
    try:
        # Change to python3 if needed
        subprocess.run(["python", plot_script], check=True)
        print("The charts were generated succesfully!.")
    except subprocess.CalledProcessError:
        print("Error during the excecution of the graphing program")
        sys.exit(1)

if __name__ == "__main__":
    compile()
    execute_simulations()
    plot()
