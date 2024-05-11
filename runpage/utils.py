# utils.py

import pandas as pd
import csv
import os

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

def crawl_data(start_date, end_date):
    # 크롤링 코드를 작성하세요
    # 입력된 날짜를 기반으로 데이터를 크롤링하고 결과를 반환합니다.

    # 저장할 폴더 경로
    folder_path = './afhelper_capture'

    # 폴더가 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 크롤링할 사이트 주소 = 아프리카도우미
    etc_data_url = f"http://rank.afreehp.kr/user#maxview!{start_date},{end_date}/a|"

    # 수정하실 땐 BJ 아이디와 닉네임 순서를 맞추셔야합니다.

    bj_id = ['wnnw',
            'skygkrtn', 'vlfvlf789', 'p0r0r0',
            'sunwo2534', 'churros05', 'kchoij',
            'yunhee1222',
            'damikim', 'jha0331', 'jyurim99', 'rrrr4719', '1000song2', 'wendysul', '2boo2boo', 'domangcha13', 'taeri0806', 'hhy2124', 'b24ip7',
            'indy1028',
            'tlswlgus95', 'dkjfke', 'ooo9330', 'jieujieun11', 'goodb99', 'thwl9386', 'tpqhrdl', 'ekdus0830', 'name1234', 'taezzang9', 'danstar11']

    bj_name = ['남순',
            '김학수' , '빵훈', '날박',                              
            '최깨비', '쮸러스', '로링',                         
            '깅예솔',                                                  
            '[DM]퀸다미', '아띠_♥', '겸둥이', '류하♡', '강민아', '설하', '뚜부', '도원', '태리츄','츄릅쪼앙', '민서율',
            '안예슬',                                                    
            '져리', '빡다혜', '진솔', '미캣', '배그나', '지붕위소희', '권도연', '백다연', '안녕하소', '태은짱', '단별짱']

    # bj_id = ['wnnw',
    #          'skygkrtn', 'vlfvlf789', 'p0r0r0', 'cinnamoroll']

    # bj_name = ['남순',
    #            '김학수' , '빵훈', '날박', '눈또']

    count_total_people = []
    count_time = []
    count_max_people = []
    count_accr_people = []
    count_followers = []
    count_accr_followers = []


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 3600)

    for i in range(len(bj_id)):

        # 아프 도우미로 데이터 조회
        final_etc_data_url = etc_data_url + bj_id[i]  
        driver.get(final_etc_data_url)
        
        # 총 즐겨찾기 수
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[2]/td/div/p'))).text
        count_followers.append(temp)

        # 기간내 증감 즐겨찾기 수
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[2]/td/div/div[2]/p[1]'))).text
        count_accr_followers.append(temp)
        
        # 총 누적 시청자 수
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[5]/td/div/p'))).text
        count_total_people.append(temp)

        # 기간내 누적 시청자 수
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[5]/td/div/div[2]/p[1]'))).text
        count_accr_people.append(temp)

        # 기간 내 방송시간
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[10]/td/div/p'))).text
        count_time.append(temp)

        # 기간 내 최대 시청자 수
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[4]/table/tbody/tr[9]/td/div/p'))).text
        count_max_people.append(temp)

        # 기간 내 최대 시청자 수가 나타난 날짜 캡쳐
        temp = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div[3]/div[2]')))
        time.sleep(2)
        screenshot_path = os.path.join(folder_path, bj_name[i] + '_afhelper.png')
        temp.screenshot(screenshot_path)


    # 현재 날짜를 포함한 파일명 생성
    current_date = datetime.now().strftime("%Y-%m-%d")
    csv_file = f"afhelper_data_{start_date}~{end_date}.csv"

    # CSV 파일 쓰기
    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        # 헤더 쓰기
        writer.writerow(['BJ Name', '총 즐겨찾기 수', '증감 즐겨찾기수', '방송시간', '최대 시청자 수', '기간내 누적 시청자수', '총 누적 시청자수'])

        # 데이터 쓰기
        for j in range(len(bj_name)):
            writer.writerow([bj_name[j], count_followers[j], count_accr_followers[j], count_time[j], count_max_people[j], count_accr_people[j], count_total_people[j]])

    print(f"CSV 파일 '{csv_file}'이 생성되었습니다.")

    # for j in range(len(bj_name)):
    #     print('*' * 50)
    #     print(bj_name[j] + ' ' + '풍력 : ' + count_baloon[j] + ' ' + '방송시간 : ' + count_time[j] + ' ' + '최대 시청자 수 : ' + count_max_people[j])

    # 드라이버 종료
    driver.quit()   
