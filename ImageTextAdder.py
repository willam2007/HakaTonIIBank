from PIL import Image, ImageDraw, ImageFont
import os

class ImageTextAdder:
    def __init__(self, font_path):
        self.font_path = font_path
    
    def get_size(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        return width, height, image

    def add_text(self, image_path, text):
        # Получаем размеры изображения
        width, height, image = self.get_size(image_path)
        draw = ImageDraw.Draw(image)

        # Выбираем размер шрифта в зависимости от разрешения
        font_size = 150
        font = ImageFont.truetype(self.font_path, font_size)

        # Определяем позицию для текста в зависимости от разрешения
        position = self.create_global_container_position(width, height)

        color = (238, 17, 51)

        # Цвет текста в формате RGB
        # dark_blue_color = (0, 136, 187)
        # blue_color = (0, 187, 238)
        # red_color = (238, 17, 51)
        # light_red_color = (255, 90, 90)
        # orange_color = (255, 187, 68)
        # sand_color = (255, 204, 136)
        # black_color = (0, 0, 0)
        # gray_color = (85, 85, 85)

        # Добавляем текст на изображение
        draw.text(position, text, font=font, fill=color)

        if width <= height:
            self.add_rectangle(draw, position, width*0.8, height*0.4, outline_color="black", fill_color=None)
        else:
            self.add_rectangle(draw, position, width*0.55, height*0.8, outline_color="black", fill_color=None)

        # Сохраняем измененное изображение
        output_path = f"out_{os.path.basename(image_path)}"
        output_folder = "output"
        output_folder_path = os.path.join(os.getcwd(), output_folder)
        output_path = os.path.join(output_folder_path,  f"{os.path.basename(image_path)}")
        image.save(output_path)
        print(f"Saved image with text at: {output_path}")

    def add_rectangle(self, draw, position, rect_width, rect_height, outline_color, fill_color=None):
        x, y = position
        shape = [(x, y), (x + rect_width, y + rect_height)]
        draw.rectangle(shape, outline=outline_color, fill=fill_color, width=5)


    def create_global_container_position(self, width, height):
        if ((width == 1748) and (height == 2480)) or ((width == 3507) and (height == 4960)) or ((width == 700) and (height == 1080)):
            x = width*0.1; y = height*0.55
            return x,y
        elif ((width == 1084) and (height == 585)) or ((width == 1200) and (height == 520)) or ((width == 1200) and (height == 593)) or ((width == 1920) and (height == 1080)):
            x = width*0.055; y = height*0.1
            return x,y
        
    def process_images_in_folder(self, folder_path, text):
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            self.add_text(image_path, text)


# Пример использования
font_path = "arialmt.ttf"
folder_path = "output/"

adder = ImageTextAdder(font_path)
adder.process_images_in_folder(folder_path, "AHAHAHAKATON")
# image_paths = ["1748_2480.png", "3507_4960.png", "700_1080.png", "1084_585.png", "1200_520.png", "1200_593.png", "1920_1080.png"]

# adder = ImageTextAdder(font_path)
# # for image_path in image_paths:
# adder.add_text(image_paths[0], "AHAHAHAKATON")
# adder.add_text(image_paths[1], "AHAHAHAKATON")
# adder.add_text(image_paths[2], "AHAHAHAKATON")
# adder.add_text(image_paths[3], "AHAHAHAKATON")
# adder.add_text(image_paths[4], "AHAHAHAKATON")
# adder.add_text(image_paths[5], "AHAHAHAKATON")
# adder.add_text(image_paths[6], "AHAHAHAKATON")


#цвет должен выбираться в зависимости от переданного параметра

# у Ильи должна быть функция которая будет передовать значения загловока подзаголовка и кнопки
# а я будет и считывать в переменные: Text1, Text2, Text3 = get_text()