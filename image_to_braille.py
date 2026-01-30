from PIL import Image
import numpy as np

# Define the Braille Unicode characters
BRAILLE_CHARACTERS = ["⠿", "⠿", "⠿", "⠿", "⠿", "⠿", "⠿", "⠿"]

def image_to_braille(image_path):
    # Open the image and convert it to grayscale
    img = Image.open(image_path).convert('L')
    # Resize the image to a suitable size for Braille representation
    img = img.resize((img.width // 8, img.height // 8))
    # Convert the image to a numpy array
    img_array = np.array(img)
    braille_output = ""

    for row in img_array:
        for pixel in row:
            # Determine the Braille character based on pixel intensity
            if pixel < 128:
                braille_output += BRAILLE_CHARACTERS[0]  # Filled dot
            else:
                braille_output += BRAILLE_CHARACTERS[1]  # Empty dot
        braille_output += '\n'  # New line for each row

    return braille_output

if __name__ == '__main__':
    image_path = input('Enter the path to the image: ')
    braille_representation = image_to_braille(image_path)
    print(braille_representation)