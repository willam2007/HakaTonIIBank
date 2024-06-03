
from PIL import Image, ImageDraw, ImageFont
import os
from dkd import *
import textwrap

class ImageTextAdder:
    def __init__(self, font_path):
        self.font_path = font_path
    
    def get_size(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        return width, height, image

    def add_text(self, image_path, Text1, Text2, Text3, text1_color):
        # Получаем размеры изображения
        width, height, image = self.get_size(image_path)
        draw = ImageDraw.Draw(image)


        if (width == 700) and (height == 1080):
            font_size1 = 80
            font_size2 = 50
        else:
            font_size1 = 100
            font_size2 = 50


        font1 = ImageFont.truetype(self.font_path, font_size1)
        font2 = ImageFont.truetype(self.font_path, font_size2)
        print('font sizeeeee ', font1.size)

        # Определяем позицию для первой рамки
        position1 = self.create_global_container_position(width, height)
        rect_width = width * 0.8 if width <= height else width * 0.55
        rect_height = height * 0.4 if width <= height else height * 0.8

        # Добавляем текст на изображение
        # self.add_rectangle(draw, position1, rect_width, rect_height, outline_color="black", fill_color=None)

        # Позиции для текста внутри первой рамки
        text1_position = (position1[0] + 10, position1[1] + 10)
        text2_position = (position1[0] + 10, position1[1] + rect_height / 3)
        text3_position = (position1[0] + 10, position1[1] + 2 * rect_height / 3)

        max_text_width = rect_width - 20
        # написать метод wrap у которого на вход подается строка и максимальная ширина
        # на выходе должно получиться несколько строк 
        text_width = font1.getsize(Text1)
        print('pooooooopa', text_width)


        def draw_text_wrapped(draw, text, position, font, max_width, fill):
            margin, offset = position
            words = text.split()
            line = ''
            stroka = []
            offset_index = font.getsize(text)[1]

            for word in words:
                line_width = font.getsize(line + word)[0]
                if (line_width <= max_width):
                    line = line + word + ' '
                else:
                    # draw.text((margin, offset), line, font=font, fill=fill)
                    stroka.append(line)
                    offset += offset_index
                    line = word + ' '
            if line:
                # draw.text((margin, offset), line, font=font, fill=fill)
                stroka.append(line)

            return stroka
        
        def draw_text(draw, text, position, font, max_width, fill):
            stroka = draw_text_wrapped(draw, text, position, font, max_width, fill)

            while len(stroka) > 2: 
                font = ImageFont.truetype(font.path, int(font.size * 0.8))
                stroka = draw_text_wrapped(draw, text, position, font, max_width, fill)

            margin, offset = position
            for line in stroka:
                draw.text((margin, offset), line, font=font, fill=fill)
                offset += font.getsize(line)[1]



        draw_text(draw, Text1, text1_position, font1, max_text_width, text1_color)
        draw_text(draw, Text2, text2_position, font2, max_text_width, text1_color)
        draw_text(draw, Text3, text3_position, font2, max_text_width, text1_color)


        # Проверяем и создаем папку для вывода
        output_folder = "output"
        output_folder_path = os.path.join(os.getcwd(), output_folder)
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Сохраняем измененное изображение
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
            x = width * 0.1; y = height * 0.55
            return x, y
        elif ((width == 1084) and (height == 585)) or ((width == 1200) and (height == 520)) or ((width == 1200) and (height == 593)) or ((width == 1920) and (height == 1080)):
            x = width * 0.055; y = height * 0.1
            return x, y
        
    def process_images_in_folder(self, folder_path, Text1, Text2, Text3, text1_color):
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            self.add_text(image_path, Text1, Text2, Text3, text1_color)

