import tkinter as tk
from dkd import *
from ImageTextAdder import *
from image_generation import *

root = tk.Tk()  # создание окна
root.title("IGKA")  # заголовок окна
root.geometry("1250x800")  # установка размеров
root.resizable(height=True, width=True)  # закрепление размеров

# Столбы и строки страницы
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
root.grid_rowconfigure(14, weight=1)

label = tk.Label(root, text="1 Billion Dollar App")
label.grid(row=0, column=0, pady=20, sticky=tk.EW)

default_texts = {                           #надписи-подсказки в поля для ввода
    "zapros": "Введите ваш запрос",
    "title": "Введите заголовок",
    "subtitle": "Введите подзаголовок",
    "button": "Введите текст для кнопки/дату и время"
}

# Создание поля для запроса
entry_zapros = tk.Entry(root, width=40, fg='grey')
entry_zapros.insert(0, default_texts["zapros"])
entry_zapros.grid(row=1, column=0, pady=0, sticky=tk.NW, padx=100)

def on_zapros_click(event):
    if entry_zapros.get() == default_texts["zapros"]:
        entry_zapros.delete(0, "end")  # delete all the text in the entry
        entry_zapros.insert(0, '')     #Insert blank for user input
        entry_zapros.config(fg='green')

entry_zapros.bind('<FocusIn>', on_zapros_click)

# Создание поля для заголовка
entry_title = tk.Entry(root, width=40, fg='grey')
entry_title.insert(0, default_texts["title"])
entry_title.grid(row=1, column=1, pady=(0,0), sticky=tk.NW)

def on_title_click(event):
    if entry_title.get() == default_texts["title"]:
        entry_title.delete(0, "end") # delete all the text in the entry
        entry_title.insert(0, '') #Insert blank for user input
        entry_title.config(fg='blue')

entry_title.bind('<FocusIn>', on_title_click)

# Создание поля для подзаголовка
entry_subtitle = tk.Entry(root, width=40, fg='grey')
entry_subtitle.insert(0, default_texts["subtitle"])
entry_subtitle.grid(row=2, column=1, pady=(0,0), sticky=tk.NW)

def on_subtitle_click(event):
    if entry_subtitle.get() == default_texts["subtitle"]:
        entry_subtitle.delete(0, "end") # delete all the text in the entry
        entry_subtitle.insert(0, '') #Insert blank for user input
        entry_subtitle.config(fg='blue')

entry_subtitle.bind('<FocusIn>', on_subtitle_click)

# Создание поля для кнопки
entry_button = tk.Entry(root, width=40, fg='grey')
entry_button.insert(0, default_texts["button"])
entry_button.grid(row=3, column=1, pady=(0,0), sticky=tk.NW)

def on_button_click(event):
    if entry_button.get() == default_texts["button"]:
        entry_button.delete(0, "end") # delete all the text in the entry
        entry_button.insert(0, '') #Insert blank for user input
        entry_button.config(fg='blue')

entry_button.bind('<FocusIn>', on_button_click)


# Текст над параметрами избражения
checkbox_label = tk.Label(root, text="Выберите форматы, в которых необходимо получить изображение")
checkbox_label.grid(row=3, column=0, pady=20, sticky=tk.W, padx=100)

# Элементы для чекбокса
checkbox_vars = [tk.BooleanVar() for _ in range(7)]
checkbox_labels = [ "Информационные доски (Формат А3, 297*420мм)", 
                    "Тейбл-тенты (Формат А4, 148*210мм)",
                    "Экраны блокировки ПК (FullHD 1920*1080 px)", 
                    "Кликабельный баннер,  1200*593 px",
                    "Кликабельный баннер, 1200*520 px", 
                    "Иллюстрация к новости, 700*1080 px", 
                    "Иллюстрация на анонс, 1084х585 px"]

# Параметры для выпадающего меню
dropdown_options_first = ["PNG", "JPG", "PDF", "PPTX"]
dropdown_options_second = ["PNG", "JPG", "PDF"]
dropdown_options_others = ["PNG", "JPG"]


# Лейбл выбора цвета фона
color_label = tk.Label(root, text="Выбор цвета фона")
color_label.grid(row=4, column=0, pady=0, sticky=tk.E)

# Параметры для выпадающего меню с цветами
color_options = ["Cиний", "Красный", "Оранжевый", "Серый", "Светло-голубой", "Светло-красный", "Светло-оранжевый", "Светло-серый"]

# Создание выпадающего меню с цветами фона
selected_color = tk.StringVar(root)
selected_color.set(color_options[0])  # set default value
color_dropdown = tk.OptionMenu(root, selected_color, *color_options)
color_dropdown.grid(row=4, column=1, pady=2, sticky=tk.W, padx=0)


# Цвета
colortext_options = ["Cиний", "Красный", "Оранжевый", "Серый", "Светло-голубой", "Светло-красный", "Светло-оранжевый", "Светло-серый"]

# Лейбл выбора цвета заголовка
colortext_label = tk.Label(root, text="Выбор цвета заголовка")
colortext_label.grid(row=5, column=0, pady=0, sticky=tk.E)
# создание выпадающего меню для цвета заголовка
selected_colortext = tk.StringVar(root)
selected_colortext.set(colortext_options[0])  # set default value
colortext_dropdown = tk.OptionMenu(root, selected_colortext, *colortext_options)
colortext_dropdown.grid(row=5, column=1, pady=2, sticky=tk.W, padx = 0)

