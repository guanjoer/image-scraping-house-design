from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os
import mimetypes
import imghdr

driver = webdriver.Chrome() # 크롬 브라우저 열기
driver.maximize_window() # 창 최대화

url = "https://www.arkaenergy.com/learn/modern-house-ideas"
driver.get(url=url) # url 접속
driver.implicitly_wait(time_to_wait=10) # 화면 로드 완료 시까지 최대 10초 휴식



# 웹 페이지 끝까지 내리기
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    else:
        last_height = new_height



links = []
images = driver.find_elements(By.CSS_SELECTOR, ".w-richtext-align-fullwidth.w-richtext-figure-type-image img") # 이미지 썸네일
for image in images:
    src = image.get_attribute('src')
    if src: # 'src' 속성이 존재할 시
        links.append(src) # 리스트에 추가

print(links)

# 이미지 저장 폴더 생성
os.makedirs("./downloaded_images", exist_ok=True)

# headers 설정
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# 이미지 다운로드 및 저장
for i, link in enumerate(links):
    req = urllib.request.Request(link, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        # 임시 파일에 저장하여 확장자를 확인
        temp_file_path = f"./downloaded_images/temp_image_{i+1}"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(data)
        
        # 확장자 확인
        image_type = imghdr.what(temp_file_path)
        if image_type:
            image_file_path = f"./downloaded_images/image_{i+1}.{image_type}"
            os.rename(temp_file_path, image_file_path)
        else:
            os.remove(temp_file_path)

print("다운로드를 성공적으로 완료하였습니다.")

# 브라우저 닫기
driver.quit()


