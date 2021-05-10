from pathlib import Path
from image_to_text import to_text
from pdf_to_text import to_text as text_from_pdf
from pprint import pprint


TEST_DIR = Path("test")

SHOW_IMAGES = False

for filename in Path(TEST_DIR).iterdir():
    if filename.suffix == ".pdf":
        # print(text_from_pdf(str(filename.absolute())))
        continue
    pprint(to_text(str(filename.absolute()), show_image=SHOW_IMAGES))