# Лейбл выбора цвета подзаголовка
colorsubtitle_label = tk.Label(root, text="Выбор цвета подзаголовка")
colorsubtitle_label.grid(row=6, column=0, pady=0, sticky=tk.E)
# создание выпадающего меню для цвета подзаголовка
selected_colorsubtitle = tk.StringVar(root)
selected_colorsubtitle.set(colortext_options[0])  # set default value
colorsubtitle_dropdown = tk.OptionMenu(root, selected_colorsubtitle, *colortext_options)
colorsubtitle_dropdown.grid(row=6, column=1, pady=2, sticky=tk.W, padx = 0)

# Лейбл выбора цвета кнопки
colorbutton_label = tk.Label(root, text="Выбор цвета кнопки/инфо")
colorbutton_label.grid(row=7, column=0, pady=0, sticky=tk.E)
# создание выпадающего меню для цвета подзаголовка
selected_colorbutton = tk.StringVar(root)
selected_colorbutton.set(colortext_options[0])  # set default value
colorbutton_dropdown = tk.OptionMenu(root, selected_colorbutton, *colortext_options)
colorbutton_dropdown.grid(row=7, column=1, pady=2, sticky=tk.W, padx = 0)


dropdown_vars = []
dropdown_options_list = []

# создание чекбокса и меню выбора форматов
for i, (var, label) in enumerate(zip(checkbox_vars, checkbox_labels), start=4):
    checkbox = tk.Checkbutton(root, text=label, variable=var, command=lambda: check_checkbox_state())
    checkbox.grid(row=i, column=0, pady=0, sticky=tk.W, padx=160)

    # меню выбора форматов
    selected_option = tk.StringVar(root)
    if i == 5: # с ПДФ
        selected_option.set(dropdown_options_first[0]) 
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_first)
        dropdown_options_list.append(dropdown_options_first)
    elif i == 4:  # с ПДФ и ПП
        selected_option.set(dropdown_options_second[0])  
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_second)
        dropdown_options_list.append(dropdown_options_second)
    else:  # остальные(png,jpg)
        selected_option.set(dropdown_options_others[0])  
        dropdown = tk.OptionMenu(root, selected_option, *dropdown_options_others)
        dropdown_options_list.append(dropdown_options_others)
    
    dropdown.grid(row=i, column=0, pady=5, sticky=tk.W, padx=80)
    dropdown_vars.append(selected_option)

def check_checkbox_state():
    if any(var.get() for var in checkbox_vars):
        process_button.config(state=tk.NORMAL)
    else:
        process_button.config(state=tk.DISABLED)


def process_text():

    zapros_text = entry_zapros.get() if entry_zapros.get() != default_texts["zapros"] else ""
    title_text = entry_title.get() if entry_title.get() != default_texts["title"] else ""
    subtitle_text = entry_subtitle.get() if entry_subtitle.get() != default_texts["subtitle"] else ""
    button_text = entry_button.get() if entry_button.get() != default_texts["button"] else ""

    checkbox_values = []
    for idx, (var, dropdown_var) in enumerate(zip(checkbox_vars, dropdown_vars)):
        status = int(var.get())
        try:
            format_index = dropdown_options_list[idx].index(dropdown_var.get()) + 1
        except ValueError:
            format_index = 0  # если формат не найден, установить значение по умолчанию
        checkbox_values.append(f"{status}{format_index}")
    selected_color_index = color_options.index(selected_color.get()) + 1
    selected_colortext_index = colortext_options.index(selected_colortext.get()) + 1
    selected_colorsubtitle_index = colortext_options.index(selected_colorsubtitle.get()) + 1
    selected_colorbutton_index = colortext_options.index(selected_colorbutton.get()) + 1
    print(" Заголовок: ", selected_colortext_index , 
          " Подзаголовок: " ,selected_colorsubtitle_index, 
          " Кнопка/инфо: "  ,selected_colorbutton_index)
    result_process.config(text=f"Processed: {zapros_text}, Checkboxes: {checkbox_values}, Color: {selected_color_index}, Colortext: {selected_colortext_index}, Title: {title_text}, Subitle: {subtitle_text}, Button: {button_text}")


    creation(zapros_text,checkbox_values,selected_color_index) 
#####################
    font_path = "arialmt.ttf"
    folder_path = "output/"
    colorshrift = choosecolor(selected_colortext_index)

    adder = ImageTextAdder(font_path)
    adder.process_images_in_folder(folder_path, title_text, subtitle_text, button_text, colorshrift)
    #******************************************************************************************
    text_query = title_text #передаю титульник в промт
    translated_text = translate_to_english(text_query) #перевожу текст промта для нейро
    best_image_path = find_best_image(translated_text) #ищу картинку по промту
    print("Best image path:", best_image_path) #проверка работы выбора картинки
    #print(output_path)
    for filename in os.listdir(folder_path):
            base_image_path = os.path.join(folder_path, filename)
    #base_image_path = os.path.altsep("output/") #путь по которому находится image на 2 этапе обработки
    print(base_image_path)
    selected_image_path = os.path.abspath(best_image_path)  # Путь к изображению, выбранному нейросетью
    output_image_path = 'finaly/output_image.png' #Название файла на 3 этапе
    insert_image(base_image_path, selected_image_path, output_image_path)

    result_process.config(text=f"Processed: {zapros_text}, Checkboxes: {checkbox_values}, Color: {selected_color_index}, Colortext: {selected_colortext_index}, Title: {title_text}, Subitle: {subtitle_text}, Button: {button_text}")

# Создание "process button"
process_button = tk.Button(root, text="Process Text", command=process_text, state=tk.DISABLED)
process_button.grid(row=13, column=0, pady=20, sticky=tk.N)

result_process = tk.Label(root, text="")
result_process.grid(row=14, column=0, pady=20, sticky=tk.N)

# Начальная проверка чекбоксов(чтоб кнопка без выбранного варианта не работала)
check_checkbox_state()

root.mainloop()
