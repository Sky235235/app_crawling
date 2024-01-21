import time
from utils import Eng2Kor, ImgProcessing
from utils import AppConnect

def run(departure_address, arrival_address, device):
    # --- 1. T맵 오픈
    print('T Map Open')
    device.shell("monkey -p com.skt.tmap.ku")
    time.sleep(6.0)

    # --- 1.1 T맵 비정상 종료 체크

    # --- 1.2 메인화면 광고 팝업 체크
    print('Check ad pop-up')
    img_process = ImgProcessing()
    t_map_main_img = device.screencap()

    with open('screenshot/t_map_main_compare.png', 'wb') as f:
        f.write(t_map_main_img)
    print('screenshot app main img save')
    time.sleep(3.0)
    main_img_path = 'screenshot/t_map_main.png'
    main_compare_img_path = 'screenshot/t_map_main_compare.png'
    check_img_similarity = img_process.compare_image(main_img_path, main_compare_img_path)
    print('check main ad popup', check_img_similarity)

    if check_img_similarity < 0.9:
        ## 광고 팝업 뜨면 오늘은 그만 보기 터치
        ad_popup_Position = ''
        device.shell(f"input tap {ad_popup_Position}")
        time.sleep(2.5)

    else:
        print('no ad pop_up continue')

    # --- 2. 대리운전 카테고리 터치
    replacement_Position = ''
    device.shell(f"input tap {replacement_Position}")
    time.sleep(2.5)

    # --- 2.1 대리운전 광고 팝업 체크
    t_map_input_address_img = device.screencap()
    with open('screenshot/t_map_input_address_compare.png', 'wb') as f:
        f.write(t_map_input_address_img)
    print('screenshot t map input address img save')
    time.sleep(5.0)
    input_img_path = 'screenshot/t_map_input_address.png'
    input_compare_img_path = 'screenshot/t_map_input_address_compare.png'
    check_img_similarity = img_process.compare_image(main_img_path, main_compare_img_path)
    print('check input address ad popup', check_img_similarity)

    if check_img_similarity < 0.9:
        ## 광고 팝업 뜨면 오늘은 그만 보기 터치
        input_ad_Position = ''
        device.shell(f"input tap {input_ad_Position}")
        time.sleep(2.5)

    else:
        print('no input ad pop_up continue')

    # --- 3. 출발지 입력
    departure_Position = ''
    device.shell(f"input tap {departure_Position}")
    time.sleep(3.0)
    _departure_address = departure_address
    eng2kor = Eng2Kor()

    result = eng2kor.split(_departure_address)
    upper_result = result.upper()

    for _text in upper_result:
        device.shell(f"input keyevent KEYCODE_{_text}")
        time.sleep(0.2)
    time.sleep(2.0)
    ### 자동완성 탭
    point_Position = ''
    device.shell(f"input tap {point_Position}")
    time.sleep(3.0)
    ### 세부 사항  탭
    point_detail_Position = ''
    device.shell(f"input tap {point_detail_Position}")
    time.sleep(3.0)
    #### "출발지로 설정하기" 탭
    departure_tap_Position = ''
    device.shell(f"input tap {departure_tap_Position}")
    time.sleep(3.0)

    # --- 4. 도착지 입력
    arrival_input_Position = ''
    device.shell(f"input tap {arrival_input_Position}")
    time.sleep(3.0)
    _arrival_address = arrival_address
    arrival_result = eng2kor.split(_arrival_address)
    arrival_upper_result = arrival_result.upper()

    for _arrival_text in arrival_upper_result:
        device.shell(f"input keyevent KEYCODE_{_arrival_text}")
        time.sleep(0.2)
    time.sleep(3.0)
    ### 자동완성 탭
    arrival_point_Position = ''
    device.shell(f"input tap {arrival_point_Position}")
    time.sleep(3.0)
    ### 도착지 세부 지역 탭
    arrival_detail_Position = ''
    device.shell(f"input tap {arrival_detail_Position}")
    time.sleep(3.0)
    ### 도착지로 설정하기 탭
    arrival_tap_Position = ''
    device.shell(f"input tap {arrival_tap_Position}")
    time.sleep(5.0)

    # --- 5. 요금 이미지 캡처
    print('screenshot T Map fare img')
    fare_screen = device.screencap()
    with open('screenshot/t_map_fare_img.png', 'wb') as fp:
        fp.write(fare_screen)
    time.sleep(2.0)

    # --- 6. 티맵 종료
    device.shell('am force-stop com.skt.tmap.ku')
    time.sleep(2.0)