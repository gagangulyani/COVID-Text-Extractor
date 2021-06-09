from src.image_to_text import to_text as ocr
from src.pdf_to_text import to_text as ocr_pdf
from src.text_functions import get_info as get_info_from_text
from magic import from_file, from_buffer
from mimetypes import guess_extension
from pathlib import Path
from time import sleep
from urllib.request import urlopen
from urllib.parse import urlparse


class Extractor:

    temp_dir_path = Path(__file__).parent / "temp_files"

    def __init__(self, path_to_file, file_type=None):
        self.path_to_file, self.file_type = Extractor.validate_file(
            path_to_file, file_type)
        self.file_type = self.file_type.lower() if not file_type else file_type.lower()
        self.ocr_result = {}

    def get_info(self):
        if "image" in self.file_type:
            self.ocr_result = ocr(self.path_to_file)
        elif "pdf" in self.file_type:
            self.ocr_result = ocr_pdf(self.path_to_file)
        elif "text" in self.file_type:
            with open(self.path_to_file) as f:
                self.ocr_result = get_info_from_text(f.read())
        else:
            raise ValueError("Invalid File Type! Can't perform OCR on it")
        return self.ocr_result

    @staticmethod
    def find_downloaded(filename):
        if not Extractor.temp_dir_path.exists():
            Extractor.temp_dir_path.mkdir()

        result = [i for i in Extractor.temp_dir_path.iterdir()
                  if filename in str(i)]
        return str(result[0]) if len(result) == 1 else ""

    @staticmethod
    def get_image_from_url(url):
        path = urlparse(url).path

        filename_without_ext = Path(path).stem

        if (new_filename := Extractor.find_downloaded(filename_without_ext)):
            print("File Already downloaded!")
            return new_filename, from_file(new_filename, mime=True)

        page = urlopen(url)
        content_type = page.headers.get_content_type()
        extension = guess_extension(content_type)
        new_filename = (Extractor.temp_dir_path /
                        f"{Path(path).stem}{extension}")

        if not Path(new_filename).exists():
            with open(new_filename, "wb") as f:
                for _ in range(3):
                    try:
                        f.write(page.read())
                        print("New File Created!")
                    except Exception as e:
                        print(e)
                        sleep(3)
                    else:
                        break

        return str(new_filename.absolute()), content_type

    @staticmethod
    def create_text_file(content):
        temp_dir_path = Path(f"{__file__}").parent / "temp_files"
        new_filename = temp_dir_path / f"{content[::-3][:10]}.txt"
        with open(new_filename, "w") as f:
            f.write(content)
        return str(new_filename.absolute())

    @staticmethod
    def validate_file(path_to_file, file_type=None):
        if path_to_file.startswith("http"):
            return Extractor.get_image_from_url(path_to_file)
        elif (file := Path(path_to_file)).exists():
            return str(file.absolute()), from_file(str(file.absolute()), mime=True)
        elif "text" in file_type:
            return Extractor.create_text_file(path_to_file), file_type
        raise ValueError("Invalid File Path Provided!")


if __name__ == '__main__':
    urls = [
        ("https://pbs.twimg.com/media/E1aZrN-UYAEK8Le?format=jpg&name=medium",),
        ("763-656-6458", "text"),
    ]
    for url in urls:
        temp_object = Extractor(*url)
        print(temp_object.path_to_file, temp_object.file_type)
        print(temp_object.get_info())
