import os
import random
from PIL import Image


def generate_jpg(width, height, target_size, output_file):
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    img = Image.new("RGB", (width, height), color)
    # img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=1)
    # img.save(output_file, "PNG", quality=1, optimize=True, compress_level=9, bits=1)
    img.save(output_file, "JPEG", quality=1, optimize=True, subsempling=2)  # progressive=True
    final_size = os.path.getsize(output_file)
    if final_size < target_size:
        with open(output_file, "ab") as f:
            f.write(b"\0" * (target_size - final_size))
        final_size = os.path.getsize(output_file)

    print(f"File size: {final_size} bytes")

# Example usage: 1024x1024, ~2MB
generate_jpg(16, 16, 4, "output.jpg")
