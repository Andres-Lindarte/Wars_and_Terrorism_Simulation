import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats


# ==========================================
# 0. FUNCIONES HELPER 🛠️
# ==========================================
def extraer_parametros(nombre_archivo):
    """
    Extrae nu, T y semilla del nombre del archivo: master_data_nu_T_semilla.txt
    """
    partes = nombre_archivo.split('_')
    nu = partes[2]
    T = partes[3]
    s = partes[4].replace('.txt', '')
    return nu, T, s


def cargar_datos_maestros(lista_archivos):
    """
    Lee cada archivo .txt y extrae (valores_t, valores_a, ultima_linea_tuplas)
    Retorna la lista datos_maestros completa.
    """
    datos = []
    for archivo in lista_archivos:
        valores_t = []
        valores_a = []
        ultima_linea_tuplas = ""
        
        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.split(maxsplit=2) 
                if len(partes) >= 2:
                    valores_t.append(float(partes[0]))
                    valores_a.append(float(partes[1]))
                    
                if len(partes) == 3:
                    ultima_linea_tuplas = partes[2] 
        
        datos.append((valores_t, valores_a, ultima_linea_tuplas))
    
    return datos

def linear_regression(x: list, y: list):
    X=np.array(x) # Convert the list to a numpy array
    Y=np.array(y) 
    X = X.reshape(-1, 1) # Reshape the data to fit the model

    model = LinearRegression() # Create a linear regression model
    model.fit(X, Y) # Fit the model to the data

    slope = model.coef_[0] # Get the slope of the line
    intercept = model.intercept_ # Get the intercept of the line
    r_pearson, _ = stats.pearsonr(x, y) # Calculate the Pearson correlation coefficient
    r_squared = r_pearson**2 # Calculate the R-squared value
    return slope, intercept, r_squared


# ==========================================
# 1. PARÁMETROS GLOBALES Y ARCHIVOS
# ==========================================
# Archivos
archivos = list(Path("../data").glob("master_data_*.txt"))


# Listas de referencia para la lógica de filtrado y ubicación
nu_valores = ["0.01", "0.069", "0.1"]
T_valores = ["10000", "25000", "50000"]  # Se ajustan libremente T1, T2, T3
semillas = ["42", "69", "911"]


# Mapeo de tiempos a semillas específicas (Figura 2)
semilla_por_T = {
    T_valores[0]: semillas[0],
    T_valores[1]: semillas[1],
    T_valores[2]: semillas[2]
}


# Configuración para la Figura 1
T_maximo = T_valores[-1]  # Toma automáticamente el mayor T (último elemento)
semilla_fija = "42"


# ==========================================
# 2. LEER Y GUARDAR LOS DATOS
# ==========================================
datos_maestros = cargar_datos_maestros(archivos)

# ==========================================
# 3. CÁLCULO ESTADÍSTICO DE ALPHA (MEDIA Y DESVIACIÓN) 📊
# ==========================================
sample_size = 10  # Número de puntos al final de la simulación por semilla
stats_alpha = {}  # Diccionario para almacenar (mu, sigma) por cada nu

print("\n" + "="*50)
print("  ESTADÍSTICAS DEL EXPONENTE ALPHA (µ ± σ)")
print("="*50)

for nu in nu_valores:
    for T in T_valores:
        alphas_combinados = []
        
        for i, archivo in enumerate(archivos):
            nu_f, T_f, s_f = extraer_parametros(archivo)
            
            if nu_f == nu and T_f == T:
                valores_a = datos_maestros[i][1]
                ultimos_alfas = valores_a[-sample_size:]
                alphas_combinados.extend(ultimos_alfas)
        
        if alphas_combinados:
            mu = np.mean(alphas_combinados)
            sigma = np.std(alphas_combinados, ddof=1)
            print(f"Parámetros: ν = {nu:<5} | T = {T:<5} ---> Alpha = {mu:.4f} ± {sigma:.4f}  (N={len(alphas_combinados)})")
            
            # Guardamos la estadística para T_maximo (utilizado en las gráficas)
            if T == T_maximo:
                stats_alpha[nu] = (mu, sigma)

