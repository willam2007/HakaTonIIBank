import pandas as pd
import os
import torch
import clip
from PIL import Image
import torchvision.transforms as transforms
import csv
from translate import Translator

# Шаг 1: Подготовка данных
banners_df = pd.read_excel('banners.xlsx', usecols='B', skiprows=1)
data_pairs = []
images_path = 'image'

for index, row in banners_df.iterrows():
    text_data = row.iloc[0]  # Получаем данные из колонки B
    image_filename = f"image_{index}.png"  # Имена файлов формата image_0.png, image_1.png и т.д.
    image_path = os.path.join(images_path, image_filename)
    if os.path.exists(image_path):
        data_pairs.append((text_data, image_path))
    else:
        print(f"Файл {image_path} не найден и будет пропущен")

# Шаг 2: Обучение модели CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

texts = [pair[0] for pair in data_pairs]
images = [preprocess(Image.open(pair[1]).convert("RGB")).unsqueeze(0).to(device) for pair in data_pairs]
text_tokens = [clip.tokenize(text).to(device) for text in texts]
with torch.no_grad():
    image_features = torch.cat([model.encode_image(image) for image in images])
    text_features = torch.cat([model.encode_text(text_token) for text_token in text_tokens])
torch.save(image_features, 'image_features.pt')
torch.save(text_features, 'text_features.pt')

# Шаг 3: Подбор изображения на основе текста
image_features = torch.load('image_features.pt')
text_features = torch.load('text_features.pt')

def find_best_image(text_query):
    text_token = clip.tokenize([text_query]).to(device)
    with torch.no_grad():
        text_feature = model.encode_text(text_token)
    similarity = (100.0 * text_feature @ image_features.T).softmax(dim=-1)
    best_match_idx = similarity.argmax().item()
    best_image_path = data_pairs[best_match_idx][1]
    return best_image_path

