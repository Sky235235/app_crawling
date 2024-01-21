from PIL import Image
import pytesseract
import cv2
import re

tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

## 이미지 전처리

def run(img_path):

    image = cv2.imread(img_path)
    x = 150
    y = 1267
    width = 848
    height = 331

    cropped_image = image[y:y+height, x:x+width]
    cv2.imwrite('screenshot/cropped_image.png', cropped_image)
    options = "--psm 4"
    extracted_text = pytesseract.image_to_string(cropped_image, lang='kor+eng', config=options)
    text_list = extracted_text.split('\n')
    edited_text_list = [v for v in text_list if v != '']
    print('crawling_result', edited_text_list)

    call_type_lst = []
    fare_lst = []
    for _text in edited_text_list:

        _new_text = _text.replace(' ', '')
        _num = re.sub(r'[^0-9]', '', _new_text)
        _index = _new_text.index(_num[:1])
        _cat_str = _new_text[:_index]
        # ---- _fare_str 전처리
        if len(_num) > 1:
            _fare = int(_num) * 1000

        elif len(_num) == 0:
            _fare = 0
        else:
            _fare = int(_num) * 10000

        call_type_lst.append(_cat_str)
        fare_lst.append(_fare)

    return call_type_lst, fare_lst
