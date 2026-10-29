import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# 1. Encontrar los archivos
archivos = list(Path("../data").glob("master_data_*.txt"))  # ta_nu_T_semilla (master, data, nu, T, semilla)
# (Ajusta la ruta en Path() si tus archivos están en otra carpeta)

# 2. Leer y guardar los datos
datos_maestros = [] #datos_maestros será una lista de tuplas, cada tupla contiene (valores_t, valores_a, ultima_linea_tuplas)

for archivo in archivos:
    # Reiniciamos variables por cada archivo 
    valores_t = []
    valores_a = []
    ultima_linea_tuplas = ""
    
    with open(archivo, 'r') as f:
        for linea in f:
                
                # maxsplit=2 separa t, alfa y deja todas las tuplas juntas en el índice 2
                partes = linea.split(maxsplit=2) 
                if len(partes) >= 2:
                    valores_t.append(float(partes[0]))
                    valores_a.append(float(partes[1]))
                    
                if len(partes) == 3:
                    ultima_linea_tuplas = partes[2] 
    
    # Guardamos los datos de este archivo como una tupla
    datos_maestros.append((valores_t, valores_a, ultima_linea_tuplas))

# 3. FIGURA 1: Evolución de Alfa
fig_alfa, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
ejes_alfa = [ax1, ax2, ax3]

for i in range(len(archivos)): # Iteramos según la cantidad de archivos

    # Extraer variables del nombre del archivo
    nombre_archivo = archivos[i].name
    partes = nombre_archivo.split('_')
    nu = partes[2]
    T = partes[3] 
    
    # Graficar y configurar ejes (aplicando [::100] a AMBOS ejes para que midan lo mismo)
    ejes_alfa[i].plot(datos_maestros[i][0][3::50], datos_maestros[i][1][3::50], "-*", color='blue')  # Usamos [3::100] para saltar los primeros 3 valores y luego tomar cada 100
    ejes_alfa[i].set_xlabel('Tiempo (t)')
    ejes_alfa[i].set_ylabel(r'Exponente $\alpha$')
    ejes_alfa[i].tick_params(top=True, right=True, direction='in')
    
    # Título para cada gráfica individual
    ejes_alfa[i].set_title(f"\u03BD = {nu} y T = {T}")

# Título grande para toda la figura completa (FUERA DEL CICLO)
fig_alfa.suptitle("Evolución temporal del exponente \u03B1", fontsize=14)
fig_alfa.tight_layout() # Ajusta los márgenes automáticamente

# 4. FIGURA 2: Distribución (Log-Log)
fig_log, (ax11, ax22, ax33) = plt.subplots(1, 3, figsize=(15, 5))
ejes_log = [ax11, ax22, ax33]

for i in range(len(archivos)):
    # Extraer variables del nombre del archivo
    nombre_archivo = archivos[i].name
    partes = nombre_archivo.split('_')
    nu = partes[2]
    T = partes[3]

    texto_tuplas = datos_maestros[i][2]
    
    # 1 y 2. Limpieza del texto para extraer S y N
    lista_pares = texto_tuplas.strip(" ()\n").split(")(")
    lista_S = []
    lista_N = []

    for par in lista_pares:
        if ',' in par:
            numeros = par.split(',')
            lista_S.append(float(numeros[0]))
            lista_N.append(float(numeros[1]))
            
    # 3. Calcular la frecuencia acumulada (de mayor a menor)
    S_invertida = lista_S[::-1]
    N_invertida = lista_N[::-1]

    acumulada = 0
    lista_acumulada = []

    for n in N_invertida:
        acumulada += n
        lista_acumulada.append(acumulada)

    # 4. Calcular los logaritmos
    eje_x = np.log(S_invertida)
    eje_y = np.log(lista_acumulada)
            
    # 5. Graficar (usamos plot normal porque YA calculamos el Ln)
    ejes_log[i].plot(eje_x, eje_y, marker='o', linestyle='none', color='red')
    
    ejes_log[i].set_xlabel('Ln(S)')
    ejes_log[i].set_ylabel('Ln(Frecuencia Acumulada)')
    ejes_log[i].tick_params(top=True, right=True, direction='in')
    
    # Título para cada gráfica individual
    ejes_log[i].set_title(f"\u03BD = {nu} y T = {T}")

# Título grande para toda la figura completa y ajuste final (FUERA DEL CICLO)
fig_log.suptitle("Distribución de tamaños (Log-Log)", fontsize=14)
fig_log.tight_layout()

# 5. Guardar los PDFs por separado
fig_alfa.savefig('../results/ALPHA.pdf', dpi=300)
fig_log.savefig('../results/DISTRIBUCION_LOG.pdf', dpi=300) 
# (Nota: asegúrate de que la carpeta '../results/' exista en tu computadora)

plt.show() # Para visualizar las gráficas en tu pantalla