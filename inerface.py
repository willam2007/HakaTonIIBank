import tkinter as tk


# Function to handle button click
def on_button_click():
    global button_flag
    if (button_flag):
     result_label.config(text="не нажимай ебанат")
     button_flag=False
    else:
     result_label.config(text="заебись красава")
     button_flag=True

# Create the main window
root = tk.Tk()

# Set the title of the window
root.title("IGKA")

# Set the window size
root.geometry("800x800")

# Configure the grid to have one column that expands
root.grid_columnconfigure(0, weight=1)

# Create a label widget
label = tk.Label(root, text="1 Billion Dollar App")
label.grid(row=0, column=0, pady=20, sticky=tk.N)


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

# Function to handle text processing
def process_text():
    input_text = entry.get()
    # Here you can add code to process the input_text with your neural network
    result_process.config(text=f"Processed: {input_text}")

# Create a process button
process_button = tk.Button(root, text="Process Text", command=process_text)
process_button.grid(row=4, column=0, pady=20, sticky=tk.N)

result_process = tk.Label(root, text="")
result_process.grid(row=5,column=0,pady=20,sticky=tk.N)
# Run the application
root.mainloop()
