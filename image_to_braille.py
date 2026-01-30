from PIL import Image
import numpy as np

# 盲文字符对应的二进制值
# 盲文有8个点，分别对应：
# 1 4
# 2 5
# 3 6
# 7 8

def get_braille_char(value):
    """
    根据0-255的值返回对应的盲文Unicode字符
    """
    return chr(0x2800 + value)

def image_to_braille(image_path, width=100, threshold=128):
    """
    将图片转换为盲文点阵
    
    参数:
    - image_path: 图片路径
    - width: 输出的盲文字符宽度（默认100）
    - threshold: 像素灰度阈值（默认128，用于8点盲文模式）
    """
    # 打开并转换为灰度图
    img = Image.open(image_path).convert('L')
    
    # 计算宽高比并调整大小
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)  # 0.5是因为字符的高宽比
    img = img.resize((width, height))
    
    # 转换为numpy数组
    img_array = np.array(img)
    braille_output = ""
    
    # 每次处理4个像素块，生成一个盲文字符
    for y in range(0, img_array.shape[0] - 1, 2):
        for x in range(0, img_array.shape[1] - 1, 2):
            # 获取4个像素
            pixel_tl = img_array[y, x]           # 左上
            pixel_bl = img_array[y + 1, x]       # 左下
            pixel_tr = img_array[y, x + 1]       # 右上
            pixel_br = img_array[y + 1, x + 1]   # 右下
            
            # 根据亮度计算盲文值（8个点对应8个位）
            braille_value = 0
            if pixel_tl < threshold:
                braille_value |= (1 << 0)  # 点1
            if pixel_bl < threshold:
                braille_value |= (1 << 1)  # 点2
            if pixel_bl < threshold:
                braille_value |= (1 << 2)  # 点3
            if pixel_tr < threshold:
                braille_value |= (1 << 3)  # 点4
            if pixel_tr < threshold:
                braille_value |= (1 << 4)  # 点5
            if pixel_br < threshold:
                braille_value |= (1 << 5)  # 点6
            if pixel_bl < threshold:
                braille_value |= (1 << 6)  # 点7
            if pixel_br < threshold:
                braille_value |= (1 << 7)  # 点8
            
            braille_output += get_braille_char(braille_value)
        
        braille_output += '\n'
    
    return braille_output

def save_braille(braille_text, output_path):
    """保存盲文输出到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(braille_text)
    print(f"已保存到: {output_path}")

if __name__ == '__main__':
    image_path = input('请输入图片路径: ')
    try:
        width = int(input('请输入盲文宽度 (默认100): ') or '100')
    except ValueError:
        width = 100
    
    try:
        threshold = int(input('请输入灰度阈值 (默认128): ') or '128')
    except ValueError:
        threshold = 128
    
    braille_representation = image_to_braille(image_path, width, threshold)
    print("\n=== 盲文点阵 ===\n")
    print(braille_representation)
    
    # 选择是否保存
    save_choice = input('\n是否保存到文件? (y/n): ').lower()
    if save_choice == 'y':
        output_path = input('请输入输出文件路径: ')
        save_braille(braille_representation, output_path)
