import subprocess
import sys

# Names
cpp_file = "simulation.cpp"
executable = "./simulation.x" 
plot_script = "grafica.py"

# Different values for the simulation
v_values = ["0.01", "0.069", "0.10"]
T_values = ["10000", "25000", "50000"]
seed_values = ["42", "69", "911"]

def compile():
    print(f"Compilating {cpp_file}...")
    try:
        # Comando: g++ simulacion.cpp -o simulacion
        subprocess.run(["g++", "-std=c++20", cpp_file, "-o", "simulation.x", "-O3"], check=True)
        print("Successfully compiled.\n")
    except subprocess.CalledProcessError:
        print("Error during the compilation of the C++ program.")
        sys.exit(1)

def execute_simulations():
    print("\t### SIMULATION PROTOCOLE STARTED: ###")
    for v in v_values:
        for T in T_values:
            for s in seed_values:
                try:
                    subprocess.run([executable, "10000", v, T, s], check=True)
                except subprocess.CalledProcessError:
                    print(f"Error at excecuting the simulation with v={v}, T={T}, seed={s}.")
                    sys.exit(1)
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