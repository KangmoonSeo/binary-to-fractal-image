from typing import Union
from PIL import Image


def create_fractal_image(
    input_data: Union[bytes, int, str], width: int = 800, height: int = 800
):
    """
    Create a fractal image based on input data and save it to a file.

    Parameters
    ----------

    input_data : bytes or int or str
        Data used to generate fractal parameters.
        Can be bytes, an integer, or a bit-string (str).
    width : int
        Width of the image in pixels (default is 800).
    height : int
        Height of the image in pixels (default is 800).


    Returns
    -------
    image : :py:class:`~PIL.Image.Image`
        A fractal image
    """

    if isinstance(input_data, bytes):  # bytes
        input_data = input_data[:48]
        bits = "".join(format(byte, "08b") for byte in input_data)

        if len(bits) < 48:
            raise ValueError("length of bits must be up to 48.")

    elif isinstance(input_data, int):  # bit
        bits = format(input_data, "048b")

    elif isinstance(input_data, str):  # bit-string
        bits = input_data[:48]

        if len(bits) < 48:
            raise ValueError("length of bits must be up to 48.")

    else:
        raise TypeError("input_data must be in [ bytes, int, str(bit-string) ].")

    # set RGB color
    r = int(bits[:8], 2) % 256
    g = int(bits[8:16], 2) % 256
    b = int(bits[16:24], 2) % 256

    # set fractal parameters
    max_iterations = int(bits[24:32], 2) % 100 + 50
    bailout = int(bits[32:40], 2) / 256.0 + 2.0
    power = int(bits[40:48], 2) / 16.0 + 1.0

    # set image size
    fractal_image = Image.new("RGB", (width, height))

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
            fractal_image.putpixel((x, y), color)

    return fractal_image


if __name__ == "__main__":

    import random
    import os

    int_stream_data = random.getrandbits(48)
    byte_stream_data = os.urandom(6)

    image = create_fractal_image(input_data=int_stream_data)

    # save image
    image.save("image.png")

    print("fractal image created")
