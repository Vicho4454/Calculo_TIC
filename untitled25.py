import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Parámetros de la elipse y de la circunferencia
a = 2000  # Semieje mayor de la elipse
b = 1200  # Semieje menor de la elipse
r = 300   # Radio de la circunferencia
S_x, S_y = -1600, 0  # Coordenadas del punto S

# Definimos la variable simbólica para el tiempo
t_sym = sp.symbols('t')

# Definimos las funciones de las coordenadas de T en forma simbólica
x_t_sym = a * sp.cos((2 * np.pi * t_sym / 365) + (np.pi / 2))
y_t_sym = b * sp.sin((2 * np.pi * t_sym / 365) + (np.pi / 2))

# Coordenadas de P en función de t
p_x_sym = x_t_sym + r * sp.cos(2 * np.pi * t_sym)
p_y_sym = y_t_sym + r * sp.sin(2 * np.pi * t_sym)

# Función simbólica de distancia entre P(t) y S
d_t_sym = sp.sqrt((p_x_sym - S_x)**2 + (p_y_sym - S_y)**2)

# Convertimos la función simbólica de distancia a una función numérica
d_t_func = sp.lambdify(t_sym, d_t_sym, 'numpy')

# Función para calcular las coordenadas de T en la elipse
def centro_elipse(t):
    x_t = a * np.cos(2 * np.pi * t / 365 + np.pi / 2)
    y_t = b * np.sin(2 * np.pi * t / 365 + np.pi / 2)
    return x_t, y_t

# Función para calcular las coordenadas de P en la circunferencia alrededor de T
def punto_circunferencia(t):
    x_t, y_t = centro_elipse(t)
    x_p = x_t + r * np.cos(2 * np.pi * t)
    y_p = y_t + r * np.sin(2 * np.pi * t)
    return x_p, y_p

# Función para graficar la trayectoria de T y P, y marcar el punto S
def graficar_trayectoria(t=0):
    x_t, y_t = centro_elipse(t)
    x_p, y_p = punto_circunferencia(t)

    plt.figure(figsize=(8, 8))
    t_vals = np.linspace(0, 365, 200)  # Reducción de puntos
    x_vals, y_vals = centro_elipse(t_vals)
    plt.plot(x_vals, y_vals, 'b-', label='Trayectoria de T (Elipse)', linewidth=2)  # Línea sólida
    plt.plot(x_t, y_t, 'bo', label=f'Punto T en t={t}', markersize=8)  # Mayor tamaño para T
    theta_vals = np.linspace(0, 2 * np.pi, 100)
    x_circ = x_t + r * np.cos(theta_vals)
    y_circ = y_t + r * np.sin(theta_vals)
    plt.plot(x_circ, y_circ, 'g-', label='Circunferencia alrededor de T', linewidth=2)
    plt.plot(x_p, y_p, 'ro', label=f'Punto P en t={t}', markersize=8)  # Mayor tamaño para P
    
    # Marcamos el punto S en el gráfico
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

# Función para graficar la distancia entre P y S
def graficar_distancia():
    t_vals = np.linspace(0, 365, 500)  # Usar más puntos para suavizar
    d_vals = d_t_func(t_vals)

    # Encontrar máximos y mínimos
    d_min = np.min(d_vals)
    t_min = t_vals[np.argmin(d_vals)]
    d_max = np.max(d_vals)
    t_max = t_vals[np.argmax(d_vals)]

    plt.figure(figsize=(10, 6))
    plt.plot(t_vals, d_vals, label='Distancia d(t)', color='blue', linewidth=2)  # Línea más gruesa
    plt.title('Función de distancia d(t) entre P y S', fontsize=16)
    plt.xlabel('Tiempo t (días)', fontsize=14)
    plt.ylabel('Distancia d(t)', fontsize=14)

    # Anotar mínimos y máximos
    plt.annotate(f'Mínimo: d={d_min:.2f}\n en t={t_min:.2f}', xy=(t_min, d_min), 
                 xytext=(t_min + 10, d_min + 50),
                 arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=10, color='red')
    plt.annotate(f'Máximo: d={d_max:.2f}\n en t={t_max:.2f}', xy=(t_max, d_max), 
                 xytext=(t_max + 10, d_max + 50),
                 arrowprops=dict(facecolor='green', arrowstyle='->'), fontsize=10, color='green')

    plt.grid(False)  # Desactivar cuadrícula
    plt.legend(fontsize=12)
    st.pyplot(plt.gcf())
    plt.clf()

# Función para calcular la distancia actual entre P y S
def calcular_distancia_actual(t):
    return d_t_func(t)

# Interfaz de Streamlit
st.title("Visualización de la trayectoria de T y P y distancia d(t) entre P y S")

# Slider para el parámetro t en la trayectoria de T y P
t = st.slider("Valor de t (días)", min_value=0, max_value=365, step=1, value=0)
graficar_trayectoria(t)

# Calculamos la distancia actual y la mostramos como métrica
distancia_actual = calcular_distancia_actual(t)
st.metric(label="Distancia d(t) entre P y S", value=f"{distancia_actual:.2f} unidades")

if st.button("Mostrar gráfico de distancia d(t) entre P y S"):
    graficar_distancia()
