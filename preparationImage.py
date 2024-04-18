from PIL import Image
from RLE_bytes import printFile

WIDTH: int = 10
HEIGHT: int = 10


def imagePreparation(file_path: str, image_type: str) -> str:
    im = Image.open(file_path)
    im = im.resize((WIDTH, HEIGHT))
    # im.save(file_path)
    return covertImageToRowFormat(im, file_path, image_type)


def covertImageToRowFormat(image: Image, file_path: str, image_type: str) -> str:
    pixels = image.load()

    new_file_name: str = file_path.split(".")[0] + "_rawformat.txt"
    file = open(new_file_name, "wb")

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = pixels[x, y]
            if image_type == "BLACK_WHITE":
                if pixel != (255, 255, 255):
                    pixel = (0, 0, 0)
            file.write(bytearray([pixel[0]]))
            file.write(bytearray([pixel[1]]))
            file.write(bytearray([pixel[2]]))
        file.write(b'\n')
    file.close()

    return new_file_name


if __name__ == '__main__':
    imagePreparation("images/grey.jpg", "COLOR")
    # printFile("images/black_white_rawformat.txt")
