import subprocess
import sys
import itertools
import concurrent.futures
import os

# Names
cpp_file = "simulation.cpp"
executable = "./simulation.x"
plot_script = "plotting.py"
data_file = "master_data.txt"

# Different values for the simulation
v_values = ["0.01", "0.069", "0.1"]
T_values = ["1000000", "2500000", "5000000"]
seed_values = ["42", "69", "911"]

def compile():
    print(f"Compilating {cpp_file}...")
    try:
        subprocess.run(["g++", "-std=c++20", cpp_file, "-o", "simulation.x", "-O3"], check=True)
        print("Successfully compiled.\n")
    except subprocess.CalledProcessError:
        print("Error during the compilation of the C++ program.")
        sys.exit(1)

# Nueva función auxiliar para correr una sola simulación
def run_single_simulation(params):
    v, T, s = params
    try:
        # capture_output=True evita que las barras de carga de C++ colapsen la terminal
        subprocess.run([executable, "10000", v, T, s], check=True, capture_output=True, text=True)
        print(f"Completado: v={v}, T={T}, seed={s}")
    except subprocess.CalledProcessError:
        print(f"Error at executing the simulation with v={v}, T={T}, seed={s}.")
        raise  # Lanza el error para que el ejecutor principal lo detecte

def execute_simulations():
    print("\t### SIMULATION PROTOCOLE STARTED: ###")
    
    # Crea una lista con todas las combinaciones posibles de parámetros (27 simulaciones en total)
    combinations = list(itertools.product(v_values, T_values, seed_values))
    
    # Obtiene el número de núcleos de tu procesador para lanzar esa cantidad de procesos a la vez
    nucleos = os.cpu_count()
    print(f"Ejecutando {len(combinations)} simulaciones en paralelo usando {nucleos} núcleos...")
    
    # Ejecuta el pool de hilos
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=nucleos) as executor:
            # executor.map asigna cada combinación a un hilo disponible
            list(executor.map(run_single_simulation, combinations))
    except Exception:
        print("Una o más simulaciones fallaron. Deteniendo ejecución.")
        sys.exit(1)
        
    print("\t### SIMULATION PROTOCOLE FINISHED SUCCESSFULLY ###")

def plot():
    print(f"Excecution {plot_script}...")
    try:
        # Change to python3 if needed
        subprocess.run(["python3", plot_script], check=True)
        print("The charts were generated succesfully!.")
    except subprocess.CalledProcessError:
        print("Error during the excecution of the graphing program")
        sys.exit(1)

if __name__ == "__main__":
    compile()
    execute_simulations()
    plot()