# Шаг 4: Вставка изображения в нужную область
def insert_image(base_image_path, insert_image_path, position):
    base_image = Image.open(base_image_path).convert("RGBA")
    insert_image = Image.open(insert_image_path).convert("RGBA")

    # Изменение размера вставляемого изображения
    insert_image = insert_image.resize((base_image.width // 2, base_image.height // 2))

    # Вставка изображения с учетом альфа-канала
    base_image.paste(insert_image, position, insert_image)
    return base_image

# Функция для сохранения пользовательских предпочтений
def save_user_feedback(text_query, chosen_image_path):
    feedback_file = 'user_feedback.csv'
    feedback_data = [text_query, chosen_image_path]

    # Проверка, существует ли файл и содержит ли он данные
    file_exists = os.path.isfile(feedback_file)
    with open(feedback_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['text_query', 'chosen_image_path'])  # Запись заголовков
        writer.writerow(feedback_data)

# Функция переподготовки модели на основе обратной связи
def retrain_model_with_feedback():
    feedback_file = 'user_feedback.csv'
    if not os.path.exists(feedback_file):
        print("Нет данных обратной связи для переподготовки модели.")
        return
    
    try:
        feedback_df = pd.read_csv(feedback_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            feedback_df = pd.read_csv(feedback_file, encoding='latin1')
        except UnicodeDecodeError:
            feedback_df = pd.read_csv(feedback_file, encoding='cp1252')
    
    feedback_pairs = []
    for index, row in feedback_df.iterrows():
        text_data = row['text_query']
        image_path = row['chosen_image_path']
        if os.path.exists(image_path):
            feedback_pairs.append((text_data, image_path))
        else:
            print(f"Файл {image_path} не найден и будет пропущен")
    
    if feedback_pairs:
        texts = [pair[0] for pair in feedback_pairs]
        images = [preprocess(Image.open(pair[1]).convert("RGB")).unsqueeze(0).to(device) for pair in feedback_pairs]
        text_tokens = [clip.tokenize(text).to(device) for text in texts]
        with torch.no_grad():
            image_features_feedback = torch.cat([model.encode_image(image) for image in images])
            text_features_feedback = torch.cat([model.encode_text(text_token) for text_token in text_tokens])
        
        # Объединение с текущими фичами
        global image_features, text_features
        image_features = torch.cat([image_features, image_features_feedback])
        text_features = torch.cat([text_features, text_features_feedback])
        
        torch.save(image_features, 'image_features.pt')
        torch.save(text_features, 'text_features.pt')
        print("Модель успешно переподготовлена с учетом пользовательской обратной связи.")

def translate_to_english(text):
    translator = Translator(to_lang="en", from_lang="ru")
    translated_text = translator.translate(text)
    return translated_text

from PIL import Image

def get_insert_position(base_width, base_height, insert_width, insert_height):
    """
    Определяет позицию вставки изображения в зависимости от размеров базового изображения.

    :param base_width: Ширина базового изображения.
    :param base_height: Высота базового изображения.
    :param insert_width: Ширина вставляемого изображения.
    :param insert_height: Высота вставляемого изображения.
    :return: Координаты (x, y) для вставки изображения.
    """
    
    top_margin_700_1080 = 150  # Отступ от верхнего края для изображений, которые должны быть размещены в верхней середине
    top_margin_1748_2480 = 300
    top_margin_3507_4960 = 400
    right_margin_1200_520 = 30
    right_margin_1200_593 = 30
    if (base_width, base_height) == (700, 1080):
        position = ((base_width - insert_width) // 2, top_margin_700_1080)  # Верхняя середина, с отступом
    elif (base_width, base_height) == (1084, 585):
        position = (base_width - insert_width - 10, (base_height - insert_height) // 2)  # Середина правой части
    elif (base_width, base_height) == (1200, 520):
        position = (base_width - insert_width - right_margin_1200_520, (base_height - insert_height) // 2)  # Середина правой части
    elif (base_width, base_height) == (1200, 593):
        position = (base_width - insert_width - right_margin_1200_593, (base_height - insert_height) // 2)  # Середина правой части
    elif (base_width, base_height) == (1748, 2480):
        position = ((base_width - insert_width) // 2, top_margin_1748_2480)  # Верхняя середина, с отступом
    elif (base_width, base_height) == (1920, 1080):
        position = (base_width - insert_width - 10, (base_height - insert_height) // 2)  # Середина правой части
    elif (base_width, base_height) == (3507, 4960):
        position = ((base_width - insert_width) // 2, top_margin_3507_4960)  # Верхняя середина, с отступом
    else:
        position = (base_width - insert_width - 10, base_height - insert_height - 10)  # Нижний правый угол по умолчанию

    return position

def insert_image(base_image_path, selected_image_path, output_image_path):
    """
    Вставляет изображение, выбранное нейросетью, в базовое изображение в зависимости от его размера.

    :param base_image_path: Путь к базовому изображению.
    :param selected_image_path: Путь к изображению, выбранному нейросетью.
    :param output_image_path: Путь для сохранения выходного изображения.
    """
    # Шаг 1: Чтение базового изображения
    base_image = Image.open(base_image_path).convert("RGBA")
    base_width, base_height = base_image.size

    # Шаг 2: Чтение выбранного изображения
    selected_image = Image.open(selected_image_path).convert("RGBA")

    # Шаг 3: Изменение размера выбранного изображения
    # Используем 20% от ширины и высоты базового изображения
    new_selected_width = int(base_width * 0.5)
    new_selected_height = int(base_height * 0.5)
    aspect_ratio = selected_image.width / selected_image.height

    # Сохраняем соотношение сторон
    if new_selected_width / aspect_ratio < new_selected_height:
        new_selected_height = int(new_selected_width / aspect_ratio)
    else:
        new_selected_width = int(new_selected_height * aspect_ratio)

    resized_selected_image = selected_image.resize((new_selected_width, new_selected_height), Image.Resampling.LANCZOS)

    # Шаг 4: Определение позиции вставки в зависимости от размера базового изображения
    position = get_insert_position(base_width, base_height, new_selected_width, new_selected_height)

    # Шаг 5: Вставка выбранного изображения в базовое изображение
    base_image.paste(resized_selected_image, position, resized_selected_image)

    # Шаг 6: Сохранение выходного изображения
    base_image.save(output_image_path, format="PNG")
# Пример использования
if __name__ == '__main__':
    base_image_path = 'image_test_gen/base_image_3507_4960.png'
    selected_image_path = 'image/image_4.png'  # Путь к изображению, выбранному нейросетью
    output_image_path = 'output_image.png'

    insert_image(base_image_path, selected_image_path, output_image_path)
'''# Пример использования
if __name__ == '__main__':
    text_query = "Особый опыт, тренинг по этике общения с людьми с инвалидностью"
    translated_text = translate_to_english(text_query)
    print(translated_text)
    best_image_path = find_best_image(translated_text)
    print("Best image path:", best_image_path)
    
    # Предположим, что пользователь не согласен с выбором модели и выбирает другое изображение
    user_chosen_image_path = 'image/image_1.png'
    save_user_feedback(translated_text, user_chosen_image_path)
    
    # Переподготовка модели
    retrain_model_with_feedback()
'''