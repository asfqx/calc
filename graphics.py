import matplotlib.pyplot as plt
import numpy as np


def plot_linear(a, b):
    x = np.linspace(-10, 10, 400)
    y = a * x + b
    plt.plot(x, y, label=f"{a}x + {b}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

def plot_quadratic(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    plt.plot(x, y, label=f"{a}x² + {b}x + {c}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

def plot_trig(func_type):
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400)
    if func_type == "sin":
        y = np.sin(x)
        label = "sin(x)"
    elif func_type == "cos":
        y = np.cos(x)
        label = "cos(x)"
    elif func_type == "tan":
        y = np.tan(x)
        label = "tan(x)"
    plt.plot(x, y, label=label)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.ylim(-10, 10)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()