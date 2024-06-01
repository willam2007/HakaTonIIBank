import pandas as pd
import os
import torch
import clip
from PIL import Image
import torchvision.transforms as transforms
import csv

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
    
    feedback_df = pd.read_csv(feedback_file)
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
        image_features_combined = torch.cat([image_features, image_features_feedback])
        text_features_combined = torch.cat([text_features, text_features_feedback])
        
        torch.save(image_features_combined, 'image_features.pt')
        torch.save(text_features_combined, 'text_features.pt')
        print("Модель успешно переподготовлена с учетом пользовательской обратной связи.")

# Пример использования
if __name__ == '__main__':
    text_query = "Your short text description"
    best_image_path = find_best_image(text_query)
    print("Best image path:", best_image_path)
    
    # Предположим, что пользователь не согласен с выбором модели и выбирает другое изображение
    user_chosen_image_path = 'images/image_2.png'
    save_user_feedback(text_query, user_chosen_image_path)
    
    # Пример вставки изображения
    base_image_path = 'path/to/your/base_image.png'
    position = (50, 50)  # Позиция вставки
    final_image = insert_image(base_image_path, best_image_path, position)
    final_image.show()
    final_image.save('output_image.png')

    # Переподготовка модели
    retrain_model_with_feedback()