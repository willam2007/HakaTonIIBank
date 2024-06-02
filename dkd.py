from PIL import Image, ImageDraw
import os

#НЕ ТРОГАТЬ
''' 
# Параметры изображения
formats = {
    1: "png",
    2: "jpg",
    3: "pdf",
    4: "pptx"
}
'''


def choosecolor(colornum):
        if colornum == 1:
            return (1,127,181)
        elif colornum == 2:
            return (228,29,50)
        elif colornum == 3:
            return (247,167,8)
        elif colornum == 4:
            return (91,91,91)
        elif colornum == 5:
            return (1,181,230)
        elif colornum == 6:
            return (235,98,92)
        elif colornum == 7:
            return (253,216,136)
        elif colornum == 8:
            return (125,125,125)
        

def choose(i):
            
            if i == 0:
                width_px = 3507
                height_px = 4960
                dpi = 300
            elif i == 1:
                width_px = 1748
                height_px = 2480
                dpi = 300
            elif i == 2:
                width_px = 1920
                height_px = 1080
                dpi = 300
            elif i == 3:
                width_px = 1200
                height_px = 593
                dpi = 72
            elif i == 4:
                width_px = 1200
                height_px = 520
                dpi = 72
            elif i == 5:
                width_px = 700
                height_px = 1080
                dpi = 300
            elif i == 6:
                width_px = 1084
                height_px = 585
                dpi = 300
    
            return width_px, height_px, dpi

def create_image(filename: str, width_px: int, height_px: int, dpi: int, color: tuple) -> None:
    print(format)
    # Создание изображения
    image = Image.new("RGB", (width_px, height_px), color)
    draw = ImageDraw.Draw(image)
    
    # Нарисуем прямоугольник
    draw.rectangle([(0, 0), (width_px - 1, height_px - 1)], outline="black")

    # Сохранение изображения с заданным DPI
    image.save(filename, dpi=(dpi, dpi))




def creation(image_name,array,colornum):
    for i in range(len(array)):
        first,second=int(array[i][0]),int(array[i][1])
    # Выбор параметров
        if first==1:


            '''format = formats[second] - НЕ ТРОГАТЬ'''

        
            color=choosecolor(colornum)
            width_px, height_px, dpi = choose(i)

            if width_px and height_px and dpi:
                # Получение текущего пути и создание полного пути к файлу
                # Название папки, куда будет сохраняться файл
                output_folder = "output"

                # Путь к этой папке
                output_folder_path = os.path.join(os.getcwd(), output_folder)

                # Убедимся, что папка существует
                if not os.path.exists(output_folder_path):
                    os.makedirs(output_folder_path)

                # Путь к файлу внутри папки output
                output_path = os.path.join(output_folder_path, f"{image_name}_{width_px}_{height_px}.png")

                # Пример использования функции:
                create_image(output_path, width_px, height_px, dpi, color)
                #getsie(width_px,height_px,format)
                print(f"Image saved to {output_path}")

