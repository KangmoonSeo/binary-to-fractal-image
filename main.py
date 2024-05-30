from PIL import Image


def create_fractal_image(
    input_data: bytes | int | str, filename: str, width: int = 800, height: int = 800
):
    if isinstance(input_data, bytes):  # bytes
        bits = "".join(format(byte, "08b") for byte in input_data)

    elif isinstance(input_data, int):  # bit
        bits = bin(input_data)

    elif isinstance(input_data, str):  # bit-string
        bits = input_data

    else:

        raise TypeError("input_data must be in [ bytes, int, bit-string str ]")

    # set RGB color
    r = int(bits[:8], 2) % 256
    g = int(bits[8:16], 2) % 256
    b = int(bits[16:24], 2) % 256

    # set fractal parameters
    max_iterations = int(bits[24:32], 2) % 100 + 50
    bailout = int(bits[32:40], 2) / 256.0 + 2.0
    power = int(bits[40:48], 2) / 16.0 + 1.0

    # set image size
    image = Image.new("RGB", (width, height))

    # generate fractal art
    for x in range(width):
        for y in range(height):
            cx = (x - width / 2) / (width / 4.0)
            cy = (y - height / 2) / (height / 4.0)

            c = complex(cx, cy)
            z = 0j

            for i in range(max_iterations):
                z = z**power + c
                if abs(z) > bailout:
                    break

            color = (r * i % 256, g * i % 256, b * i % 256)
            image.putpixel((x, y), color)

    # save image
    image.save(filename)

    print(f"image created: {filename}")


import random

if __name__ == "__main__":
    input_data = random.getrandbits(48)
    filename = "image.png"

    create_fractal_image(
        input_data=input_data,
        filename=filename,
    )
