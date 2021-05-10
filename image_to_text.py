from pytesseract import pytesseract
from text_functions import get_info
import logging
import concurrent.futures
import cv2

logging.basicConfig(level=logging.CRITICAL)

def starred_adaptive_threshold(args):
    return cv2.adaptiveThreshold(*args)

def to_text(filename, show_image=False):
    logging.debug(f"Processing Image :{filename}")
    img = cv2.imread(filename)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    logging.debug("Converted the Image to Grayscale")

    img = cv2.bilateralFilter(img, 5, 25, 25)

    logging.debug("Adding Bilarteral Filter on the image")

    imgs = []
    results = []

    imgs.append(img)

    logging.debug("Creating Image tuple for preprocessing")

    thresh_img_params = [
         (img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 6),
         (img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 255, 3)
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        logging.debug("Started Preprocessing Images")
        for result in executor.map(starred_adaptive_threshold, thresh_img_params):
            imgs.append(result)
    
    logging.debug("Now Applying OCR on Images")
    # imgs.append(cv2.adaptiveThreshold(thresh_img_params[0]))

    for img in imgs:
        results.append(" ".join(pytesseract.image_to_string(img).splitlines()))

        if show_image:
            cv2.imshow(filename, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    logging.debug("Generating Result...")
    final = {}
    for result in sorted(results, key=lambda x: len(x)):
        final |= get_info(result, final)

    return final


if __name__ == '__main__':
    from sys import argv
    from pathlib import Path
    from random import choice

    filename = "".join(argv[1:]).strip()

    if not filename:
        test_dir = Path('test')
        filename = choice(
            [i for i in test_dir.iterdir() if i.suffix != ".pdf"])
        filename = str(filename)

    print(filename)
    show_image = False

    print(to_text(filename, show_image=show_image))
