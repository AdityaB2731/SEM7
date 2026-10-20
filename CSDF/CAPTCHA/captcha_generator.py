from pathlib import Path
import random
import string

from PIL import Image, ImageDraw, ImageFont


CAPTCHA_FILE = Path(__file__).resolve().parent / "captcha.png"
CAPTCHA_LENGTH = 8
IMAGE_SIZE = (420, 140)


def _font():
    try:
        import captcha

        font_path = Path(captcha.__file__).parent / "data" / "DroidSansMono.ttf"
        return ImageFont.truetype(str(font_path), 58)
    except (ImportError, OSError):
        return ImageFont.load_default()


def generate_captcha():
    text = "".join(random.choices(string.digits, k=CAPTCHA_LENGTH))
    image = Image.new("RGB", IMAGE_SIZE, (20, 20, 35))
    draw = ImageDraw.Draw(image)
    font = _font()

    for index, character in enumerate(text):
        layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        layer_draw.text((18, 12), character, font=font, fill=(235, 235, 245, 255))
        layer = layer.rotate(random.randint(-25, 25), resample=Image.Resampling.BICUBIC, expand=1)
        image.paste(layer, (index * 45 - 4, random.randint(8, 28)), layer)

    draw = ImageDraw.Draw(image)
    for _ in range(8):
        draw.line(
            (random.randint(0, 419), random.randint(0, 139),
             random.randint(0, 419), random.randint(0, 139)),
            fill=(100, 150, 190),
            width=2,
        )
    image.save(CAPTCHA_FILE)
    return text


def verify_captcha(captcha_text):
    print(f"CAPTCHA image generated at:\n{CAPTCHA_FILE}")
    print("It contains 8 overlapping, slanted digits on a dark background.")
    print("Open the image manually if it does not open automatically.")

    for attempt in range(1, 4):
        answer = input(f"Enter the CAPTCHA (attempt {attempt}/3): ").strip()
        if answer == captcha_text:
            print("CAPTCHA verification successful!")
            return True
        print("Incorrect CAPTCHA.")

    print("CAPTCHA verification failed.")
    return False


if __name__ == "__main__":
    verify_captcha(generate_captcha())
