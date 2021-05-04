from pathlib import Path
from image_to_text import to_text


TEST_DIR = Path("test")

for filename in Path(TEST_DIR).iterdir():
    print(to_text(str(filename.absolute())))