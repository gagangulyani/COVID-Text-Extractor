from json import loads, load, dumps
from pathlib import Path
try:
    from config import REGEX_FILE_PATH
except:
    from .config import REGEX_FILE_PATH
import re
from urllib.request import Request, urlopen


def find_number_in_scam_dir(number):
    if type(number) != str:
        return []
    number = to_number(number)
    url = "https://api.cov.social/v1/info/findFraud"
    data = {"search": number.removeprefix("0")}
    data = dumps(data).encode('utf-8')
    headers = {"Content-Type": "application/json"}
    try:
        req = Request(url=url, data=data, headers=headers)
        resp = urlopen(req)
        return loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] {e}")
        return []


def remove_duplicates(text):
    return list(dict.fromkeys([clean_text(i.lower()).strip() for i in text if i.strip()]))


def clean_text(text, replacement_string=None):
    replacements = {
        "  ": " ",
        "\n": " ",
        "(": " ",
        ")": " ",
    } if replacement_string is None else replacement_string

    for replacement in replacements:
        text = text.replace(replacement, replacements[replacement])

    return text


def to_number(text):
    replacements = {
        " ": "",
        "-": "",
        "+": "",
        "\n": " ",
        "\t": "",
        "/": "",
        "\\": ""
    }
    return "".join(clean_text(text, replacements).split())


def is_number(text):
    temp = to_number(text)
    if temp.isdigit() and (len(temp) in [*range(10, 15)]):
        return True
    return False


def get_info(text, existing_dict=None, filename=REGEX_FILE_PATH, verify_number=False):

    with open(filename) as f:
        json_obj = load(f)

    result_dict = existing_dict if existing_dict else {}

    for key in json_obj:
        if (result := [clean_text(found.group().strip()) for found in re.finditer(json_obj[key], text, re.IGNORECASE)]):
            if len(result) >= 1:
                result_dict[key] = result_dict.get(
                    key, []) + remove_duplicates(result)
            else:
                result_dict[key] = result_dict.get(key, []) + result

            # Extract Phone Numbers
            result_dict[key] = [i for i in result_dict[key] if is_number(
                i) and i in text] if key == "Phone-Numbers" else result_dict[key]
            result_dict[key] = remove_duplicates(result_dict[key]) if type(
                result_dict[key]) == list else result_dict[key]

            if existing_dict:
                result_dict.update({
                    key: remove_duplicates(
                        existing_dict[key] + result_dict[key])
                })

    if verify_number:
        result_dict["Scammer-Dir-Result"] = {}
        for pno in result_dict.get("Phone-Numbers", []):
            result_dict["Scammer-Dir-Result"].update(
                {
                    f"{pno}": find_number_in_scam_dir(pno)
                }
            )

    return result_dict


if __name__ == "__main__":
    from pprint import pprint
    VERIFY_NUM = True
    pprint(get_info(
        """hello oxygen plasma (A+, A-,o-, AB+) and cylinder concentrator required
               age 22, 0132-2205379/78, +91-9763484463, 8272989242 asap verified needed hs@test.in ju2@hulu.com""", verify_number=VERIFY_NUM)
    )
