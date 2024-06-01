from PIL import Image, ImageDraw, ImageFont

class ImageTextAdder:
    def __init__(self, font_path):
        self.font_path = font_path
    
    def add_text_with_wrap(self, image, text, output_path, max_width, max_height):
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        # Выбираем размер шрифта в зависимости от разрешения
        font_size = min(width, height) // 20
        font = ImageFont.truetype(self.font_path, font_size)
        
        # Ограничиваем текст по ширине
        wrapped_text = self.wrap_text(draw, text, font, max_width)

        # Определяем позицию для текста
        position = self.get_text_position(width, height, max_width, max_height)

        # Цвет текста в формате RGB
        color = (235, 64, 52)

        # Добавляем текст на изображение
        draw.multiline_text(position, wrapped_text, font=font, fill=color, spacing=10)

        # Сохраняем измененное изображение
        image.save(output_path)
        print(f"Saved image with text at: {output_path}")

    def wrap_text(self, draw, text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textsize(line + words[0], font=font)[0] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line.strip())
        return '\n'.join(lines)

    def get_text_position(self, width, height, max_width, max_height):
        # Пример логики определения позиции текста с учетом максимальной ширины и высоты
        return (width // 10, height // 10)

# Пример использования
font_path = "Comfortaa-VariableFont_wght.ttf"
image_path = "banner.png"
output_path = "output_banner_with_wrap.png"
max_width = 300
max_height = 400

image = Image.open(image_path)

adder = ImageTextAdder(font_path)
adder.add_text_with_wrap(image, "This is a long text that should be wrapped to fit within the specified width.", output_path, max_width, max_height)
