import tkinter as tk
from tkinter import ttk
from math import sqrt, pi, tan

# Функции расчета
def calculate_hit_probability(target_crossection, distance, weapon_arc, skill_difference, distance_change):
    target_radius = sqrt(target_crossection / pi)
    hit_probability = (target_radius - (distance_change * (1 + skill_difference * 0.1))) / (
        tan(weapon_arc / 2) * distance
    )
    return max(0, min(1, hit_probability))  # Вероятность в пределах [0, 1]

def calculate_movement_change(acceleration, time):
    return 0.5 * acceleration * time**2

# Функция обновления данных
def update():
    try:
        target_crossection = float(entry_target_crossection.get())
        distance = float(entry_distance.get())
        weapon_arc = float(entry_weapon_arc.get())
        skill_difference = float(entry_skill_difference.get())
        distance_change = float(entry_distance_change.get())
        acceleration = float(entry_acceleration.get())
        time = float(entry_time.get())
        
        hit_probability = calculate_hit_probability(
            target_crossection, distance, weapon_arc, skill_difference, distance_change
        )
        movement_change = calculate_movement_change(acceleration, time)
        
        label_result.config(
            text=f"Вероятность попадания: {hit_probability:.2%}\n"
                 f"Изменение положения: {movement_change:.2f} км"
        )
        
        draw_graph(target_crossection, distance_change, movement_change)
    except ValueError:
        label_result.config(text="Введите корректные числовые значения!")

# Рисование графика
def draw_graph(crossection, distance_change, movement_change):
    canvas.delete("all")
    target_radius = sqrt(crossection / pi)
    
    # Центр цели
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    
    # Окружность цели
    canvas.create_oval(
        center_x - target_radius, center_y - target_radius,
        center_x + target_radius, center_y + target_radius,
        outline="blue", width=2, tags="target"
    )
    
    # Снаряд
    canvas.create_oval(
        center_x - distance_change, center_y - distance_change,
        center_x + distance_change, center_y + distance_change,
        outline="red", width=2, tags="missile"
    )

# Интерфейс
root = tk.Tk()
root.title("Расчет попадания в космический корабль")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Поля ввода
labels = [
    "Площадь поперечного сечения цели (км²):",
    "Расстояние до цели (км):",
    "Угол оружия (рад):",
    "Разница в навыках (от -1 до 1):",
    "Изменение расстояния (км):",
    "Ускорение (км/с²):",
    "Время (с):",
]
entries = []

for i, label_text in enumerate(labels):
    ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky=tk.W)
    entry = ttk.Entry(frame, width=15)
    entry.grid(row=i, column=1, sticky=tk.W)
    entries.append(entry)

(entry_target_crossection, entry_distance, entry_weapon_arc,
 entry_skill_difference, entry_distance_change, entry_acceleration,
 entry_time) = entries

# Результаты
label_result = ttk.Label(frame, text="Результаты появятся здесь", foreground="green")
label_result.grid(row=len(labels), column=0, columnspan=2, sticky=tk.W)

# Кнопка расчета
ttk.Button(frame, text="Рассчитать", command=update).grid(row=len(labels) + 1, column=0, columnspan=2)

# Канва для графики
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.grid(row=1, column=0, sticky=(tk.W, tk.E))

root.mainloop()