print("="*50 + "\n")


# ==========================================
# 4. FIGURA 1: EVOLUCIÓN DE ALFA 📈
# ==========================================
fig_alfa, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
ejes_alfa = [ax1, ax2, ax3]

for i, archivo in enumerate(archivos):
    nu, T, s = extraer_parametros(archivo)

    if T == T_maximo and s == semilla_fija:
        indice = nu_valores.index(nu)
        
        ejes_alfa[indice].plot(datos_maestros[i][0][3::2], datos_maestros[i][1][3::2], "-*", color='blue')
        ejes_alfa[indice].set_xlabel('Tiempo (t)')
        ejes_alfa[indice].set_ylabel(r'Exponente $\alpha$')
        ejes_alfa[indice].tick_params(top=True, right=True, direction='in')
        
        # Título con nu y el valor de alpha con su incertidumbre
        mu, sigma = stats_alpha.get(nu, (0.0, 0.0))
        ejes_alfa[indice].set_title(f"\\nu = {nu} (T = {T})\n$\\alpha = {mu:.4f} \\pm {sigma:.4f}$")

fig_alfa.suptitle("Evolución temporal del exponente \\alpha (T Máximo)", fontsize=14)
fig_alfa.tight_layout()


# ==========================================
# 5. FIGURA 2: DISTRIBUCIÓN (LOG-LOG) 📊
# ==========================================
fig_log, (ax11, ax22, ax33) = plt.subplots(1, 3, figsize=(15, 5))
ejes_log = [ax11, ax22, ax33]

colors = {
    T_valores[0]: "tab:blue",
    T_valores[1]: "tab:green",
    T_valores[2]: "tab:red",
}

for i, archivo in enumerate(archivos):
    nu, T, s = extraer_parametros(archivo)

    if s == semilla_por_T[T]:
        indice = nu_valores.index(nu)

        texto_tuplas = datos_maestros[i][2]
        lista_pares = texto_tuplas.strip(" ()\n").split(")(")
        lista_S = []
        lista_N = []

        for par in lista_pares:
            if ',' in par:
                numeros = par.split(',')
                lista_S.append(float(numeros[0]))
                lista_N.append(float(numeros[1]))
                
        S_invertida = lista_S[::-1]
        N_invertida = lista_N[::-1]

        acumulada = 0
        lista_acumulada = []
        for n in N_invertida:
            acumulada += n
            lista_acumulada.append(acumulada)

        eje_x = np.log(S_invertida)
        eje_y = np.log(lista_acumulada)
                
        ejes_log[indice].plot(eje_x, eje_y, marker='o', linestyle='none', color=colors[T], label=f"T = {T}", alpha=0.5)

        slope, intercept, _ = linear_regression(eje_x, eje_y)
        x_full = np.linspace(min(eje_x) - 0.01*max(eje_x), max(eje_x) + 0.01*max(eje_x), 100)
        ejes_log[indice].plot(x_full, slope*x_full + intercept, color=colors[T])

        ejes_log[indice].set_xlabel('Ln(S)')
        ejes_log[indice].set_ylabel('Ln(Frecuencia Acumulada)')
        ejes_log[indice].tick_params(top=True, right=True, direction='in')

        # Título con nu y el valor de alpha con su incertidumbre
        mu, sigma = stats_alpha.get(nu, (0.0, 0.0))
        ejes_log[indice].set_title(f"\\nu = {nu}\n$\\alpha = {mu:.4f} \\pm {sigma:.4f}$")

for ax in ejes_log:
    ax.legend()

fig_log.suptitle("Distribución de tamaños (Log-Log)", fontsize=14)
fig_log.tight_layout()


# ==========================================
# 6. GUARDAR Y MOSTRAR RESULTADOS 📄
# ==========================================
Path('../results').mkdir(parents=True, exist_ok=True)
fig_alfa.savefig('../results/ALPHA.pdf', dpi=300)
fig_log.savefig('../results/DISTRIBUCION_LOG.pdf', dpi=300)

plt.show()
