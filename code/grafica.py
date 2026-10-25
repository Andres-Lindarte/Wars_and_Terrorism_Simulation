import numpy as np
import matplotlib.pyplot as plt

valores_t = []
valores_a = []
ultima_linea_tuplas = ""

# 1. Leer los datos
with open("../results/master_data.txt", 'r') as f:
    for linea in f:
        # maxsplit=2 separa t, alfa y deja todas las tuplas juntas en el índice 2
        partes = linea.split(maxsplit=2) 
        if len(partes) >= 2:
            valores_t.append(float(partes[0]))
            valores_a.append(float(partes[1]))
            
        if len(partes) == 3:
            ultima_linea_tuplas = partes[2]

# 2. Procesar las tuplas de la última iteración
# Quitamos saltos de línea y paréntesis de los extremos, luego cortamos por ")("
lista_pares = ultima_linea_tuplas.strip(" ()\n").split(")(")

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

# 5. Graficar ambas juntas
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica 1: t vs alfa
ax1.plot(valores_t, valores_a, color='blue')
ax1.set_xlabel('Tiempo (t)')
ax1.set_ylabel(r'Exponente $\alpha$')
ax1.set_title(r'Evolución temporal de $\alpha$')
ax1.tick_params(top=True, right=True, direction='in')

# Gráfica 2: Ln(S) vs Ln(Acumulada)
ax2.plot(eje_x, eje_y, marker='o', linestyle='', color='red')
ax2.set_xlabel('Ln(S)')
ax2.set_ylabel('Ln(Frecuencia Acumulada)')
ax2.set_title('Distribución en la última iteración')
ax2.tick_params(top=True, right=True, direction='in')

plt.savefig('../results/ALPHA.pdf', dpi=300) # Guardar la figura en un archivo

plt.tight_layout() # Ajusta los espacios para que no se superpongan
plt.show()