from PIL import Image
from functools import reduce

def pixel_generator(image_path):
    with Image.open(image_path) as img:
        # Конвертируем в RGB если нужно
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        pixels = img.load()
        
        for y in range(height):
            for x in range(width):
                yield (x, y, pixels[x, y])

def invert_color(pixel_data):
    """Инвертирует цвет пикселя"""
    x, y, (r, g, b) = pixel_data
    inverted_pixel = (255 - r, 255 - g, 255 - b)
    return (x, y, inverted_pixel)

def apply_pixels_to_image(original_path, output_path, processed_pixels):
    """Применяет обработанные пиксели к новому изображению"""
    with Image.open(original_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        new_img = img.copy()
        pixels = new_img.load()
        
        for x, y, color in processed_pixels:
            pixels[x, y] = color
        
        new_img.save(output_path)
        return new_img

# Основной процесс
def invert_image_colors(input_image, output_image):
    # Создаем генератор пикселей
    pixels = pixel_generator(input_image)
    
    # Используем MAP для инвертирования каждого пикселя
    inverted_pixels = map(invert_color, pixels)
    
    # Применяем обработанные пиксели к изображению
    result = apply_pixels_to_image(input_image, output_image, inverted_pixels)
    return result

# Использование
if __name__ == "__main__":
    input_img = "input.jpg"  # путь к вашему изображению
    output_img = "output_inverted.jpg"
    
    inverted_image = invert_image_colors(input_img, output_img)
    print(f"Изображение инвертировано и сохранено как {output_img}")
