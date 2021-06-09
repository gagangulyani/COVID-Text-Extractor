from pytesseract import pytesseract
try:
    from .text_functions import get_info
    from .config import LOGGING_LEVEL, SHOW_IMAGE
except:
    from text_functions import get_info
    from config import LOGGING_LEVEL, SHOW_IMAGE
from pathlib import Path
import logging
import cv2
import numpy as np


logging.basicConfig(level=getattr(logging, LOGGING_LEVEL))


def resize_image(img, scale=0.65):
    width, height = img.shape

    if width > 4960 or height > 4960:
        scale = 0.25
        dsize = (height * scale, width * scale)
        dsize = [int(i) for i in dsize]
        return cv2.resize(img, dsize)

    elif width > 2480 or height > 2480:
        scale = 0.5
        dsize = (height * scale, width * scale)
        dsize = [int(i) for i in dsize]
        return cv2.resize(img, dsize)

    elif width > 1240 or height > 1240:
        dsize = (height * scale, width * scale)
        dsize = [int(i) for i in dsize]
        return cv2.resize(img, dsize)

    return img


def starred_adaptive_threshold(args):
    return cv2.adaptiveThreshold(*args)


def fallback(img, results, show_image):
    thresh_img_params = [
        (img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 201, 17),
    ]
    logging.info("Started Preprocessing and OCR on Additional Filtered Images")
    for i, result in enumerate(map(starred_adaptive_threshold, thresh_img_params)):
        text = ocr(result)
        results = get_info(text, results)
        if show_image:
            cv2.imshow(f"Threshold Image {i+1}", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return results


def ocr(img):
    """This function takes in image file (numpy.ndarray) and applies and returns OCR using pytesseract

    Args:
        img (numpy.ndarray): Image file

    Returns:
        str: Text returned by pytesseract-ocr
    """
    result = pytesseract.image_to_string(img)
    # print(result)
    return result


def to_text(filename, show_image=False):
    """This function takes in filename of the image and optional parameter `show_image` for
    displaying the processed images and applies OCR on them and returns the combined result in the form
    of a dictionary.

    Args:
        filename (string): path of image file
        show_image (bool, optional): Display Processed Images which will be OCR'ed. Defaults to False.

    Returns:
        dict: OCR'ed Result in the form of a dictionary
    """
    if not Path(filename).exists():
        logging.error(f"ERROR! {filename} does not exist!")
        exit(1)

    logging.info(f"Processing Image: {filename}")

    # for storing the result
    results = {}

    # read the image file and convert it to grayscale
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    logging.debug("Converted the Image to Grayscale")

    # sharpen it a bit
    # logging.debug("Adding Bilarteral Filter on the image")
    img = cv2.bilateralFilter(img, 3, 90, 90)
    img = resize_image(img)
    copy = img.copy()
    clahe = cv2.createCLAHE(clipLimit=2)
    value = 10
    img = clahe.apply(img)
    img = np.where((255 - img) < value, 255, img-value)

    # display the processed image if show_image is True
    if show_image:
        cv2.imshow("Processed Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    logging.debug("Applying OCR on Processed image")

    results = get_info(ocr(img))

    if not results.get("Phone-Numbers"):
        logging.warning(
            "Phone-Numbers not detected with originally filtered Image")
        logging.warning("Creating more filtered images for OCR")
        results |= fallback(copy, results, show_image)

    logging.info(f"OCR Matched {len(results)!a} attributes from {filename}")
    logging.info(f"Results :{results}")
    return results


if __name__ == '__main__':
    from sys import argv
    from random import choice

    if len(argv) > 1:
        filenames = argv[1:]
        for filename in filenames:
            logging.info(to_text(filename, show_image=SHOW_IMAGE))
    else:
        logging.error(
            "Invalid Number of Arguments! Please Specify Image Path!")
        exit(1)
