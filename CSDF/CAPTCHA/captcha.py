from captcha.image import ImageCaptcha
import random, string
from PIL import Image

# Generate random CAPTCHA text
captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

# Generate CAPTCHA image and save it
ImageCaptcha().write(captcha_text, 'captcha.png')

# Show the CAPTCHA image
Image.open('captcha.png').show()

# Get user input and verify
user_input = input("Enter the CAPTCHA: ")
print("CAPTCHA verification", "successful!" if user_input == captcha_text else "failed. Try again.")