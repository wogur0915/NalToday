import pandas as pd
import csv

import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

start_date = input("조회 시작 날짜를 입력하세요(예: 240301): ")
end_date = input("조회 종료 날짜를 입력하세요(예: 240315): ")

# 크롤링할 사이트 주소 = 풍투데이
poong_url = "https://static.poong.today/chart/day/"

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
#          'skygkrtn', 'vlfvlf789', 'p0r0r0']

# bj_name = ['남순',
#            '김학수' , '빵훈', '날박']

count_baloon = []
count_time = []
count_change_times = []
count_max_people = []
count_total_people = []


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)


# 풍투데이 조회

# 시작 날짜와 종료 날짜 파싱
start_datetime = datetime.strptime(start_date, "%y%m%d")
end_datetime = datetime.strptime(end_date, "%y%m%d")

# 시작 날짜부터 종료 날짜까지 모든 날짜 생성
date_range = [start_datetime + timedelta(days=x) for x in range((end_datetime - start_datetime).days + 1)]

# 각 날짜에 대한 URL 생성
detail_urls = []
for date in date_range:
    detail_url = poong_url + "20" + date.strftime("%y/%m/%d")
    detail_urls.append(detail_url)

driver.get(detail_urls[0])
for i in range(len(bj_name)):
    searchbox = driver.find_element(By.XPATH, "//*[@id='main_chart_controler']/div[3]/input")
    searchbox.clear() 
    searchbox.send_keys(bj_id[i])
    try:
        # 풍력 조회

        # check가 순위(전체순위)가 될 때까지 대기
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='chart_header_rank']"), "순위(전체순위)"))
        temp_xpath = '//*[@id="main_chart_item_fixed_' + bj_id[i] + '"]/div[4]'
        temp = driver.find_element(By.XPATH, temp_xpath).text
        value_int = int(temp.replace(",", ""))
        count_baloon.append(int(value_int))
    except NoSuchElementException:
        # 요소를 찾지 못한 경우 생략
        count_baloon.append(0)
        continue

for detail_url in detail_urls[1:]:
    driver.get(detail_url)
    for i in range(len(bj_name)):
        searchbox = driver.find_element(By.XPATH, "//*[@id='main_chart_controler']/div[3]/input")
        searchbox.clear() 
        searchbox.send_keys(bj_id[i])
        try:
            # 풍력 조회
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='chart_header_rank']"), "순위(전체순위)"))
            temp_xpath = '//*[@id="main_chart_item_fixed_' + bj_id[i] + '"]/div[4]'
            temp = driver.find_element(By.XPATH, temp_xpath).text   
            value_int = int(temp.replace(",", ""))
            count_baloon[i] += int(value_int)
        except NoSuchElementException:
            # 요소를 찾지 못한 경우 생략
            count_baloon.append(0)
            continue

# 범위 날짜를 포함한 파일명 생성
csv_file = f"pt_speed_data_{start_date}~{end_date}.csv"

# CSV 파일 쓰기
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    # 헤더 쓰기
    writer.writerow(['BJ Name', '풍력'])

    # 데이터 쓰기
    for j in range(len(bj_name)):
        writer.writerow([bj_name[j], str(count_baloon[j])])

print(f"CSV 파일 '{csv_file}'이 생성되었습니다.")

# 드라이버 종료
driver.quit()