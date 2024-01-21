from ppadb.client import Client
from jamo import h2j, j2hcj
import cv2
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account

class AppConnect:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        client = Client(host=self.host, port=self.port)
        find_devices = client.devices()

        if len(find_devices) == 0:
            print('No devices')
            quit()

        device = find_devices[0]
        print(f'찾은 디바이스{device}')

        return device, client
class Eng2Kor:
    def __init__(self):
        self.korean_alphabet = {
            'ㄱ': 'r',
            'ㄴ': 's',
            'ㄷ': 'e',
            'ㄹ': 'f',
            'ㅁ': 'a',
            'ㅂ': 'q',
            'ㅅ': 't',
            'ㅇ': 'd',
            'ㅈ': 'w',
            'ㅊ': 'c',
            'ㅋ': 'z',
            'ㅌ': 'x',
            'ㅍ': 'v',
            'ㅎ': 'g',
            'ㅏ': 'k',
            'ㅑ': 'i',
            'ㅓ': 'j',
            'ㅕ': 'u',
            'ㅜ': 'n',
            'ㅠ': 'b',
            'ㅗ': 'h',
            'ㅛ': 'y',
            'ㅡ': 'm'
            , 'ㅣ': 'l'
            , 'ㅐ': 'o'
            , 'ㅔ': 'p'
            , 'ㅚ': 'hl'
            , 'ㅟ': 'nl'
            , 'ㅒ': 'O'
            , 'ㅖ': 'P'
            , 'ㅘ': 'hk'
            , 'ㅙ': 'ho'
            , 'ㅝ': 'nj'
            , 'ㅞ': 'np'
            , 'ㅢ': 'ml'
        }

    def split(self, text):
        jamo_str = j2hcj(h2j(text))

        to_english_lst = []
        for i in range(len(jamo_str)):

            if jamo_str[i].isdigit():
                answer = jamo_str[i]
            else:
                answer = self.korean_alphabet[jamo_str[i]]
            to_english_lst.append(answer)

        result = ''.join(to_english_lst)
        print(result)
        return result

class ImgProcessing:

    def compare_image(self, base_img_path, compare_img_path):

        #이미지 크기 조정

        image1 = cv2.imread(base_img_path)
        image2 = cv2.imread(compare_img_path)

        # 그레이 스케일로 변환
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # 히스토그램 계산
        hist1 = cv2.calcHist([image1_gray], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([image2_gray], [0], None, [256], [0, 256])

        # 히스토그램 비교
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

        return similarity

class Bigquery:
    def __init__(self, KEY_PATH):
        self.KEY_PATH = KEY_PATH

    def insert_bigquery_table(self, table_id, df):
        credentials = service_account.Credentials.from_service_account_file(self.KEY_PATH)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        table = client.get_table(table_id)
        client.load_table_from_dataframe(df, table)
        print("insert successfully")

    def get_bigquery_data(self, query):
        credentials = service_account.Credentials.from_service_account_file(self.KEY_PATH)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        bqstorage_client = bigquery_storage.BigQueryReadClient(credentials=credentials)
        query_job = client.query(query)
        df = query_job.to_dataframe(bqstorage_client=bqstorage_client)

        return df



