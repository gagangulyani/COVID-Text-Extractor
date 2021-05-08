from text_functions import get_info
from pdfminer import high_level

def to_text(filename):
    return get_info(" ".join(high_level.extract_text(filename).strip().splitlines()))

if __name__ == '__main__':
    path = "test/Remdesivir-Distributor-List.pdf"
    print(to_text(path))
