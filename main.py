import pyautogui
import keyboard
import mouse
import math
import time
import tkinter as tk

scale_factor = None  # global var to save scaling

# shortcuts
start_shortcut = 'alt+q'
point_shortcut = 'alt+left'

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def create_static_window():
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("+10+10")
    window.attributes("-topmost", True)
    label = tk.Label(window, font=("Helvetica", 14), bg="yellow", padx=10, pady=5)
    label.pack()
    return window, label

def get_position_on_custom_click():
    pos = None
    def on_click(event):
        nonlocal pos
        if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down' and event.button == 'left' and keyboard.is_pressed(point_shortcut.split('+')[0]):
            pos = pyautogui.position()
            mouse.unhook(on_click)

    mouse.hook(on_click)
    while pos is None:
        time.sleep(0.05)
    return pos

def start_measurement():
    global scale_factor
    window, label = create_static_window()
    label.config(text=f"Set scale: 100 meters (Alt+Left Mouse Button)")
    window.update()

    point1 = get_position_on_custom_click()

    label.config(text=f"Press Alt+Left Mouse Button for the second point (100 meters)")
    window.update()
    point2 = get_position_on_custom_click()

    distance_in_pixels = calculate_distance(point1, point2)
    if distance_in_pixels == 0:
        label.config(text="Something wrong: set different points!")
        window.update()
        time.sleep(2)
        window.destroy()
        return

    scale_factor = 100 / distance_in_pixels
    label.config(text=f"100 meters = {distance_in_pixels:.2f} pixels")
    window.update()
    time.sleep(2)

    label.config(text=f"Measure the distance (Alt+Left Mouse Button)")
    window.update()

    point1 = get_position_on_custom_click()
    label.config(text=f"Press Alt+Left Mouse Button for the second point")
    window.update()
    point2 = get_position_on_custom_click()

    distance_in_pixels = calculate_distance(point1, point2)
    distance_in_meters = distance_in_pixels * scale_factor
    label.config(text=f"Distance: {distance_in_meters:.2f} meters")
    window.update()
    time.sleep(3)
    window.destroy()

def create_control_window():
    # create window
    control_window = tk.Tk()
    control_window.title("Control information")
    control_window.geometry("300x150")
    control_window.attributes("-topmost", True)

    # text
    info_text = (
        "Control:\n"
        "Alt + Q: Start measurement\n"
        "Alt + Left Mouse Button: Set point\n\n"
        "With love from Bulldo"
    )

    message_label = tk.Label(control_window, text=info_text, font=("Helvetica", 12), justify="left")
    message_label.pack(pady=20)

    control_window.mainloop()

keyboard.add_hotkey(start_shortcut, start_measurement)
keyboard.add_hotkey(point_shortcut, get_position_on_custom_click)

print("The program works. Use key combinations to control.")
create_control_window()
