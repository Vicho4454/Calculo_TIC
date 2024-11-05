import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import minimize_scalar

# Parámetros de la elipse y de la circunferencia
a = 2000  # Semieje mayor de la elipse
b = 1200  # Semieje menor de la elipse
r = 300   # Radio de la circunferencia
S_x, S_y = -1600, 0  # Coordenadas del punto S

# Definimos las funciones de las coordenadas de T
def x_t(t):
    return a * np.cos((2 * np.pi * t / 365) + (np.pi / 2))

def y_t(t):
    return b * np.sin((2 * np.pi * t / 365) + (np.pi / 2))

# Funciones de las coordenadas de P
def p_x(t):
    return x_t(t) + r * np.cos(2 * np.pi * t)

def p_y(t):
    return y_t(t) + r * np.sin(2 * np.pi * t)

# Función de distancia entre P(t) y S
def distancia(t):
    return np.sqrt((p_x(t) - S_x)**2 + (p_y(t) - S_y)**2)

# Función para graficar la trayectoria de T y P, y marcar el punto S
def graficar_trayectoria(t):
    x_t_val = x_t(t)
    y_t_val = y_t(t)
    x_p_val = p_x(t)
    y_p_val = p_y(t)

    plt.figure(figsize=(8, 8))
    
    # Trayectoria de T
    t_vals = np.linspace(0, 365, 1000)
    plt.plot(x_t(t_vals), y_t(t_vals), 'b--', label='Trayectoria de T (Elipse)')
    
    # Punto T en la elipse
    plt.plot(x_t_val, y_t_val, 'bo', label=f'Punto T en t={t}')
    
    # Circunferencia alrededor de T
    theta_vals = np.linspace(0, 2 * np.pi, 100)
    plt.plot(x_t_val + r * np.cos(theta_vals), y_t_val + r * np.sin(theta_vals), 'g-', label='Circunferencia alrededor de T')
    
    # Punto P en la circunferencia
    plt.plot(x_p_val, y_p_val, 'ro', label=f'Punto P en t={t}')
    
    # Marcamos el punto S
    plt.plot(S_x, S_y, 'ms', label='Punto S', markersize=8)

    # Configuración del gráfico
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.title(f'Trayectoria y posición de T y P para t={t}')
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.clf()

# Interfaz de Streamlit
st.title("Visualización de la trayectoria de T y P y distancia d(t) entre P y S")

# Slider para el parámetro t en la trayectoria de T y P
t = st.slider("Valor de t (días)", min_value=0, max_value=365, step=1, value=0)

# Graficar la trayectoria
graficar_trayectoria(t)

# Calcular la distancia actual y mostrarla como métrica
distancia_actual = distancia(t)
st.metric(label="Distancia d(t) entre P y S", value=f"{distancia_actual:.2f} unidades")

# Vector de tiempo para el gráfico de distancia
t_vals = np.linspace(0, 365, 1000)
d_vals = distancia(t_vals)

# Graficamos la función de distancia
plt.figure(figsize=(10, 6))
plt.plot(t_vals, d_vals, label='Distancia d(t)', color='blue')
plt.title('Función de distancia d(t) entre P y S', fontsize=16)
plt.xlabel('Tiempo t (días)', fontsize=14)
plt.ylabel('Distancia d(t)', fontsize=14)
plt.grid(True)

# Encontramos los puntos de mínimo y máximo
min_result = minimize_scalar(distancia, bounds=(0, 365), method='bounded')
max_result = minimize_scalar(lambda t: -distancia(t), bounds=(0, 365), method='bounded')

# Resultados de mínimo y máximo
t_min = min_result.x
d_min = min_result.fun
t_max = max_result.x
d_max = -max_result.fun  # Tomamos el valor negativo porque optimizamos la función -d(t)

# Marcamos los puntos mínimo y máximo en la gráfica
plt.scatter([t_min], [d_min], color='red', label=f'Mínimo en t={t_min:.2f}, d={d_min:.2f}')
plt.scatter([t_max], [d_max], color='green', label=f'Máximo en t={t_max:.2f}, d={d_max:.2f}')

plt.legend()
st.pyplot(plt.gcf())
plt.clf()

# Imprimimos los resultados numéricos
st.write(f"Distancia mínima en t = {t_min:.2f} días, d = {d_min:.2f}")
st.write(f"Distancia máxima en t = {t_max:.2f} días, d = {d_max:.2f}")
