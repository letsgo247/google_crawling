# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup as soups
import time
import socket
import os

from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')



### 스크롤 끝까지 ###
def scroll_down_to_the_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        print(last_height)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            break

        else:
            last_height = new_height



### 클릭해서 기다렸다가 원본 사진 뜨면 저장 ###
def click_and_retrieve(index, img, img_list_length, query, driver):
    global crawled_count

    # try: 
    #     os.makedirs(f'idol/{query}') 
    # except OSError: 
    #     if not os.path.isdir(f'idol/{query}'): 
    #         raise

    try:
        img.click()
        time.sleep(1.5)
        driver.implicitly_wait(3)
        src = None
        _format = None

        try:
            srces = driver.find_elements_by_class_name("""n3VNCb""")
            for _src in srces:
                src = _src.get_attribute('src')
                _format = src.split('.')[-1]
                if any(map(lambda x: _format == x, ['jpg', 'jpeg', 'png'])):
                    break
                else:
                    continue
            if not any(map(lambda x: _format == x, ['jpg', 'jpeg', 'png'])):
                print(f'no jpg.... pass ({_format})')
                return
        except:
            print('error2')
        # src.split('.')[-1] = 확장자
        if src is None or _format is None:
            return

        # 저장
        urlretrieve(src, f"idol/{query}{crawled_count + 1}.{_format}")
        driver.implicitly_wait(3)
        print(f"{index + 1} / {img_list_length} 번째 사진 저장 ({_format})")
        crawled_count += 1

    except HTTPError:
        print("ㅡ HTTPError & 패스 ㅡ")
        pass

    except:
        pass





### main ###
def search_selenium(search_name, search_limit) :
    search_url = "https://www.google.com/search?q=" + str(search_name) + "&hl=ko&tbm=isch"
    
    driver = webdriver.Chrome('c:/dev/Crawling/chromedriver.exe', options=options) # 경로 변경
    driver.get(search_url)
    
    scroll_down_to_the_end(driver)
    
    div = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]')
    # print(div)
    img_list = div.find_elements_by_css_selector(".rg_i.Q4LuWd")
    print(f'searched # of image: {len(img_list)}')

    for index, img in enumerate(img_list):
        search_limit -= 1        
        if search_limit == 0:
            break

        try:
            click_and_retrieve(index, img, len(img_list), search_name, driver)

        except ElementClickInterceptedException:
            print("ㅡ ElementClickInterceptedException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            img.click()
            time.sleep(3)
            click_and_retrieve(index, img, len(img_list))

        except NoSuchElementException:
            print("ㅡ NoSuchElementException ㅡ")
            driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
            print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
            time.sleep(3)
            img.click()
            click_and_retrieve(index, img, len(img_list))

        except ConnectionResetError:
            print("ㅡ ConnectionResetError & 패스 ㅡ")
            pass

        except URLError:
            print("ㅡ URLError & 패스 ㅡ")
            pass

        except socket.timeout:
            print("ㅡ socket.timeout & 패스 ㅡ")
            pass

        except socket.gaierror:
            print("ㅡ socket.gaierror & 패스 ㅡ")
            pass

        except ElementNotInteractableException:
            print("ㅡ ElementNotInteractableException ㅡ")
            break

    try:
        print("ㅡ 크롤링 종료 (성공률: %.2f%%) ㅡ" % (crawled_count / len(img_list) * 100.0))

    except ZeroDivisionError:
        print("ㅡ img_list 가 비어있음 ㅡ")

    driver.quit()

        


    


    

    



    
    # image_count = len(driver.find_elements_by_tag_name("img"))
    
    # print("로드된 이미지 개수 : ", image_count)

    # driver.implicitly_wait(2)

    # for i in range( search_limit ) :
    #     image = driver.find_elements_by_tag_name("img")[i]
    #     image.screenshot("c:/dev/KFG/Data/idol/" + str(search_name) + str(i) + ".png") # 경로 변경

    # driver.close()



# search_selenium('아이유', 100)


idol_girl_list = ['전소미', '김세정', '최유정', '김청하', '김소혜', '주결경', '정채연', '김도연', '강미나', '임나영', '유연정', '소원', '예린', '은하', '유주', '신비', '엄지', '채경', '채원', '나은', '예나', '레이첼', '진솔', '나라', '앨리스', '라임', '유영', '서영', '여름', '보람', '지연', '효민', '은정', '큐리', '소연', '오승희', '최유진', '장예은', '엘키', '장승연', 'SORN', '권은빈', '지민', '초아', '유나', '혜정', '민아', '설현', '찬미', '박초롱', '윤보미', '정은지', '손나은', '김남주', '오하영', '나연', '정연', '모모', '사나', '지효', '미나', '다현', '채영', '쯔위', '지아', '민', '수지', '페이']
idol_boy_list = ['태일', '쟈니', '태용', '유타', '도영', '텐', '재현', '윈윈', '마크', '런쥔', '제노', '해찬', '재민', '천러', '지성', '지코', '태일', '재효', '비범', '피오', '박경', '유권', 'JB', '마크', '잭슨', '진영', '영재', '뱀뱀', '유겸', '동현', '현성', '정민', '영민', '광민', '민우', '수호', '찬열', '카이', '디오', '백현', '세훈', '시우민', '레이', '첸', '타오', '루한', '크리스', '온유', '종현', 'Key', '민호', '태민', '한승우', '강승식', '허찬', '임세준', '도한세', '최병찬', '정수빈', '시월', '재빈', '만니', '리호', '다원', '승보', '블릿', '데이먼', '씬', '엔써니', '키드', '윤호', '서은광', '이민혁', '이창섭', '임현식', '프니엘', '정일훈', '육성재', '진호', '후이', '홍석', '이던', '신원', '여원', '옌안', '유토', '키노', '우석']

for name in idol_girl_list:
    print(f'### {name} ###')
    crawled_count = 0
    search_selenium(name, 100)