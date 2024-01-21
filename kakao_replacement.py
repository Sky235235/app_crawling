import time
from utils import Eng2Kor, ImgProcessing
import cv2

def run(departure_address, arrival_address, device):

    # --- 1.카카오 T 앱 오픈
    print('App Open')
    device.shell("monkey -p com.kakao.taxi")
    time.sleep(8.0)

    # ---- 1.1 카카오 T 앱 오픈 후 비정상 종료 확인
    img_process = ImgProcessing()
    main_img = device.screencap()
    print('Check Non_formal termination')
    with open('screenshot/kakao_T_main_compare.png', 'wb') as f:
        f.write(main_img)
    print('screenshot app main img save')
    time.sleep(5.0)

    bluestack_main_img_path = 'screenshot/bluestack_main_img.png'
    main_compare_path = 'screenshot/kakao_T_main_compare.png'
    check_img_similarity = img_process.compare_image(bluestack_main_img_path, main_compare_path)
    print('check termination', check_img_similarity)
    tried = 1
    while check_img_similarity >= 0.9:
        # 블루스택 메인 화면과 유사도가 0.9 이상이면 앱 비정상 종료로 판단 하고 앱 재실행
        print(f'App Open Again {tried}')
        device.shell('am force-stop com.kakao.taxi')
        time.sleep(2.0)
        device.shell("monkey -p com.kakao.taxi ")
        time.sleep(8.0)
        main_img_again = device.screencap()
        print(f'Check Non_formal termination {tried} try')
        with open('screenshot/kakao_T_main_compare.png', 'wb') as f:
            f.write(main_img_again)
        print(f'screenshot app main img save {tried}')
        time.sleep(5.0)
        check_img_similarity = img_process.compare_image(bluestack_main_img_path, main_compare_path)
        tried += 1

        if check_img_similarity < 0.9:
            print('Move Next step')
    else:
        print('App is Running')
    
    # --- 1.2 Popup 화면 확인
    app_main_img = device.screencap()
    print('Check Main Pop-up AD')
    with open('screenshot/check_main_popup.png', 'wb') as f:
        f.write(app_main_img)
    print('screenshot check main popup img save')
    time.sleep(3.0)

    app_main_img_path = 'screenshot/kakao_T_main.png'
    check_ad_pop_path = 'screenshot/check_main_popup.png'
    check_ad_img_similarity = img_process.compare_image(app_main_img_path, check_ad_pop_path)
    print('check main popup ad', check_ad_img_similarity)

    if check_ad_img_similarity < 0.9:
        no_show_Position = ''
        device.shell(f"input tap {no_show_Position}")
        time.sleep(1.5)
    else:
        print('No Pop-up AD')

    # --- 2.대리 아이콘 터치
    print('Touch Icon')
    icon_Position = ''
    device.shell(f"input tap {icon_Position}")
    time.sleep(2.5)

    # ----2.1 광고 확인
    print('define advertise')

    ad_img = device.screencap()
    with open('screenshot/compare_img.png', 'wb') as f:
        f.write(ad_img)
    print('screenshot ad img save')
    time.sleep(5.0)

    base_img_path = 'screenshot/kakao_replacement.png'
    compare_img_path = 'screenshot/compare_img.png'

    img_similarity = img_process.compare_image(base_img_path, compare_img_path)
    print('img_similarity', img_similarity)

    if img_similarity < 0.9:
        # 유사도가 0.9 미만이면 뒤로 갔다가 대리아이콘 다시 터치
        print('back')
        device.shell("input keyevent KEYCODE_BACK")
        time.sleep(2.0)

        print('Touch Icon again')
        icon_Position = ''
        device.shell(f"input tap {icon_Position}")
        time.sleep(2.5)

    else:
        print('no address popup ad')
    # --- 3.출발지 검색창 터치
    print('search departure')
    departure_Position = ''
    device.shell(f"input tap {departure_Position}")
    time.sleep(3.0)

    # --- 4. 검색창의 "x" 아이콘 터치
    remove_Position = ''
    device.shell(f"input tap {remove_Position}")
    time.sleep(3.0)

    # --- 5.출발지를 영어로로 검색
    #### 출발지를 영어 알파벳으로 변경
    eng2kr = Eng2Kor()
    if departure_address == 'wework':
        result = departure_address
    else:
        departure_address_kr = departure_address
        result = eng2kr.split(departure_address_kr)
    device.shell(f"input text {result}")
    time.sleep(3.0)

    # --- 6. 검색으로 나온 출발지 터치

    if departure_address == 'wework':
        start_address_Position = ''

    else:
        start_address_Position = ''
    device.shell(f"input tap {start_address_Position}")
    time.sleep(3.0)

    # --- 7. 검색으로 나온 출발지의 "출발" 버튼 터치
    start_click_Position = ''
    device.shell(f"input tap {start_click_Position}")
    time.sleep(5.0)

    # --- 8. 도착지 검색 창 터치
    print('search arrival')
    arrival_Position = ''
    device.shell(f"input tap {arrival_Position}")
    time.sleep(4.0)

    # --- 9. 도착지 주소 입력
    arrival_address_kr = arrival_address
    arrival_result = eng2kr.split(arrival_address_kr)
    device.shell(f"input text {arrival_result}")
    time.sleep(3.0)

    # --- 10. 검색된 도착지 주소 클릭
    end_Position = ''
    device.shell(f"input tap {end_Position}")
    time.sleep(1.5)
    end_click_Position = ''
    device.shell(f"input tap {end_click_Position}")
    time.sleep(3.0)

    # --- 11. "빠른배정 팝업 제거 임의의 화면 터치"
    touch_Position = ''
    device.shell(f"input tap {touch_Position}")
    time.sleep(1.5)

    # --- 12. 요금 스크린샷
    print('screenshot fare img')
    fare_screen = device.screencap()
    with open('screenshot/fare_img.png', 'wb') as fp:
        fp.write(fare_screen)

    # ---- 13. 카카오 택시 앱 종료
    device.shell('am force-stop com.kakao.taxi')
    time.sleep(2.0)