import tkinter as tk
from dkd import *

root = tk.Tk()  # создание окна
root.title("IGKA")  # заголовок окна
root.geometry("1024x800")  # установка размеров
root.resizable(height=True, width=True)  # закрепление размеров

# Configure the grid to have columns and multiple rows that expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_rowconfigure(11, weight=1)
root.grid_rowconfigure(12, weight=1)
root.grid_rowconfigure(13, weight=1)

# Create a label widget
label = tk.Label(root, text="1 Billion Dollar App")
label.grid(row=0, column=0, pady=20, sticky=tk.NS)

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, pady=20, sticky=tk.NS)

# Create an entry widget
entry = tk.Entry(root, width=40, fg='grey')
entry.insert(0, "Введите ваш запрос")
entry.grid(row=3, column=0, pady=20, sticky=tk.NS)

def on_entry_click(event):
    if entry.get() == "Введите ваш запрос":
        entry.delete(0, "end") # delete all the text in the entry
        entry.insert(0, '') #Insert blank for user input
        entry.config(fg='black')

entry.bind('<FocusIn>', on_entry_click)

# Add a label above the checkboxes
checkbox_label = tk.Label(root, text="Выберите форматы, в которых необходимо получить изображение")
checkbox_label.grid(row=4, column=0, pady=20, sticky=tk.NS)

# Create BooleanVar variables for checkboxes
checkbox_vars = [tk.BooleanVar() for _ in range(7)]
checkbox_labels = [ "Информационные доски (Формат А3, 297*420мм)", 
                    "Тейбл-тенты (Формат А4, 148*210мм)",
                    "Экраны блокировки ПК (FullHD 1920*1080 px)", 
                    "Кликабельный баннер, 1200*593 px",
                    "Кликабельный баннер, 1200*520 px", 
                    "Иллюстрация к новости, 700*1080 px", 
                    "Иллюстрация на анонс, 1084х585 px"]

# Options for dropdown menus
dropdown_options_first = ["PNG", "JPG", "PDF", "PPTX"]
dropdown_options_second = ["PNG", "JPG", "PDF"]
dropdown_options_others = ["PNG", "JPG"]

# Add label for color selection dropdown
color_label = tk.Label(root, text="Выбор цвета")
color_label.grid(row=4, column=1, pady=20, sticky=tk.N)

# Options for color dropdown menu
color_options = ["Цвет 1", "Цвет 2", "Цвет 3", "Цвет 4", "Цвет 5", "Цвет 6", "Цвет 7", "Цвет 8"]

# Create color dropdown menu
selected_color = tk.StringVar(root)
selected_color.set(color_options[0])  # set default value
color_dropdown = tk.OptionMenu(root, selected_color, *color_options)
color_dropdown.grid(row=5, column=1, pady=5, sticky=tk.W, padx=50)

# Create a list to store dropdown menus' StringVar and corresponding options list
dropdown_vars = []
dropdown_options_list = []

# Create checkboxes and dropdown menus
for i, (var, label) in enumerate(zip(checkbox_vars, checkbox_labels), start=6):
    checkbox = tk.Checkbutton(root, text=label, variable=var, command=lambda: check_checkbox_state())
    checkbox.grid(row=i, column=0, pady=5, sticky=tk.W, padx=50)

    # Create dropdown menu
    selected_option = tk.StringVar(root)
    if i == 7:  # First dropdown menu
        selected_option.set(dropdown_options_first[0])  # set default value
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_first)
        dropdown_options_list.append(dropdown_options_first)
    elif i == 6:  # Second dropdown menu
        selected_option.set(dropdown_options_second[0])  # set default value
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_second)
        dropdown_options_list.append(dropdown_options_second)
    else:  # Other dropdown menus
        selected_option.set(dropdown_options_others[0])  # set default value
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_others)
        dropdown_options_list.append(dropdown_options_others)
    
    dropdown.grid(row=i, column=1, pady=5, sticky=tk.W, padx=50)
    dropdown_vars.append(selected_option)  # Add the dropdown variable to the list

def check_checkbox_state():
    if any(var.get() for var in checkbox_vars):
        process_button.config(state=tk.NORMAL)
    else:
        process_button.config(state=tk.DISABLED)

# Function to handle text processing
def process_text():
    input_text = entry.get()
    checkbox_values = []
    for idx, (var, dropdown_var) in enumerate(zip(checkbox_vars, dropdown_vars)):
        status = int(var.get())
        try:
            format_index = dropdown_options_list[idx].index(dropdown_var.get()) + 1
        except ValueError:
            format_index = 0  # если формат не найден, установить значение по умолчанию
        checkbox_values.append(f"{status}{format_index}")
    selected_color_index = color_options.index(selected_color.get()) + 1
    creation(input_text,checkbox_values,selected_color_index)
    result_process.config(text=f"Processed: {input_text}, Checkboxes: {checkbox_values}, Color: {selected_color_index}")

# Create a process button
process_button = tk.Button(root, text="Process Text", command=process_text, state=tk.DISABLED)
process_button.grid(row=12, column=0, pady=20, sticky=tk.N)

result_process = tk.Label(root, text="")
result_process.grid(row=13, column=0, pady=20, sticky=tk.N)

# Initial check to set the button state
check_checkbox_state()

root.mainloop()
