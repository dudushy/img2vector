# pip freeze > requirements.txt
#* -- Imports
import os
import tkinter as tk
import tkinter.filedialog as fd
import svgwrite
from PIL import Image

#* -- Variables
path = os.path.dirname(__file__) #? Directory path

#* -- Functions
def clearConsole() -> None: #? Clear console
    os.system("cls" if os.name == "nt" else "clear")

def selectImages() -> tuple:
    image_formats= [
        # ("All", "*.jpeg *.jpg *.png"),
        # ("JPEG", "*.jpeg"),
        # ("JPG", "*.jpg"),
        ("PNG", "*.png")
    ]

    tk.Tk().withdraw()

    images = fd.askopenfilenames(title="Choose a file", filetypes=image_formats)
    print(f"[selectImages] images\n{images}\n")
    return images

def convertImages(images, path):
    count = 1
    for image in images:
        imageName = image.split("/")[-1].split(".")[-2]
        imageExtension = image.split("/")[-1].split(".")[-1]
        print(f"[convertImages#{count}/{len(images)}] {imageName}.{imageExtension}: convert")

        im = Image.open(image, 'r')
        width, height = im.size
        print(f"[convertImages#{count}/{len(images)}] size: {width}x{height}")

        if (width <= 600 and height <= 600):
            pixel_values = list(im.getdata())

            dwg = svgwrite.Drawing(filename=f"{path}/output/{imageName}.svg", size=(width, height), profile='tiny')

            for y in range(height):
                for x in range(width):
                    pixel = pixel_values[x + y * width]

                    if pixel[3] == 0:
                        continue
                    dwg.add(dwg.rect((x, y), (1, 1), fill='rgb(%d,%d,%d)' % pixel[:3]))

            dwg.save()
            print(f"[convertImages#{count}/{len(images)}] {imageName}.{imageExtension}: done!\n")
        else:
            print(f"[convertImages#{count}/{len(images)}] {imageName}.{imageExtension}: is too big, skipping...\n")

        count += 1

def main() -> None:
    files = selectImages()

    convertImages(files, f"{path}/../")

#! Main
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
