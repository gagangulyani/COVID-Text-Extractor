from pytesseract import pytesseract
import cv2
import re 


def get_info(text):
    pattern = (
        r"(oxygen)|((cylinders?)|(refill?s?)|(plasma)|"
        r"(cans?)|(concentrators?))|(available)|"
        r"(\+91-?)?(\d{3}\.?\d{3}\.?\d{4})|(verfied])|"
        r"(required)|(verfied)|(help)|(urgent)|(food)|"
        r"(\(?[0]?\d{2,3}\)?.?\d{3,8}\-?/?\d{0,8})"
        )

    return [i.group() for i in re.finditer(pattern, text, re.IGNORECASE) if i.group()]


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

    imgs.extend([cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 50),
                 cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 171, 8)])

    for img in imgs:

        results.append(pytesseract.image_to_string(img))

        if show_image:
            cv2.imshow(filename, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return max([get_info(result) for result in results])
    

if __name__ == '__main__':
    from sys import argv
    
    filename = "".join(argv[1:])
    
    resized = False
    show_image = False

    print(to_text(filename, resized=resized, show_image=show_image))
