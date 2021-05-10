from pytesseract import pytesseract
from text_functions import get_info
import logging
import concurrent.futures
import cv2

logging.basicConfig(level=logging.CRITICAL)


def starred_adaptive_threshold(args):
    return cv2.adaptiveThreshold(*args)


def ocr(img):
    return pytesseract.image_to_string(img)


def to_text(filename, show_image=False):
    logging.debug(f"Processing Image :{filename}")

    results = {}

    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    logging.debug("Converted the Image to Grayscale")

    logging.debug("Adding Bilarteral Filter on the image")
    img = cv2.bilateralFilter(img, 5, 25, 25)

    if show_image:
        cv2.imshow("Bilateral Filter", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    logging.debug("Applying OCR on first image")
    results |= get_info(" ".join(ocr(img).splitlines()), results)

    

    logging.debug("Creating Addional Images for Pre-Processing..")

    thresh_img_params = [
        (img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4),
        (img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 255, 1)
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        logging.debug("Started Preprocessing and OCR on Additional Images")
        for result in executor.map(starred_adaptive_threshold, thresh_img_params):
            results |= get_info(" ".join(ocr(result).splitlines()), results)
            if show_image:
                cv2.imshow("Threshold Image", result)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    return results


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
