from PIL import Image, ImageDraw, ImageFont
import os

class ImageTextAdder:
    def __init__(self, font_path):
        self.font_path = font_path
    
    def add_text(self, image_path, text):
        # Извлекаем разрешение из имени файла
        filename = os.path.basename(image_path)
        resolution = filename.split('.')[0]
        width, height = map(int, resolution.split('_'))

        # Открываем изображение
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Выбираем размер шрифта в зависимости от разрешения
        font_size = 150
        font = ImageFont.truetype(self.font_path, font_size)

        # Определяем позицию для текста в зависимости от разрешения
        position = self.get_text_position(width, height)

        # Цвет текста в формате RGB
        color = (235, 64, 52)

        # Добавляем текст на изображение
        draw.text(position, text, font=font, fill=color)

        # Сохраняем измененное изображение
        output_path = f"{filename}"
        image.save(output_path)
        print(f"Saved image with text at: {output_path}")

    def get_text_position(self, width, height):
        # Пример логики определения позиции текста
        if width >= 1920 and height >= 1080:
            return (width // 10, height // 10)  # Верхний левый угол
        elif width >= 1280 and height >= 720:
            return (width // 2, height // 2)  # Центр
        else:
            return (width // 4, height // 4)  # Середина верхнего левого квадранта

# Пример использования
font_path = "font.ttf"
image_paths = ["297_420.png"]

adder = ImageTextAdder(font_path)
for image_path in image_paths:
    adder.add_text(image_path, "AHAHAHAKATON")
