import tkinter as tk

# Function to handle button click
def on_button_click():
    global button_flag
    if button_flag:
        result_label.config(text="не нажимай ебанат")
        button_flag = False
    else:
        result_label.config(text="заебись красава")
        button_flag = True

# Create the main window
root = tk.Tk()

# Set the title of the window
root.title("IGKA")

# Set the window size
root.geometry("800x800")

# Configure the grid to have one column that expands
root.grid_columnconfigure(0, weight=1)
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
label.grid(row=0, column=0, pady=20, sticky=tk.N, padx=20)

button_flag = True
# Create a button widget
button = tk.Button(root, text="Do not click", command=on_button_click)
button.grid(row=1, column=0, pady=20, sticky=tk.N)

# Create a label to display the result below the button
result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, pady=20, sticky=tk.N)

# Create an entry widget
entry = tk.Entry(root, width=40)
entry.grid(row=3, column=0, pady=20, sticky=tk.N)

# Add a label above the checkboxes
checkbox_label = tk.Label(root, text="Выберите форматы, в которых необходимо получить изображение")
checkbox_label.grid(row=4, column=0, pady=20, sticky=tk.W)

# Create a frame for checkboxes and radiobuttons
checkbox_frame = tk.Frame(root)
checkbox_frame.grid(row=5, column=0, pady=20, sticky=tk.W, padx=20)

# Create a subframe for checkboxes
format_frame = tk.Frame(checkbox_frame)
format_frame.pack(side=tk.LEFT)

# Create BooleanVar variables for checkboxes
checkbox_vars = [tk.BooleanVar() for _ in range(7)]
checkbox_labels = [ "Информационные доски (Формат А3, 297*420мм)", 
                    "Тейбл-тенты (Формат А4, 148*210мм)",
                    "Экраны блокировки ПК (FullHD 1920*1080 px)", 
                    "Кликабельный баннер, 1200*593 px",
                    "Кликабельный баннер, 1200*520 px", 
                    "Иллюстрация к новости, 700*1080 px", 
                    "Иллюстрация на анонс, 1084х585 px"]

# Create checkboxes inside the format frame
for i, (var, label) in enumerate(zip(checkbox_vars, checkbox_labels)):
    checkbox = tk.Checkbutton(format_frame, text=label, variable=var)
    checkbox.pack(anchor=tk.W, pady=5)

# Create a subframe for radiobuttons
color_frame = tk.Frame(checkbox_frame)
color_frame.pack(side=tk.LEFT, padx=20)

# Add a label for the color selection
color_label = tk.Label(color_frame, text="Выберите цвет")
color_label.pack(anchor=tk.W, pady=(0, 5))

# Create IntVar for Radiobuttons
color_var = tk.IntVar()
color_labels = [f"Цвет {i}" for i in range(1, 9)]

# Create Radiobuttons inside the color frame for color selection
for i, label in enumerate(color_labels):
    radiobutton = tk.Radiobutton(color_frame, text=label, variable=color_var, value=i+1)
    radiobutton.pack(anchor=tk.W)

# Function to handle text processing
def process_text():
    input_text = entry.get()
    checkbox_values = [1 if var.get() else 0 for var in checkbox_vars]
    selected_color = color_var.get()
    # Here you can add code to process the input_text with your neural network
    result_process.config(text=f"Processed: {input_text}, Checkboxes: {checkbox_values}, Color: {selected_color}")

# Create a process button
process_button = tk.Button(root, text="Process Text", command=process_text)
process_button.grid(row=12, column=0, pady=20, sticky=tk.N)

result_process = tk.Label(root, text="")
result_process.grid(row=13, column=0, pady=20, sticky=tk.N)

# Run the application
root.mainloop()
