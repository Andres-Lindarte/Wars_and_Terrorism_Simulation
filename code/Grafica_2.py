import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

# HELPER FUNCTIONS 🛠️

def extract_parameters(file_name):
    """
    Extracts nu, T, and seed from the file name: master_data_nu_T_seed.txt
    """
    parts = file_name.name.split('_')
    nu = parts[2]
    T = parts[3]
    s = parts[4].replace('.txt', '')
    return nu, T, s


def load_master_data(file_list):
    """
    Reads each .txt file and extracts (t_values, a_values, last_line_tuples).
    Returns the complete master_data list.
    """
    data = []
    for file in file_list:
        t_values = []
        a_values = []
        last_line_tuples = ""
        
        with open(file, 'r') as f:
            for line in f:
                parts = line.split(maxsplit=2) 
                if len(parts) >= 2:
                    t_values.append(float(parts[0]))
                    a_values.append(float(parts[1]))
                    
                if len(parts) == 3:
                    last_line_tuples = parts[2] 
        
        data.append((t_values, a_values, last_line_tuples))
    
    return data

def linear_regression(x: list, y: list):
    X = np.array(x).reshape(-1, 1)
    Y = np.array(y) 

    model = LinearRegression()
    model.fit(X, Y)

    slope = model.coef_[0]
    intercept = model.intercept_
    r_pearson, _ = stats.pearsonr(x, y)
    r_squared = r_pearson**2
    return slope, intercept, r_squared



# 1. GLOBAL PARAMETERS AND FILES
files = list(Path("../data").glob("master_data_*.txt"))

nu_values = ["0.01", "0.069", "0.1"]
T_values = ["10000", "25000", "50000"]
seeds = ["42", "69", "911"]

seed_per_T = {
    T_values[0]: seeds[0],
    T_values[1]: seeds[1],
    T_values[2]: seeds[2]
}

max_T = T_values[-1]
fixed_seed = "42"

# 2. READ AND STORE DATA

master_data = load_master_data(files)


# 3. STATISTICAL CALCULATION FOR ALPHA (MEAN & STD) 📊

sample_size = 10  # Number of points at the end of the simulation per seed
alpha_stats = {}  # Dictionary to store (mu, sigma) for each nu

print("\n" + "="*50)
print("  ALPHA EXPONENT STATISTICS (µ ± σ)")
print("="*50)

for nu in nu_values:
    for T in T_values:
        combined_alphas = []
        
        for i, file in enumerate(files):
            file_nu, file_T, file_s = extract_parameters(file)
            
            if file_nu == nu and file_T == T:
                a_values = master_data[i][1]
                last_alphas = a_values[-sample_size:]
                combined_alphas.extend(last_alphas)
        
        if combined_alphas:
            mu = np.mean(combined_alphas)
            sigma = np.std(combined_alphas, ddof=1)
            print(f"Parameters: ν = {nu:<5} | T = {T:<5} ---> Alpha = {mu:.4f} ± {sigma:.4f}  (N={len(combined_alphas)})")
            
            # Store statistics for max_T (used in plot titles)
            if T == max_T:
                alpha_stats[nu] = (mu, sigma)

print("="*50 + "\n")

# 4. FIGURE 1: ALPHA EVOLUTION 📈

fig_alpha, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
alpha_axes = [ax1, ax2, ax3]

for i, file in enumerate(files):
    nu, T, s = extract_parameters(file)

    if T == max_T and s == fixed_seed:
        index = nu_values.index(nu)
        
        alpha_axes[index].plot(master_data[i][0][3::2], master_data[i][1][3::2], "-*", color='blue')
        alpha_axes[index].set_xlabel('Time (t)')
        alpha_axes[index].set_ylabel(r'Exponent $\alpha$')
        alpha_axes[index].tick_params(top=True, right=True, direction='in')
        
        # Subplot title including nu and alpha statistics
        mu, sigma = alpha_stats.get(nu, (0.0, 0.0))
        alpha_axes[index].set_title(f"\\nu = {nu} (T = {T})\n$\\alpha = {mu:.4f} \\pm {sigma:.4f}$")

fig_alpha.suptitle("Time Evolution of Exponent \\alpha (Max T)", fontsize=14)
fig_alpha.tight_layout()

# 5. FIGURE 2: SIZE DISTRIBUTION (LOG-LOG) 📊

fig_log, (ax11, ax22, ax33) = plt.subplots(1, 3, figsize=(15, 5))
log_axes = [ax11, ax22, ax33]

colors = {
    T_values[0]: "tab:blue",
    T_values[1]: "tab:green",
    T_values[2]: "tab:red",
}

for i, file in enumerate(files):
    nu, T, s = extract_parameters(file)

    if s == seed_per_T[T]:
        index = nu_values.index(nu)

        tuple_text = master_data[i][2]
        pair_list = tuple_text.strip(" ()\n").split(")(")
        s_list = []
        n_list = []

        for pair in pair_list:
            if ',' in pair:
                numbers = pair.split(',')
                s_list.append(float(numbers[0]))
                n_list.append(float(numbers[1]))
                
        reversed_s = s_list[::-1]
        reversed_n = n_list[::-1]

        cumulative_sum = 0
        cumulative_list = []
        for n in reversed_n:
            cumulative_sum += n
            cumulative_list.append(cumulative_sum)

        x_axis = np.log(reversed_s)
        y_axis = np.log(cumulative_list)
                
        log_axes[index].plot(x_axis, y_axis, marker='o', linestyle='none', color=colors[T], label=f"T = {T}", alpha=0.5)

        slope, intercept, _ = linear_regression(x_axis, y_axis)
        x_full = np.linspace(min(x_axis) - 0.01*max(x_axis), max(x_axis) + 0.01*max(x_axis), 100)
        log_axes[index].plot(x_full, slope*x_full + intercept, color=colors[T])

        log_axes[index].set_xlabel('Ln(S)')
        log_axes[index].set_ylabel('Ln(Cumulative Frequency)')
        log_axes[index].tick_params(top=True, right=True, direction='in')

        # Subplot title including nu and alpha statistics
        mu, sigma = alpha_stats.get(nu, (0.0, 0.0))
        log_axes[index].set_title(f"\\nu = {nu}\n$\\alpha = {mu:.4f} \\pm {sigma:.4f}$")

for ax in log_axes:
    ax.legend()

fig_log.suptitle("Size Distribution (Log-Log)", fontsize=14)
fig_log.tight_layout()

# 6. SAVE AND DISPLAY RESULTS 📄
Path('../results').mkdir(parents=True, exist_ok=True)
fig_alpha.savefig('../results/ALPHA.pdf', dpi=300)
fig_log.savefig('../results/LOG_DISTRIBUTION.pdf', dpi=300)

plt.show()
