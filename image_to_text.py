from pytesseract import pytesseract
from json import load
import cv2
from text_functions import get_info


def resize_frame(frame, scale=0.85):
    dimensions = tuple(int(i*scale) for i in frame.shape[::-1])
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def to_text(filename, resized=False, show_image=False):

    img = cv2.imread(filename)
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgs = []
    results = []

    if resized:
        img = resize_frame(img)
        
    imgs.append(img)

    imgs.extend([cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8),
                cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 255, 8),
                cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 171, 8)])

    for img in imgs:

        results.append("".join(pytesseract.image_to_string(img).splitlines()))

        if show_image:
            cv2.imshow(filename, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    final = {}
    for result in sorted(results, key=lambda x: len(x)):
        final |= get_info(result)

    return final
    

if __name__ == '__main__':
    from sys import argv
    from pathlib import Path
    from random import choice

    filename = "".join(argv[1:]).strip()
    
    if not filename:
        test_dir = Path('test')
        filename =  choice([i for i in test_dir.iterdir()])
        filename = str(filename)
    
    print(filename)
    
    resized = False
    show_image = True

    print(to_text(filename, resized=resized, show_image=show_image))
