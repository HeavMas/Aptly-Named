import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def shot(h, alp): 
    return math.pi * (h * math.tan(math.radians(alp))) ** 2

def dispers(h, alp_dis):
    return math.pi * (h * math.tan(math.radians(alp_dis))) ** 2

def targ(rad):
    return math.pi * rad ** 2

def bias(h, vel, acc):
    return (h / vel) * acc

def intersection_area(r1, r2, d):
    if d >= r1 + r2:
        return 0  # Нет пересечения
    elif d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2  # Один круг полностью внутри другого
    
    part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
    
    return part1 + part2 - part3

def calculate():
    h = float(entry_h.get())
    alp = float(entry_alp.get())
    alp_dis = float(entry_alp_dis.get())
    rad_targ = float(entry_rad.get())
    vel = float(entry_vel.get())
    acc = float(entry_acc.get())
    
    r_hit = h * math.tan(math.radians(alp))
    r_disp = h * math.tan(math.radians(alp_dis))
    d = bias(h, vel, acc)
    
    S_targ = targ(rad_targ)
    S_disp = dispers(h, alp_dis)
    S_intersection = intersection_area(rad_targ, r_disp, d)
    
    probability = (S_intersection / S_disp) * 100 if S_disp > 0 else 0
    label_result.config(text=f"Вероятность попадания: {probability:.2f}%")
    
    plot_circles(rad_targ, r_hit, r_disp, d)

def plot_circles(target_radius, hit_radius, dispersion_radius, distance):
    ax.clear()
    ax.set_xlim(-dispersion_radius * 1.5, dispersion_radius * 1.5)
    ax.set_ylim(-dispersion_radius * 1.5, dispersion_radius * 1.5)
    
    target_circle = Circle((0, 0), target_radius, color='blue', alpha=0.5, label='Цель')
    hit_circle = Circle((distance, 0), hit_radius, color='red', alpha=0.5, label='Попадание')
    dispersion_circle = Circle((distance, 0), dispersion_radius, color='orange', alpha=0.3, label='Разброс')
    
    ax.add_patch(target_circle)
    ax.add_patch(hit_circle)
    ax.add_patch(dispersion_circle)
    
    ax.legend()
    canvas.draw()

root = tk.Tk()
root.title("Симуляция попадания снаряда")

frame = ttk.Frame(root)
frame.pack()

entry_h = ttk.Entry(frame)
entry_alp = ttk.Entry(frame)
entry_alp_dis = ttk.Entry(frame)
entry_rad = ttk.Entry(frame)
entry_vel = ttk.Entry(frame)
entry_acc = ttk.Entry(frame)

labels = ["Высота (h):", "Угол прицела (°):", "Разброс (°):", "Радиус цели:", "Скорость снаряда:", "Ускорение цели:"]
entries = [entry_h, entry_alp, entry_alp_dis, entry_rad, entry_vel, entry_acc]

ttks = zip(labels, entries)
for i, (label, entry) in enumerate(ttks):
    ttk.Label(frame, text=label).grid(row=i, column=0)
    entry.grid(row=i, column=1)

button_calculate = ttk.Button(frame, text="Рассчитать", command=calculate)
button_calculate.grid(columnspan=2)

label_result = ttk.Label(frame, text="Вероятность попадания: ")
label_result.grid(columnspan=2)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
